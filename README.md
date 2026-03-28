# EirView

**"Your progress, in full focus."**

Multi-source health intelligence platform that computes biological age, projects health risks, and provides AI-powered coaching. Built for HackMarch 2.0 (AI for Longevity).

## Architecture

```
React + Tailwind          FastAPI + SQLite          Claude 4.6 + Gemini 2.5 Flash
(port 5173)         -->   (port 8000)         -->   (Multi-agent system)
                          |
                          +--> FaceAge ONNX (bio age from face)
                          +--> USDA API (grounded nutrition data)
                          +--> Spine-Watch (live posture detection)
                          +--> Spotify Web API (mood tracking)
                          +--> OpenWeatherMap + AQICN (environment)
```

## Key Features (35)

- **Biological Age**: 4 sub-system formula (cardiovascular, metabolic, musculoskeletal, neurological) + FaceAge + device age comparison
- **6 AI Agents**: Orchestrator, Collector, Mirror, Time Machine, Coach, Mental Health — all with Claude tool-use
- **Multi-Model Routing**: Claude for complex reasoning, Gemini Flash for vision/classification. Database as shared context.
- **USDA-Grounded Meals**: AI identifies food from photos, USDA provides real nutrition, blood-work overlay
- **Risk Projection**: 15-year disease risk curves (diabetes, CVD, metabolic, mental decline)
- **Interactive Simulation**: Habit sliders recalculate bio age in real-time
- **3 Chat Interfaces**: Future Self, Mental Health (PHQ-9), Coach — all SSE streaming
- **Gamification**: Duolingo-style streaks, XP, levels, achievements, leaderboard
- **Family System**: Join via code, auto-derive family health history from member data
- **Smart Reminders**: Data freshness tracking, medical checkup scheduling
- **Emergency Alerts**: Critical value detection, doctor email notification, crisis helplines
- **Specialist Recommendations**: Condition detection -> cardiologist/endocrinologist/psychiatrist + nearby hospitals
- **Spotify Mood Tracking**: Smart flagging (valence trend + cross-signal confirmation)

## How to Build

### Prerequisites
- Python 3.11+
- Node.js 20+
- API keys: Anthropic, Gemini, OpenWeatherMap (optional), Spotify (optional)

### Setup

```bash
# Backend
cd backend
python -m venv venv && source venv/bin/activate
pip install -r requirements.txt
cp .env.example .env  # Fill in API keys

# Frontend
cd frontend
npm install
```

### Run

```bash
# Terminal 1: Backend
cd backend && source venv/bin/activate && uvicorn main:app --port 8000 --reload

# Terminal 2: Frontend
cd frontend && npm run dev

# Terminal 3: Posture (optional)
cd backend && python posture_runner.py
```

Frontend: http://localhost:5173 | Backend docs: http://localhost:8000/docs

## Project Structure

```
Health/
├── backend/
│   ├── main.py                  # FastAPI routes
│   ├── database.py              # SQLite (18 tables)
│   ├── formulas.py              # Deterministic calculations (ZERO AI)
│   ├── ai_router.py             # Claude 4.6 + Gemini 2.5 Flash routing
│   ├── agents/                  # 6 AI agents with tool-use
│   ├── tools/                   # Tool implementations
│   ├── parsers.py               # Blood PDF, Cult.fit, Apple Health XML, USDA meals
│   ├── family.py                # Family groups + auto history
│   ├── specialists.py           # Condition -> specialist mapping
│   ├── gamification.py          # Streaks, XP, achievements
│   ├── faceage.py               # ONNX face age inference
│   └── spotify.py               # Spotify OAuth + mood analysis
│
├── frontend/
│   ├── src/
│   │   ├── App.jsx              # Router + layout
│   │   ├── api.js               # All backend calls + SSE
│   │   ├── store.js             # Zustand state
│   │   ├── pages/               # 11 pages
│   │   └── components/          # 30+ components
│   └── package.json
│
├── codex_prompts/               # Detailed prompts for Codex to generate code
│   ├── 01_BACKEND_CORE.md       # Database, formulas, gamification, family, specialists
│   ├── 02_BACKEND_AI_AND_API.md # AI router, agents, tools, parsers, API routes
│   └── 03_FRONTEND.md           # Complete React frontend with detailed UI specs
│
├── EIRVIEW_MASTER_DOCUMENT.md   # Full documentation (demo script, Q&A, formulas)
├── IPHONE_APP_PROMPT.md         # iOS companion app spec
└── EIRVIEW_IOS_BACKEND_CONTRACT.md  # Mobile API contract
```

## Team Assignment

| Person | Responsibility | Codex Prompt |
|--------|---------------|-------------|
| Person 1 | Backend core: DB, formulas, gamification, family, specialists, alerts | `01_BACKEND_CORE.md` |
| Person 2 | Backend AI: agents, tools, API routes, parsers | `02_BACKEND_AI_AND_API.md` |
| Person 3 | Frontend: all pages and components | `03_FRONTEND.md` |

### How to use the prompts
1. Open Codex (or Claude Code)
2. Copy the relevant prompt file
3. Paste as the task — it has all the context needed for one-shot generation
4. Review the output, fix any integration issues

## Key Design Decisions

1. **Deterministic formulas, not AI**: All health calculations (bio age, risk, wellness score) are deterministic code in `formulas.py`. AI only does parsing and narrative generation. This means results are reproducible and auditable.

2. **Multi-model routing**: Claude handles complex reasoning (mental health, coaching). Gemini handles fast vision tasks (meal photos, screenshots). Database is shared context — models never see each other's conversations.

3. **USDA-grounded nutrition**: We don't ask AI to guess calories. Vision AI identifies food, USDA database provides lab-tested nutrition. Every number has a USDA food ID.

4. **Family history from data, not checkboxes**: When a family member uploads blood work showing prediabetes, the system automatically updates other members' risk projections. No manual "family history" forms.

5. **Smart Spotify flagging**: We don't assume sad music = sad person. We only flag when listening patterns shift from the user's personal baseline AND at least one biological signal (sleep, HRV, steps) confirms it.

## Pre-loaded Demo Users

| User | Profile | Highlights |
|------|---------|-----------|
| zahoor | 19M, real blood work + Apple Health data | LDL 121, VitD 15 (deficient), bio age ~17.2 |
| riya | 22F, sample data | Glucose 108 (prediabetic), PHQ-9 12, poor sleep |
| arjun | 24M, healthy athlete | All values optimal, VO2max 52, bio age ~21.2 |

## Environment Variables

```
ANTHROPIC_API_KEY=sk-ant-...
GEMINI_API_KEY=...
OPENWEATHERMAP_API_KEY=...     # Optional, falls back to hardcoded
USDA_API_KEY=DEMO_KEY          # Free, no signup needed
SPOTIFY_CLIENT_ID=...          # Optional
SPOTIFY_CLIENT_SECRET=...
```
