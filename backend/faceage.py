from __future__ import annotations

import os
from typing import Any

import cv2
import numpy as np

ONNX_MODEL: str = os.getenv("FACEAGE_MODEL_PATH", "../FaceAge-main/models/faceage_model.onnx")
LANDMARKER: str = os.getenv("FACE_LANDMARKER_PATH", "../FaceAge-main/models/face_landmarker.task")
_session: Any = None


def _get_session() -> Any:
    """Lazy-load ONNX runtime session."""

    global _session
    if _session is None:
        if not os.path.exists(ONNX_MODEL):
            raise FileNotFoundError(f"FaceAge ONNX model not found at {ONNX_MODEL}")
        import onnxruntime as ort  # type: ignore

        _session = ort.InferenceSession(ONNX_MODEL)
    return _session


def detect_and_crop_face(img: np.ndarray) -> np.ndarray | None:
    """Detect a face using MediaPipe and return a cropped region."""

    try:
        import mediapipe as mp  # type: ignore
    except Exception as exc:  # pragma: no cover - native dependency import
        raise RuntimeError("MediaPipe face detection is unavailable in this environment") from exc

    with mp.solutions.face_detection.FaceDetection(model_selection=1, min_detection_confidence=0.5) as detector:
        rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        results = detector.process(rgb)
        if not results.detections:
            return None
        bbox = results.detections[0].location_data.relative_bounding_box
        h, w, _ = img.shape
        x = max(0, int(bbox.xmin * w))
        y = max(0, int(bbox.ymin * h))
        bw = int(bbox.width * w)
        bh = int(bbox.height * h)
        margin_x = int(bw * 0.2)
        margin_y = int(bh * 0.2)
        x1 = max(0, x - margin_x)
        y1 = max(0, y - margin_y)
        x2 = min(w, x + bw + margin_x)
        y2 = min(h, y + bh + margin_y)
        crop = img[y1:y2, x1:x2]
        return crop if crop.size else None


def predict_face_age(image_bytes: bytes) -> float:
    """Run FaceAge ONNX inference and return predicted age."""

    session = _get_session()
    image = cv2.imdecode(np.frombuffer(image_bytes, np.uint8), cv2.IMREAD_COLOR)
    if image is None:
        raise ValueError("Could not decode image")
    crop = detect_and_crop_face(image)
    if crop is None:
        raise ValueError("No face detected in the image")
    face = cv2.resize(crop, (224, 224)).astype(np.float32) / 255.0
    face = np.transpose(face, (2, 0, 1))
    face = np.expand_dims(face, 0)
    output = session.run(None, {session.get_inputs()[0].name: face})
    predicted_age = output[0]
    if isinstance(predicted_age, np.ndarray):
        predicted_age = float(predicted_age.reshape(-1)[0])
    return round(float(predicted_age), 1)
