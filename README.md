# EirView

EirView is a full-stack health intelligence platform that combines deterministic health calculations, multi-source data ingestion, and AI-assisted coaching. It runs locally with a React frontend, a FastAPI backend, SQLite storage, and a small agent/tool layer for guided reasoning tasks.

## What It Does

- Computes biological age across cardiovascular, metabolic, musculoskeletal, and neurological subsystems
- Tracks health data from blood reports, body composition scans, Apple Health exports, meals, posture checks, and manual entries
- Projects medium-term health risks and supports what-if scenario simulation
- Provides contextual coaching for activity, nutrition, future-self reflection, and mental health support
- Surfaces reminders, alerts, specialist recommendations, and data freshness timelines

## Stack

**Frontend**
- React 19, Vite, Tailwind CSS, Zustand, Recharts

**Backend**
- FastAPI, SQLite with `aiosqlite`
- Deterministic health and risk logic in Python
- Claude and Gemini API integrations for parsing and coaching flows

**Supporting Services**
- Spotify Web API
- OpenWeatherMap
- USDA food data
- ONNX Runtime for face age inference
- MediaPipe Tasks for browser posture analysis

## Repository Layout

```
Health/
├── backend/
│   ├── main.py
│   ├── database.py
│   ├── formulas.py
│   ├── reminder_engine.py
│   ├── activity.py
│   ├── parsers.py
│   ├── alerts.py
│   ├── specialists.py
│   ├── reports.py
│   ├── family.py
│   ├── gamification.py
│   ├── spotify.py
│   ├── faceage.py
│   ├── posture_runner.py
│   ├── agents/
│   └── tools/
├── frontend/
│   ├── src/
│   │   ├── pages/
│   │   ├── components/
│   │   ├── api.js
│   │   ├── store.js
│   │   └── App.jsx
│   └── package.json
└── ...
```

## Core Features

**Health Modeling**
- Biological age scoring across subsystems
- Mental wellness scoring
- Risk projection and habit simulation
- Workout and nutrition target generation

**Data Ingestion**
- Blood report upload (PDF parsing)
- Cult.fit / body composition scan upload
- Apple Health zip or XML import
- Meal photo or text analysis
- Face age estimation
- Browser-based posture checks

**Coaching & Guidance**
- Coach chat, mental health chat, Future Self chat
- Contextual reminders and specialist recommendations
- Doctor-report generation

## Local Development

**Requirements**
- Python 3.12+
- Node.js 20+
- npm

### 1. Set up the backend

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r backend/requirements.txt
```

### 2. Set up the frontend

```bash
cd frontend
npm install
```

### 3. Configure environment variables

Copy `.env.example` to `.env` at the repository root and fill in the keys you need.

Minimum setup:

```env
ANTHROPIC_API_KEY=
GEMINI_API_KEY=
EIRVIEW_CORS_ORIGINS=http://127.0.0.1:5173,http://localhost:5173
```

Optional integrations:

```env
OPENWEATHERMAP_API_KEY=
USDA_API_KEY=DEMO_KEY
SPOTIFY_CLIENT_ID=
SPOTIFY_CLIENT_SECRET=
SPOTIFY_REDIRECT_URI=http://127.0.0.1:5173/callback
FACEAGE_MODEL_PATH=FaceAge-main/models/faceage_model.onnx
FACE_LANDMARKER_PATH=FaceAge-main/models/face_landmarker.task
SMTP_HOST=
SMTP_PORT=587
SMTP_USER=
SMTP_PASS=
SMTP_FROM_EMAIL=
SMTP_FROM_NAME=EirView Alerts
```

### 4. Run

Backend:

```bash
source .venv/bin/activate
python -m uvicorn backend.main:app --host 127.0.0.1 --port 8000 --reload --reload-dir backend
```

Frontend (in a separate terminal):

```bash
cd frontend
npm run dev -- --host 127.0.0.1
```

- Frontend: http://127.0.0.1:5173
- API docs: http://127.0.0.1:8000/docs

## Notes

**Face Age** — requires local model assets under `FaceAge-main/models/`. That directory is not committed to the repo.

**Posture** — runs entirely in the browser via MediaPipe Tasks Web; readings are stored through the backend.

**Weather / AQI** — falls back to cached/default conditions if `OPENWEATHERMAP_API_KEY` is not set.

**Spotify** — per-user OAuth; the redirect URI in your Spotify developer dashboard must match the value in `.env`.

## Validation

```bash
# From repo root
python3 -m py_compile backend/main.py backend/formulas.py backend/reminder_engine.py backend/activity.py

cd frontend
npm run build
```
