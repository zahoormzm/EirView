"""
FaceAge Microservice — FastAPI application.

Receives an image, detects and aligns the face using MediaPipe,
runs the ONNX age-prediction model, and returns the estimated
biological age as JSON.

Start with:
    uvicorn app:app --host 0.0.0.0 --port 8000
"""

import os
import math
from typing import Optional

import cv2
import numpy as np
import mediapipe as mp
import onnxruntime as ort
from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.responses import JSONResponse

# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------
MODEL_PATH = os.environ.get(
    "FACEAGE_MODEL_PATH",
    os.path.join(os.path.dirname(__file__), "models", "faceage_model.onnx"),
)
LANDMARKER_PATH = os.environ.get(
    "FACE_LANDMARKER_PATH",
    os.path.join(os.path.dirname(__file__), "models", "face_landmarker.task"),
)
REQUIRED_SIZE = (160, 160)

# ---------------------------------------------------------------------------
# Load ONNX model once at startup
# ---------------------------------------------------------------------------
app = FastAPI(title="FaceAge", version="2.0.0")

_session: Optional[ort.InferenceSession] = None


def get_session() -> ort.InferenceSession:
    global _session
    if _session is None:
        if not os.path.isfile(MODEL_PATH):
            raise RuntimeError(
                f"ONNX model not found at {MODEL_PATH}. "
                "Run scripts/convert_h5_to_onnx.py first."
            )
        _session = ort.InferenceSession(
            MODEL_PATH, providers=ort.get_available_providers()
        )
    return _session


# ---------------------------------------------------------------------------
# MediaPipe FaceLandmarker setup (replaces MTCNN)
# ---------------------------------------------------------------------------
_landmarker: Optional[mp.tasks.vision.FaceLandmarker] = None


def get_landmarker() -> mp.tasks.vision.FaceLandmarker:
    global _landmarker
    if _landmarker is None:
        base_options = mp.tasks.BaseOptions(model_asset_path=LANDMARKER_PATH)
        options = mp.tasks.vision.FaceLandmarkerOptions(
            base_options=base_options,
            running_mode=mp.tasks.vision.RunningMode.IMAGE,
            num_faces=1,
            min_face_detection_confidence=0.5,
            min_face_presence_confidence=0.5,
        )
        _landmarker = mp.tasks.vision.FaceLandmarker.create_from_options(options)
    return _landmarker


# MediaPipe FaceLandmarker landmark indices for eye centres
# With refine_landmarks, iris landmarks are at 468-477
_LEFT_IRIS = 468
_RIGHT_IRIS = 473
# Fallback: eye corner averages
_LEFT_EYE_INNER = 133
_LEFT_EYE_OUTER = 33
_RIGHT_EYE_INNER = 362
_RIGHT_EYE_OUTER = 263


def _eye_centres(landmarks, w: int, h: int):
    """Return (left_eye_xy, right_eye_xy) in pixel coordinates."""
    def lm(idx):
        p = landmarks[idx]
        return np.array([p.x * w, p.y * h])

    if len(landmarks) > _RIGHT_IRIS:
        left = lm(_LEFT_IRIS)
        right = lm(_RIGHT_IRIS)
    else:
        left = (lm(_LEFT_EYE_INNER) + lm(_LEFT_EYE_OUTER)) / 2
        right = (lm(_RIGHT_EYE_INNER) + lm(_RIGHT_EYE_OUTER)) / 2

    return left, right


def _align_and_crop(image_rgb: np.ndarray) -> np.ndarray:
    """Detect, align, and crop the face to 160x160, mimicking the original
    MTCNN pipeline (direct bounding-box crop with no extra padding)."""

    h, w, _ = image_rgb.shape

    # Use MediaPipe Tasks API
    mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=image_rgb)
    landmarker = get_landmarker()
    result = landmarker.detect(mp_image)

    if not result.face_landmarks:
        raise ValueError("No face detected in the image.")

    lms = result.face_landmarks[0]
    left_eye, right_eye = _eye_centres(lms, w, h)

    # --- Affine rotation to level the eyes ---
    dx = right_eye[0] - left_eye[0]
    dy = right_eye[1] - left_eye[1]
    angle = math.degrees(math.atan2(dy, dx))

    eye_center = ((left_eye + right_eye) / 2).astype(np.float32)
    rot_mat = cv2.getRotationMatrix2D(tuple(eye_center), angle, scale=1.0)
    aligned = cv2.warpAffine(image_rgb, rot_mat, (w, h), flags=cv2.INTER_LINEAR)

    # --- Compute bounding box from all landmarks (post-rotation) ---
    pts = np.array([[l.x * w, l.y * h] for l in lms], dtype=np.float64)
    ones = np.ones((pts.shape[0], 1))
    pts_h = np.hstack([pts, ones])  # (N, 3)
    pts_rot = (rot_mat @ pts_h.T).T  # (N, 2)

    x_min, y_min = pts_rot.min(axis=0)
    x_max, y_max = pts_rot.max(axis=0)

    # The original MTCNN gives a tight box. MediaPipe mesh hugs the face
    # contour tightly, so we add a small margin (~10%) to approximate the
    # MTCNN bounding box which includes a bit of forehead and chin.
    bw = x_max - x_min
    bh = y_max - y_min
    margin_x = bw * 0.10
    margin_y = bh * 0.10

    x1 = max(int(x_min - margin_x), 0)
    y1 = max(int(y_min - margin_y), 0)
    x2 = min(int(x_max + margin_x), w)
    y2 = min(int(y_max + margin_y), h)

    face_crop = aligned[y1:y2, x1:x2]
    if face_crop.size == 0:
        raise ValueError("Face crop resulted in empty image.")

    # Resize to model input size (bilinear, same as original PIL resize)
    face_crop = cv2.resize(face_crop, REQUIRED_SIZE, interpolation=cv2.INTER_LINEAR)
    return face_crop


def _normalize(face: np.ndarray) -> np.ndarray:
    """Per-sample global mean/std normalization — exact copy of original code:
        mean, std = face_pixels.mean(), face_pixels.std()
        face_pixels = (face_pixels - mean) / std
    """
    face = face.astype(np.float32)
    mean = face.mean()
    std = face.std()
    if std == 0:
        std = 1.0
    return (face - mean) / std


# ---------------------------------------------------------------------------
# API endpoint
# ---------------------------------------------------------------------------
@app.post("/predict_age")
async def predict_age(file: UploadFile = File(...)):
    """Accept an image upload and return the predicted biological age."""

    contents = await file.read()
    if not contents:
        raise HTTPException(status_code=400, detail="Empty file.")

    nparr = np.frombuffer(contents, np.uint8)
    image_bgr = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
    if image_bgr is None:
        raise HTTPException(status_code=400, detail="Could not decode image.")

    image_rgb = cv2.cvtColor(image_bgr, cv2.COLOR_BGR2RGB)

    try:
        face = _align_and_crop(image_rgb)
    except ValueError as exc:
        raise HTTPException(status_code=422, detail=str(exc))

    face = _normalize(face)
    face_input = face.reshape(1, 160, 160, 3)

    session = get_session()
    input_name = session.get_inputs()[0].name
    output = session.run(None, {input_name: face_input})
    age = float(output[0].flatten()[0])

    return JSONResponse(
        content={"status": "success", "biological_age": round(age, 1)}
    )


@app.get("/health")
async def health():
    return {"status": "ok"}
