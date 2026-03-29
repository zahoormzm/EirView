# EirView

EirView is a full-stack health intelligence platform that combines deterministic health calculations, multi-source data ingestion, and AI-assisted coaching. The application is built with a React frontend, a FastAPI backend, SQLite storage, and a small agent/tool layer for guided reasoning tasks.

## What The Project Does

- Computes biological age across cardiovascular, metabolic, musculoskeletal, and neurological subsystems
- Tracks health data from blood reports, body composition scans, Apple Health exports, meals, posture checks, and manual entries
- Projects medium-term health risks and supports what-if scenario simulation
- Provides contextual coaching for activity, nutrition, future-self reflection, and mental health support
- Surfaces reminders, alerts, specialist recommendations, and data freshness timelines

## Stack

### Frontend

- React 19
- Vite
- Tailwind CSS
- Zustand
- Recharts

### Backend

- FastAPI
- SQLite with `aiosqlite`
- Deterministic health and risk logic in Python
- Anthropic and Gemini integrations for selected parsing and coaching flows

### Supporting Services

- Spotify Web API
- OpenWeatherMap
- USDA food data
- ONNX Runtime for face age inference
- MediaPipe Tasks for browser posture analysis

## Repository Layout

```text
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

## Core Product Areas

### Health Modeling

- Biological age scoring
- Mental wellness scoring
- Risk projection
- Habit simulation
- Workout target generation
- Nutrition target generation

### Data Ingestion

- Blood report upload
- Cult.fit/body composition scan upload
- Apple Health zip or XML import
- Meal photo or meal text analysis
- Face age upload
- Browser-based posture checks

### Coaching And Guidance

- Coach chat
- Mental health chat
- Future Self chat
- Contextual reminders
- Specialist recommendations
- Doctor-report generation

## Local Development

### Requirements

- Python 3.12+
- Node.js 20+
- npm

### 1. Create And Activate A Virtual Environment

```bash
cd /Users/zahoormashahir/Documents/Projects/Health
python3 -m venv .venv
source .venv/bin/activate
```

### 2. Install Backend Dependencies

```bash
pip install -r backend/requirements.txt
```

### 3. Install Frontend Dependencies

```bash
cd /Users/zahoormashahir/Documents/Projects/Health/frontend
npm install
```

### 4. Configure Environment Variables

Copy `.env.example` to `.env` at the repository root and populate the keys you need.

Minimum useful setup:

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

## Running The Application

### Backend

```bash
cd /Users/zahoormashahir/Documents/Projects/Health
source .venv/bin/activate
python -m uvicorn backend.main:app --host 127.0.0.1 --port 8000 --reload --reload-dir backend
```

### Frontend

```bash
cd /Users/zahoormashahir/Documents/Projects/Health/frontend
npm run dev -- --host 127.0.0.1
```

### URLs

- Frontend: [http://127.0.0.1:5173](http://127.0.0.1:5173)
- API docs: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)

## Notes On Optional Features

### Face Age

Face age inference requires local model assets under `FaceAge-main/models/`. That directory is treated as a local runtime dependency and is intentionally not committed to the repository.

### Posture

The current posture feature runs in the browser using MediaPipe Tasks Web and stores readings through the backend.

### Weather And AQI

Weather-driven suggestions fall back to cached/default conditions if `OPENWEATHERMAP_API_KEY` is not configured.

### Spotify

Spotify integration is per EirView user and requires the OAuth redirect URI in Spotify developer settings to match the value in `.env`.

## Validation

Useful local checks:

```bash
cd /Users/zahoormashahir/Documents/Projects/Health
python3 -m py_compile backend/main.py backend/formulas.py backend/reminder_engine.py backend/activity.py
cd frontend
npm run build
```

## Project Status

This repository contains a working application with active product features and several optional integrations. The backend and frontend are designed to run locally together, with SQLite as the default development datastore.
