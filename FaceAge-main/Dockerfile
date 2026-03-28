FROM python:3.11-slim

WORKDIR /app

# System deps for OpenCV headless
RUN apt-get update && \
    apt-get install -y --no-install-recommends libgl1 libglib2.0-0 && \
    rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY models/faceage_model.onnx models/faceage_model.onnx
COPY models/face_landmarker.task models/face_landmarker.task
COPY app.py .

EXPOSE 8000

CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]
