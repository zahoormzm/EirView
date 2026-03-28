# Codex Task: EirView Backend Core

## Overview

Generate the complete backend core for **EirView**, a health intelligence platform. Create **9 Python files** plus an `__init__.py` inside the `backend/` directory. The stack is **FastAPI + SQLite (via aiosqlite) + Pydantic**, targeting **Python 3.11+**.

All files must:
- Have complete type hints on every function signature
- Include docstrings on every function and class
- Use `from __future__ import annotations` at the top
- Import from sibling modules correctly (e.g., `from backend.formulas import calculate_bio_age`)
- Be production-ready with proper error handling

## File Dependency Graph

```
formulas.py          (pure, no imports from backend)
health_state.py      (pure Pydantic models, no DB)
database.py          (imports health_state)
gamification.py      (imports database)
family.py            (imports database, formulas)
specialists.py       (pure, no DB — takes dict)
reminder_engine.py   (imports database)
alerts.py            (imports database)
activity.py          (imports database, formulas)
```

---

## File 1: `backend/__init__.py`

```python
"""EirView backend core package."""
```

---

## File 2: `backend/health_state.py` — Pydantic Models

Define the following Pydantic `BaseModel` classes with `from pydantic import BaseModel, Field`. All fields should be `Optional` with sensible defaults (`None` for measurements, `0` for counters).

### Class: `HealthProfile`

This is the main model representing a user's complete health state. Fields must match the `profiles` table columns exactly:

**Blood work fields:**
- `ldl: float | None = None`
- `hdl: float | None = None`
- `triglycerides: float | None = None`
- `total_cholesterol: float | None = None`
- `vitamin_d: float | None = None`
- `b12: float | None = None`
- `tsh: float | None = None`
- `ferritin: float | None = None`
- `fasting_glucose: float | None = None`
- `hba1c: float | None = None`
- `hemoglobin: float | None = None`
- `creatinine: float | None = None`
- `sgpt_alt: float | None = None`
- `sgot_ast: float | None = None`

**Body composition fields:**
- `weight_kg: float | None = None`
- `bmi: float | None = None`
- `bmr: float | None = None`
- `body_fat_pct: float | None = None`
- `visceral_fat_kg: float | None = None`
- `muscle_mass_kg: float | None = None`
- `body_water_pct: float | None = None`
- `protein_kg: float | None = None`
- `bone_mass_kg: float | None = None`
- `body_age_device: int | None = None`

**HealthKit / Apple Health fields:**
- `resting_hr: float | None = None`
- `hrv_ms: float | None = None`
- `steps_today: int | None = None`
- `steps_avg_7d: int | None = None`
- `active_energy_kcal: float | None = None`
- `exercise_min: int | None = None`
- `sleep_hours: float | None = None`
- `sleep_deep_pct: float | None = None`
- `sleep_rem_pct: float | None = None`
- `vo2max: float | None = None`
- `respiratory_rate: float | None = None`
- `walking_asymmetry_pct: float | None = None`
- `flights_climbed: int | None = None`
- `blood_oxygen_pct: float | None = None`
- `blood_pressure_systolic: float | None = None`
- `blood_pressure_diastolic: float | None = None`

**Face Age:**
- `face_age: float | None = None`

**Posture:**
- `posture_score_pct: float | None = None`

**Environment:**
- `temperature_c: float | None = None`
- `humidity_pct: float | None = None`
- `aqi: int | None = None`
- `uv_index: float | None = None`

**Mental:**
- `phq9_score: int | None = None`
- `stress_level: int | None = None`
- `screen_time_hours: float | None = None`

**Family history (booleans):**
- `family_diabetes: bool = False`
- `family_heart: bool = False`
- `family_hypertension: bool = False`
- `family_mental: bool = False`

**Lifestyle:**
- `exercise_hours_week: float | None = None`
- `sleep_target: float | None = None`
- `smoking: str = "never"`
- `diet_quality: str = "average"`

**User metadata (carried through for formulas):**
- `age: int | None = None`
- `sex: str | None = None`
- `height_cm: float | None = None`

### Additional Models

```python
class UserCreate(BaseModel):
    """Request body for creating a user."""
    id: str
    name: str
    age: int | None = None
    sex: str | None = None
    height_cm: float | None = None

class MealEntry(BaseModel):
    """A single meal log entry."""
    description: str | None = None
    photo_path: str | None = None
    calories: float | None = None
    protein_g: float | None = None
    carbs_g: float | None = None
    fat_g: float | None = None
    saturated_fat_g: float | None = None
    fiber_g: float | None = None
    vitamin_d_ug: float | None = None
    b12_ug: float | None = None
    health_score: float | None = None
    ai_notes: str | None = None

class WorkoutEntry(BaseModel):
    """A single workout log entry."""
    type: str
    duration_min: int | None = None
    calories: float | None = None
    source: str = "manual"
    date: str  # ISO date string YYYY-MM-DD

class WaterEntry(BaseModel):
    """A water intake log entry."""
    amount_ml: int

class PostureEntry(BaseModel):
    """A posture reading."""
    score_pct: float
    avg_angle: float | None = None
    is_slouching: bool = False

class SpotifyEntry(BaseModel):
    """Spotify listening analysis entry."""
    avg_valence: float | None = None
    avg_energy: float | None = None
    avg_danceability: float | None = None
    track_count: int | None = None
    baseline_valence: float | None = None

class GamificationState(BaseModel):
    """Current gamification state for a user."""
    current_streak: int = 0
    longest_streak: int = 0
    total_xp: int = 0
    level: int = 1
    level_name: str = "Health Rookie"
    today_actions: list[str] = []
    achievements: list[str] = []
    active_challenge: dict | None = None

class FamilyCreate(BaseModel):
    """Request body for creating a family group."""
    name: str

class FamilyJoin(BaseModel):
    """Request body for joining a family group."""
    join_code: str
    relationship: str
    privacy_level: str = "summary"
```

---

## File 3: `backend/database.py` — SQLite Setup + CRUD

Use `aiosqlite` for all database operations. Structure:

### Database Path

```python
import os
DB_PATH = os.environ.get("EIRVIEW_DB_PATH", "eirview.db")
```

### Schema Creation

Write a function `async def init_db() -> None` that creates all 18 tables using `CREATE TABLE IF NOT EXISTS`. Use the exact schema below:

```sql
-- Users table
CREATE TABLE IF NOT EXISTS users (
    id TEXT PRIMARY KEY,
    name TEXT NOT NULL,
    age INTEGER,
    sex TEXT,
    height_cm REAL,
    family_id TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Health profiles
CREATE TABLE IF NOT EXISTS profiles (
    user_id TEXT PRIMARY KEY REFERENCES users(id),
    -- Blood work
    ldl REAL, hdl REAL, triglycerides REAL, total_cholesterol REAL,
    vitamin_d REAL, b12 REAL, tsh REAL, ferritin REAL,
    fasting_glucose REAL, hba1c REAL, hemoglobin REAL,
    creatinine REAL, sgpt_alt REAL, sgot_ast REAL,
    -- Body composition
    weight_kg REAL, bmi REAL, bmr REAL,
    body_fat_pct REAL, visceral_fat_kg REAL,
    muscle_mass_kg REAL, body_water_pct REAL,
    protein_kg REAL, bone_mass_kg REAL, body_age_device INTEGER,
    -- HealthKit / Apple Health
    resting_hr REAL, hrv_ms REAL,
    steps_today INTEGER, steps_avg_7d INTEGER,
    active_energy_kcal REAL, exercise_min INTEGER,
    sleep_hours REAL, sleep_deep_pct REAL, sleep_rem_pct REAL,
    vo2max REAL, respiratory_rate REAL,
    walking_asymmetry_pct REAL, flights_climbed INTEGER,
    blood_oxygen_pct REAL,
    blood_pressure_systolic REAL, blood_pressure_diastolic REAL,
    -- Face Age
    face_age REAL,
    -- Posture
    posture_score_pct REAL,
    -- Environment
    temperature_c REAL, humidity_pct REAL,
    aqi INTEGER, uv_index REAL,
    -- Mental
    phq9_score INTEGER, stress_level INTEGER,
    screen_time_hours REAL,
    -- Family history
    family_diabetes BOOLEAN DEFAULT 0, family_heart BOOLEAN DEFAULT 0,
    family_hypertension BOOLEAN DEFAULT 0, family_mental BOOLEAN DEFAULT 0,
    -- Lifestyle
    exercise_hours_week REAL, sleep_target REAL,
    smoking TEXT DEFAULT 'never',
    diet_quality TEXT DEFAULT 'average',
    -- Medical
    last_blood_report_date DATE,
    last_vitd_test_date DATE,
    last_glucose_test_date DATE,
    last_general_checkup_date DATE,
    doctor_name TEXT, doctor_email TEXT, doctor_phone TEXT,
    emergency_contact_name TEXT, emergency_contact_phone TEXT,
    -- Computed
    bio_age_overall REAL,
    bio_age_cardiovascular REAL, bio_age_metabolic REAL,
    bio_age_musculoskeletal REAL, bio_age_neurological REAL,
    mental_wellness_score REAL,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Agent logs
CREATE TABLE IF NOT EXISTS agent_logs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id TEXT REFERENCES users(id),
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    agent_name TEXT NOT NULL,
    action TEXT,
    tool_name TEXT,
    tool_input TEXT,
    tool_output TEXT,
    prompt TEXT,
    response TEXT,
    tokens_in INTEGER,
    tokens_out INTEGER,
    latency_ms INTEGER,
    model TEXT DEFAULT 'claude-sonnet-4-6'
);

-- Meals
CREATE TABLE IF NOT EXISTS meals (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id TEXT REFERENCES users(id),
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    description TEXT,
    photo_path TEXT,
    calories REAL, protein_g REAL, carbs_g REAL, fat_g REAL,
    saturated_fat_g REAL, fiber_g REAL,
    vitamin_d_ug REAL, b12_ug REAL,
    health_score REAL,
    ai_notes TEXT
);

-- Water log
CREATE TABLE IF NOT EXISTS water_log (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id TEXT REFERENCES users(id),
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    amount_ml INTEGER
);

-- Posture history
CREATE TABLE IF NOT EXISTS posture_history (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id TEXT REFERENCES users(id),
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    score_pct REAL,
    avg_angle REAL,
    is_slouching BOOLEAN
);

-- Risk projections
CREATE TABLE IF NOT EXISTS risk_projections (
    user_id TEXT REFERENCES users(id),
    year INTEGER,
    diabetes_risk REAL,
    cvd_risk REAL,
    metabolic_risk REAL,
    mental_decline_risk REAL,
    PRIMARY KEY (user_id, year)
);

-- Spotify history
CREATE TABLE IF NOT EXISTS spotify_history (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id TEXT REFERENCES users(id),
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    avg_valence REAL,
    avg_energy REAL,
    avg_danceability REAL,
    track_count INTEGER,
    baseline_valence REAL,
    flagged BOOLEAN DEFAULT 0,
    flag_reason TEXT
);

-- Streaks
CREATE TABLE IF NOT EXISTS streaks (
    user_id TEXT PRIMARY KEY REFERENCES users(id),
    current_streak INTEGER DEFAULT 0,
    longest_streak INTEGER DEFAULT 0,
    last_streak_date DATE,
    total_xp INTEGER DEFAULT 0,
    level INTEGER DEFAULT 1
);

-- Daily actions
CREATE TABLE IF NOT EXISTS daily_actions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id TEXT REFERENCES users(id),
    date DATE NOT NULL,
    action TEXT NOT NULL,
    xp_earned INTEGER,
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(user_id, date, action)
);

-- Achievements
CREATE TABLE IF NOT EXISTS achievements (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id TEXT REFERENCES users(id),
    badge_id TEXT NOT NULL,
    earned_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(user_id, badge_id)
);

-- Weekly challenges
CREATE TABLE IF NOT EXISTS weekly_challenges (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id TEXT REFERENCES users(id),
    week_start DATE NOT NULL,
    challenge_id TEXT NOT NULL,
    progress INTEGER DEFAULT 0,
    target INTEGER NOT NULL,
    completed BOOLEAN DEFAULT 0
);

-- Families
CREATE TABLE IF NOT EXISTS families (
    id TEXT PRIMARY KEY,
    name TEXT NOT NULL,
    join_code TEXT UNIQUE NOT NULL,
    created_by TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Family members
CREATE TABLE IF NOT EXISTS family_members (
    family_id TEXT REFERENCES families(id),
    user_id TEXT REFERENCES users(id),
    relationship TEXT NOT NULL,
    role TEXT DEFAULT 'member',
    privacy_level TEXT DEFAULT 'summary',
    joined_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (family_id, user_id)
);

-- Family health flags
CREATE TABLE IF NOT EXISTS family_health_flags (
    family_id TEXT REFERENCES families(id),
    condition TEXT NOT NULL,
    source_user_id TEXT,
    evidence TEXT,
    severity TEXT,
    detected_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (family_id, condition, source_user_id)
);

-- USDA foods cache
CREATE TABLE IF NOT EXISTS usda_foods (
    fdc_id INTEGER PRIMARY KEY,
    description TEXT NOT NULL,
    calories_per_100g REAL,
    protein_per_100g REAL,
    fat_per_100g REAL,
    carbs_per_100g REAL,
    sat_fat_per_100g REAL,
    fiber_per_100g REAL,
    vitamin_d_ug_per_100g REAL,
    b12_ug_per_100g REAL,
    iron_mg_per_100g REAL,
    cached_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Specialist referrals
CREATE TABLE IF NOT EXISTS specialist_referrals (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id TEXT REFERENCES users(id),
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    specialist_type TEXT NOT NULL,
    trigger_metric TEXT NOT NULL,
    trigger_value REAL,
    trigger_threshold REAL,
    reason TEXT,
    recommended_hospitals TEXT,
    acknowledged BOOLEAN DEFAULT 0,
    appointment_scheduled BOOLEAN DEFAULT 0
);

-- Data sources (freshness tracking)
CREATE TABLE IF NOT EXISTS data_sources (
    user_id TEXT REFERENCES users(id),
    source TEXT NOT NULL,
    last_synced_at TIMESTAMP,
    refresh_interval_days INTEGER,
    reminder_sent_at TIMESTAMP,
    PRIMARY KEY (user_id, source)
);

-- Alerts history
CREATE TABLE IF NOT EXISTS alerts (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id TEXT REFERENCES users(id),
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    metric TEXT NOT NULL,
    value REAL NOT NULL,
    threshold REAL NOT NULL,
    severity TEXT NOT NULL,
    user_notified BOOLEAN DEFAULT 1,
    doctor_notified BOOLEAN DEFAULT 0,
    doctor_email_sent_at TIMESTAMP,
    user_approved_doctor_alert BOOLEAN
);

-- Workouts
CREATE TABLE IF NOT EXISTS workouts (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id TEXT REFERENCES users(id),
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    type TEXT NOT NULL,
    duration_min INTEGER,
    calories REAL,
    source TEXT DEFAULT 'manual',
    date DATE NOT NULL,
    cv_impact REAL,
    msk_impact REAL,
    met_impact REAL,
    neuro_impact REAL
);
```

### CRUD Functions

Implement these async functions:

```python
async def get_db() -> aiosqlite.Connection:
    """Get a database connection with row_factory set to aiosqlite.Row."""

async def create_user(user_id: str, name: str, age: int | None, sex: str | None, height_cm: float | None) -> dict:
    """Insert a new user. Return the created user dict."""

async def get_user(user_id: str) -> dict | None:
    """Fetch a user by ID. Return None if not found."""

async def get_all_users() -> list[dict]:
    """Fetch all users."""

async def upsert_profile(user_id: str, data: dict) -> dict:
    """Insert or update a health profile. Use INSERT OR REPLACE.
    Before saving, merge with existing data so partial updates don't erase fields.
    Return the full updated profile."""

async def get_profile(user_id: str) -> dict | None:
    """Fetch a user's health profile as a dict. Include user age/sex/height from users table."""

async def log_meal(user_id: str, meal: dict) -> dict:
    """Insert a meal entry. Return the created meal with its ID."""

async def get_meals(user_id: str, limit: int = 20) -> list[dict]:
    """Fetch recent meals for a user, ordered by timestamp DESC."""

async def log_water(user_id: str, amount_ml: int) -> dict:
    """Insert a water log entry."""

async def get_water_today(user_id: str) -> int:
    """Sum of water intake today in ml."""

async def log_posture(user_id: str, entry: dict) -> dict:
    """Insert a posture reading."""

async def get_posture_history(user_id: str, limit: int = 50) -> list[dict]:
    """Fetch recent posture readings."""

async def save_risk_projections(user_id: str, projections: list[dict]) -> None:
    """Save risk projection rows (replace existing for user)."""

async def get_risk_projections(user_id: str) -> list[dict]:
    """Fetch risk projections for a user."""

async def log_agent_action(user_id: str, agent_name: str, action: str, **kwargs) -> None:
    """Insert an agent log entry. kwargs may include tool_name, tool_input, tool_output, prompt, response, tokens_in, tokens_out, latency_ms, model."""

async def log_spotify(user_id: str, entry: dict) -> dict:
    """Insert a Spotify analysis entry."""
```

### Seed Data Function

```python
async def seed_data() -> None:
    """Insert seed data for 3 users if they don't already exist.
    Call this at the end of init_db()."""
```

Seed the following data:

**User "zahoor":**
```python
# users table
{"id": "zahoor", "name": "Zahoor Mashahir", "age": 19, "sex": "male", "height_cm": 178}

# profiles table — all fields
{
    "user_id": "zahoor",
    # Blood work
    "ldl": 121, "hdl": 48, "total_cholesterol": 198, "vitamin_d": 15, "b12": 310,
    "tsh": 2.8, "hemoglobin": 14.2, "fasting_glucose": 85, "hba1c": 5.1,
    "creatinine": 0.9, "sgpt_alt": 28, "sgot_ast": 22, "ferritin": 65,
    # Body composition
    "weight_kg": 66.9, "bmi": 21.1, "bmr": 1575, "body_fat_pct": 18.5,
    "visceral_fat_kg": 1.2, "muscle_mass_kg": 29.1, "body_water_pct": 58.2,
    "protein_kg": 10.1, "bone_mass_kg": 2.8, "body_age_device": 15,
    # HealthKit
    "resting_hr": 67, "hrv_ms": 42, "steps_today": 8234, "steps_avg_7d": 7500,
    "active_energy_kcal": 420, "exercise_min": 35, "sleep_hours": 6.5,
    "sleep_deep_pct": 15, "sleep_rem_pct": 20, "vo2max": 42.5,
    "respiratory_rate": 15.2, "walking_asymmetry_pct": 3.2, "flights_climbed": 4,
    "blood_oxygen_pct": 97,
    # Face
    "face_age": 21.3,
    # Posture
    "posture_score_pct": 72,
    # Mental
    "phq9_score": 6, "stress_level": 5, "screen_time_hours": 8,
    # Lifestyle
    "exercise_hours_week": 4, "sleep_target": 8, "smoking": "never", "diet_quality": "average",
    # Family history
    "family_diabetes": 0, "family_heart": 0, "family_hypertension": 0,
}

# streaks table
{"user_id": "zahoor", "current_streak": 3, "longest_streak": 3, "total_xp": 250, "level": 2}
```

**User "riya":**
```python
# users table
{"id": "riya", "name": "Riya Sharma", "age": 22, "sex": "female", "height_cm": 162}

# profiles table
{
    "user_id": "riya",
    "ldl": 95, "hdl": 55, "vitamin_d": 12, "b12": 245, "fasting_glucose": 108,
    "hba1c": 5.8, "hemoglobin": 11.5, "tsh": 4.8,
    "weight_kg": 58, "bmi": 22.1, "body_fat_pct": 28, "muscle_mass_kg": 20.5,
    "body_age_device": 25,
    "resting_hr": 78, "hrv_ms": 28, "steps_today": 3200, "steps_avg_7d": 4100,
    "exercise_min": 8, "sleep_hours": 5.5, "sleep_deep_pct": 10, "sleep_rem_pct": 15,
    "vo2max": 32,
    "phq9_score": 12, "stress_level": 7, "screen_time_hours": 11,
    "family_diabetes": 1,
}

# streaks table
{"user_id": "riya", "current_streak": 0, "longest_streak": 0, "total_xp": 50, "level": 1}
```

**User "arjun":**
```python
# users table
{"id": "arjun", "name": "Arjun Patel", "age": 24, "sex": "male", "height_cm": 180}

# profiles table
{
    "user_id": "arjun",
    "ldl": 85, "hdl": 65, "vitamin_d": 38, "b12": 520, "fasting_glucose": 82,
    "hba1c": 4.9, "hemoglobin": 15.5,
    "weight_kg": 75, "bmi": 23.1, "body_fat_pct": 12, "muscle_mass_kg": 38,
    "body_age_device": 20,
    "resting_hr": 55, "hrv_ms": 65, "steps_today": 12500, "steps_avg_7d": 11000,
    "exercise_min": 65, "sleep_hours": 7.8, "sleep_deep_pct": 22, "sleep_rem_pct": 25,
    "vo2max": 52,
    "phq9_score": 3, "stress_level": 3, "screen_time_hours": 4,
    "exercise_hours_week": 8, "diet_quality": "excellent",
}

# streaks table
{"user_id": "arjun", "current_streak": 12, "longest_streak": 12, "total_xp": 1200, "level": 5}
```

Also seed `data_sources` for each user with these sources and their default refresh intervals:
- `healthkit`: 2 days
- `meal`: 1 day
- `water`: 1 day
- `posture`: 7 days
- `faceage`: 30 days
- `blood_report`: 90 days
- `mental_checkin`: 7 days

Set `last_synced_at` to various dates in the past to make reminders interesting (e.g., healthkit synced 1 day ago, blood_report synced 100 days ago for zahoor, etc.).

---

## File 4: `backend/formulas.py` — Deterministic Health Formulas

This file is **pure Python** with zero imports from the backend package. It takes `dict` inputs (profile data) and returns computed results. **No AI, no database, no async.** Every function is synchronous.

### `calculate_bio_age(profile: dict) -> dict`

Main entry point. Returns overall + 4 sub-system bio ages.

```python
def calculate_bio_age(profile: dict) -> dict:
    """Calculate biological age from health profile data.

    Returns dict with keys: overall, cardiovascular, metabolic,
    musculoskeletal, neurological, deltas.
    """
    chrono = profile.get("age", 25)
    cv = cardiovascular_delta(profile)    # clamped to [-8, +8]
    met = metabolic_delta(profile)        # clamped to [-8, +8]
    msk = musculoskeletal_delta(profile)  # clamped to [-6, +6]
    neuro = neurological_delta(profile)   # clamped to [-6, +6]

    overall = chrono + (0.30 * cv + 0.25 * met + 0.20 * msk + 0.25 * neuro)

    return {
        "overall": round(overall, 1),
        "cardiovascular": round(chrono + cv, 1),
        "metabolic": round(chrono + met, 1),
        "musculoskeletal": round(chrono + msk, 1),
        "neurological": round(chrono + neuro, 1),
        "deltas": {
            "cv": round(cv, 2),
            "met": round(met, 2),
            "msk": round(msk, 2),
            "neuro": round(neuro, 2),
        }
    }
```

### `cardiovascular_delta(profile: dict) -> float`

Sum the following contributions, then clamp to [-8, +8]:

| Factor | Condition | Score |
|--------|-----------|-------|
| HDL | <40 | +1.5 |
| HDL | 40-59 | 0 |
| HDL | >=60 | -1.5 |
| LDL | <100 | -1.0 |
| LDL | 100-129 | 0 |
| LDL | 130-159 | +1.0 |
| LDL | >=160 | +2.0 |
| Triglycerides | <150 | 0 |
| Triglycerides | 150-199 | +0.5 |
| Triglycerides | >=200 | +1.5 |
| Resting HR | <60 | -1.0 |
| Resting HR | 60-72 | 0 |
| Resting HR | 73-84 | +0.5 |
| Resting HR | >=85 | +1.5 |
| HRV (SDNN ms) | >=50 | -1.0 |
| HRV | 30-49 | 0 |
| HRV | <30 | +1.5 |
| VO2max | >=45 | -1.5 |
| VO2max | 35-44 | -0.5 |
| VO2max | 25-34 | +0.5 |
| VO2max | <25 | +1.5 |
| Steps avg 7d | >=10000 | -1.0 |
| Steps avg 7d | 7500-9999 | -0.5 |
| Steps avg 7d | 5000-7499 | 0 |
| Steps avg 7d | <5000 | +1.0 |
| Exercise min/day | >=45 | -1.0 |
| Exercise min/day | 30-44 | -0.5 |
| Exercise min/day | 15-29 | 0 |
| Exercise min/day | <15 | +1.0 |
| BP systolic | <120 | -0.5 |
| BP systolic | 120-129 | 0 |
| BP systolic | 130-139 | +1.0 |
| BP systolic | >=140 | +2.0 |

For missing values (None), skip that factor (contribute 0). Use `.get()` with fallback to None, then check `if value is not None`.

### `metabolic_delta(profile: dict) -> float`

Sum the following, clamp to [-8, +8]:

| Factor | Condition | Score |
|--------|-----------|-------|
| BMI | 18.5-22.9 | -0.5 |
| BMI | 23-24.9 | 0 |
| BMI | 25-29.9 | +1.0 |
| BMI | >=30 | +2.0 |
| BMI | <18.5 | +0.5 |
| Visceral fat | <1kg | -0.5 |
| Visceral fat | 1-2kg | 0 |
| Visceral fat | >2kg | +1.5 |
| Fasting glucose | <85 | -0.5 |
| Fasting glucose | 85-99 | 0 |
| Fasting glucose | 100-125 | +1.5 |
| Fasting glucose | >=126 | +3.0 |
| HbA1c | <5.4 | -0.5 |
| HbA1c | 5.4-5.6 | 0 |
| HbA1c | 5.7-6.4 | +1.5 |
| HbA1c | >=6.5 | +3.0 |
| Vitamin D | >=30 | -0.5 |
| Vitamin D | 20-29 | 0 |
| Vitamin D | <20 | +1.5 |
| B12 | >=300 | -0.5 |
| B12 | 200-299 | 0 |
| B12 | <200 | +1.0 |
| TSH | 0.5-4.0 | 0 |
| TSH | outside range | +1.0 |
| BMR | >5% above Mifflin expected | -0.5 |
| BMR | >5% below Mifflin expected | +0.5 |
| BMR | within 5% | 0 |

**Mifflin-St Jeor formula** for expected BMR:
- Male: `10 * weight_kg + 6.25 * height_cm - 5 * age + 5`
- Female: `10 * weight_kg + 6.25 * height_cm - 5 * age - 161`
- Only calculate if weight, height, age, and sex are all available.

### `musculoskeletal_delta(profile: dict) -> float`

Sum the following, clamp to [-6, +6]:

| Factor | Condition | Score |
|--------|-----------|-------|
| Muscle ratio (male) | >=0.40 | -1.0 |
| Muscle ratio (male) | 0.35-0.39 | 0 |
| Muscle ratio (male) | <0.35 | +1.5 |
| Muscle ratio (female) | >=0.32 | -1.0 |
| Muscle ratio (female) | 0.28-0.31 | 0 |
| Muscle ratio (female) | <0.28 | +1.5 |
| Bone mass (male) | >=3.0kg | -0.5 |
| Bone mass (male) | <2.5kg | +1.0 |
| Bone mass (male) | 2.5-2.99 | 0 |
| Bone mass (female) | >=2.5kg | -0.5 |
| Bone mass (female) | <2.0kg | +1.0 |
| Bone mass (female) | 2.0-2.49 | 0 |
| Posture score | >=80% | -1.0 |
| Posture score | 60-79% | 0 |
| Posture score | <60% | +1.5 |
| Walking asymmetry | <3% | -0.5 |
| Walking asymmetry | 3-5% | 0 |
| Walking asymmetry | >5% | +1.0 |

`muscle_ratio = muscle_mass_kg / weight_kg` (only if both present)

### `neurological_delta(profile: dict) -> float`

Sum the following, clamp to [-6, +6]:

| Factor | Condition | Score |
|--------|-----------|-------|
| Sleep hours | 7-9 | -1.0 |
| Sleep hours | 6-6.9 | 0 |
| Sleep hours | <6 | +1.5 |
| Sleep hours | >9 | +0.5 |
| Sleep deep % | >=20% | -0.5 |
| Sleep deep % | 13-19% | 0 |
| Sleep deep % | <13% | +1.0 |
| PHQ9 | 0-4 | -0.5 |
| PHQ9 | 5-9 | 0 |
| PHQ9 | 10-14 | +1.0 |
| PHQ9 | 15-19 | +2.0 |
| PHQ9 | >=20 | +3.0 |
| Stress (1-10) | 1-3 | -0.5 |
| Stress | 4-6 | 0 |
| Stress | 7-8 | +1.0 |
| Stress | 9-10 | +2.0 |
| Screen time | <4h | -0.5 |
| Screen time | 4-8h | 0 |
| Screen time | 8-12h | +0.5 |
| Screen time | >12h | +1.0 |

### `project_risk(profile: dict, years: int = 15) -> list[dict]`

Project diabetes, CVD, metabolic syndrome, and mental decline risk over N years.

```python
def project_risk(profile: dict, years: int = 15) -> list[dict]:
    """Project health risks over future years using biomarker-based multipliers.

    Uses compound probability: P(event in N years) = 1 - (1 - annual_rate)^N
    Returns list of dicts with year, diabetes_risk, cvd_risk, metabolic_risk, mental_decline_risk.
    """
    # Base annual risk rates (for healthy young adult)
    diabetes_base = 0.002   # 0.2% per year
    cvd_base = 0.001        # 0.1% per year
    metabolic_base = 0.002  # 0.2% per year
    mental_base = 0.003     # 0.3% per year

    # --- Diabetes multiplier ---
    diabetes_mult = 1.0
    if profile.get('fasting_glucose', 0) > 100: diabetes_mult *= 2.5
    if profile.get('hba1c', 0) > 5.7: diabetes_mult *= 2.0
    if profile.get('bmi', 0) > 25: diabetes_mult *= 1.5
    if profile.get('family_diabetes'): diabetes_mult *= 2.0
    if profile.get('exercise_hours_week', 0) < 2.5: diabetes_mult *= 1.3

    # --- CVD multiplier ---
    cvd_mult = 1.0
    if profile.get('ldl', 0) > 130: cvd_mult *= 1.8
    if profile.get('blood_pressure_systolic', 0) > 130: cvd_mult *= 1.5
    if profile.get('hdl', 999) < 40: cvd_mult *= 1.5
    if profile.get('smoking') == 'current': cvd_mult *= 2.5
    if profile.get('family_heart'): cvd_mult *= 1.8

    # --- Metabolic multiplier ---
    metabolic_mult = 1.0
    if profile.get('bmi', 0) > 25: metabolic_mult *= 1.5
    if profile.get('visceral_fat_kg', 0) > 2: metabolic_mult *= 1.5
    if profile.get('triglycerides', 0) > 150: metabolic_mult *= 1.3

    # --- Mental decline multiplier ---
    mental_mult = 1.0
    if profile.get('phq9_score', 0) > 10: mental_mult *= 2.0
    if profile.get('sleep_hours', 8) < 6: mental_mult *= 1.5
    if profile.get('stress_level', 0) > 7: mental_mult *= 1.3
    if profile.get('vitamin_d', 30) < 20: mental_mult *= 1.3
    if profile.get('family_mental'): mental_mult *= 1.5

    results = []
    for year in range(1, years + 1):
        results.append({
            "year": year,
            "diabetes_risk": round(min(1 - (1 - diabetes_base * diabetes_mult) ** year, 0.95), 4),
            "cvd_risk": round(min(1 - (1 - cvd_base * cvd_mult) ** year, 0.95), 4),
            "metabolic_risk": round(min(1 - (1 - metabolic_base * metabolic_mult) ** year, 0.95), 4),
            "mental_decline_risk": round(min(1 - (1 - mental_base * mental_mult) ** year, 0.95), 4),
        })
    return results
```

### `mental_wellness_score(profile: dict) -> dict`

Score starts at 100, subtract penalties. Returns `{"score": float, "breakdown": dict}`.

```python
def mental_wellness_score(profile: dict) -> dict:
    """Calculate mental wellness score (0-100) with detailed breakdown.

    Starts at 100 and subtracts penalties for poor sleep, high stress,
    excessive screen time, inactivity, poor posture, vitamin deficiencies, and low HRV.
    """
    score = 100.0
    breakdown = {}

    # PHQ9 penalty (max 30)
    phq9 = profile.get('phq9_score', 0)
    phq9_penalty = min(phq9 * 3, 30)
    breakdown['phq9_penalty'] = round(phq9_penalty, 1)
    score -= phq9_penalty

    # Sleep penalty (max 15)
    sleep = profile.get('sleep_hours', 7.5)
    if sleep < 6:
        sleep_penalty = 15
    elif sleep < 7:
        sleep_penalty = (7 - sleep) * 15
    else:
        sleep_penalty = 0
    breakdown['sleep_penalty'] = round(sleep_penalty, 1)
    score -= sleep_penalty

    # Stress penalty (max 15)
    stress = profile.get('stress_level', 5)
    stress_penalty = max(0, (stress - 4) * 2.5)
    breakdown['stress_penalty'] = round(min(stress_penalty, 15), 1)
    score -= min(stress_penalty, 15)

    # Screen time penalty (max 10)
    screen = profile.get('screen_time_hours', 6)
    screen_penalty = max(0, (screen - 6) * 1.67)
    breakdown['screen_penalty'] = round(min(screen_penalty, 10), 1)
    score -= min(screen_penalty, 10)

    # Inactivity penalty (max 10)
    exercise = profile.get('exercise_min', 30)
    if exercise < 15:
        exercise_penalty = 10
    elif exercise < 30:
        exercise_penalty = 5
    else:
        exercise_penalty = 0
    breakdown['exercise_penalty'] = round(exercise_penalty, 1)
    score -= exercise_penalty

    # Posture penalty (max 5)
    posture = profile.get('posture_score_pct', 70)
    posture_penalty = max(0, (60 - posture) / 12)
    breakdown['posture_penalty'] = round(min(posture_penalty, 5), 1)
    score -= min(posture_penalty, 5)

    # Vitamin D penalty (max 10)
    vitd = profile.get('vitamin_d', 30)
    if vitd and vitd < 20:
        vitd_penalty = 10
    elif vitd and vitd < 30:
        vitd_penalty = 5
    else:
        vitd_penalty = 0
    breakdown['vitd_penalty'] = round(vitd_penalty, 1)
    score -= vitd_penalty

    # HRV penalty (max 5)
    hrv = profile.get('hrv_ms', 40)
    if hrv and hrv < 20:
        hrv_penalty = 5
    elif hrv and hrv < 30:
        hrv_penalty = 3
    else:
        hrv_penalty = 0
    breakdown['hrv_penalty'] = round(hrv_penalty, 1)
    score -= hrv_penalty

    return {"score": round(max(score, 0), 1), "breakdown": breakdown}
```

### `nutrition_targets(profile: dict) -> dict`

Blood-work-aware daily nutrition targets.

```python
def nutrition_targets(profile: dict) -> dict:
    """Calculate personalized daily nutrition targets based on body composition and blood work.

    Adjusts protein for low muscle mass, saturated fat for high LDL,
    vitamin D/B12 for deficiencies, and water for temperature.
    """
    weight = profile.get('weight_kg', 70)
    bmr = profile.get('bmr', 1575)

    # Calories: BMR * 1.4 (moderate activity) or from actual BMR
    calories = round(bmr * 1.4) if bmr else round(weight * 30)

    # Protein: 1.2g per kg (higher if low muscle mass)
    muscle_ratio = (profile.get('muscle_mass_kg', 0) / weight) if weight else 0
    protein_mult = 1.5 if muscle_ratio < 0.35 else 1.2
    protein_g = round(weight * protein_mult)

    # Saturated fat: limit based on LDL
    ldl = profile.get('ldl', 100)
    if ldl > 160: sat_fat_g = 10
    elif ldl > 130: sat_fat_g = 11
    elif ldl > 100: sat_fat_g = 13
    else: sat_fat_g = 16

    # Fiber
    fiber_g = 30

    # Water: 35ml per kg + weather adjustment
    temp = profile.get('temperature_c', 28)
    water_ml = round(weight * 35 + (max(0, temp - 25) * 100))

    # Vitamin D target if deficient
    vitd_ug = 50 if (profile.get('vitamin_d', 30) < 20) else 15

    # B12 target if low
    b12_ug = 100 if (profile.get('b12', 300) < 300) else 2.4

    # Macros: fat = 25% of calories, carbs = remainder
    fat_g = round(calories * 0.25 / 9)
    carbs_g = round((calories - protein_g * 4 - fat_g * 9) / 4)

    return {
        "calories": calories,
        "protein_g": protein_g,
        "carbs_g": carbs_g,
        "fat_g": fat_g,
        "sat_fat_g": sat_fat_g,
        "fiber_g": fiber_g,
        "water_ml": water_ml,
        "vitamin_d_ug": vitd_ug,
        "b12_ug": b12_ug,
    }
```

### `simulate_habit_change(profile: dict, changes: dict) -> dict`

```python
def simulate_habit_change(profile: dict, changes: dict) -> dict:
    """Apply hypothetical lifestyle changes and recalculate bio age.

    Args:
        profile: Current health profile dict.
        changes: Dict of fields to override, e.g. {"sleep_hours": 8, "exercise_hours_week": 6}

    Returns:
        Dict with current bio ages, projected bio ages, and improvement delta.
    """
    modified = {**profile, **changes}
    current = calculate_bio_age(profile)
    projected = calculate_bio_age(modified)
    return {
        "current": current,
        "projected": projected,
        "improvement": round(current["overall"] - projected["overall"], 1)
    }
```

---

## File 5: `backend/gamification.py` — Streaks, XP, Achievements, Leaderboard

Uses `aiosqlite` for database operations. Import DB helper from `database.py`.

### Constants

```python
XP_AWARDS: dict[str, int] = {
    "meal_log": 10,
    "step_goal": 15,       # triggered when steps > 7500
    "sleep_goal": 15,      # triggered when sleep > 7h
    "water_goal": 5,       # triggered when daily water > 2000ml
    "checkin": 20,         # mental checkin or coach chat
    "selfie": 10,          # face age selfie
    "data_upload": 25,     # blood report or body comp upload
    "exercise_goal": 15,   # triggered when exercise > 30 min
}

LEVEL_THRESHOLDS: list[int] = [0, 100, 300, 600, 1000, 1500, 2500, 4000, 6000, 10000]

LEVEL_NAMES: list[str] = [
    "Health Rookie",
    "Data Conscious",
    "Pattern Seeker",
    "Bio Optimizer",
    "Longevity Learner",
    "Wellness Warrior",
    "Health Architect",
    "Age Defier",
    "Vitality Master",
    "EirView Legend",
]

ACHIEVEMENT_DEFS: dict[str, str] = {
    "first_blood": "Upload first blood report",
    "face_future": "First FaceAge selfie",
    "stand_tall": "Posture score >80%",
    "time_traveler": "Use Future Self chat",
    "know_thyself": "Complete PHQ-9 assessment",
    "age_bender": "Bio age improves by >1 year from first calculation",
    "data_complete": "90%+ of profile fields filled",
    "multi_source": "Ingest from 5+ different source types",
    "week_warrior": "7-day streak",
    "month_master": "30-day streak",
}
```

### Functions

```python
def get_level(xp: int) -> tuple[int, str]:
    """Return (level_number, level_name) for a given XP total.
    Level is the highest index where LEVEL_THRESHOLDS[index] <= xp."""

async def log_action(user_id: str, action: str, db: aiosqlite.Connection) -> dict:
    """Log a daily action, award XP, update streak, check achievements.

    Steps:
    1. Check if action already logged today (UNIQUE constraint). If duplicate, return current state.
    2. Insert into daily_actions with xp from XP_AWARDS.
    3. Update streaks table: add XP, recalculate level.
    4. Check streak: count distinct actions today. If >= 3, it's a streak day.
       - If last_streak_date == yesterday, increment current_streak.
       - If last_streak_date == today, no change.
       - Else, reset current_streak to 1.
       - Update longest_streak if current > longest.
       - Set last_streak_date = today.
    5. Call check_achievements(user_id, db).
    6. Return full gamification state via get_gamification().
    """

async def get_gamification(user_id: str, db: aiosqlite.Connection) -> dict:
    """Return full gamification state:
    {
        "current_streak": int,
        "longest_streak": int,
        "total_xp": int,
        "level": int,
        "level_name": str,
        "xp_to_next_level": int,
        "today_actions": list[str],  # actions logged today
        "achievements": list[dict],  # [{badge_id, description, earned_at}]
        "active_challenge": dict | None,  # current weekly challenge
    }
    """

async def get_leaderboard(db: aiosqlite.Connection) -> list[dict]:
    """Return all users ranked by XP descending.
    Each entry: {user_id, name, total_xp, level, level_name, current_streak}
    Join streaks with users table."""

async def check_achievements(user_id: str, db: aiosqlite.Connection) -> list[str]:
    """Check all achievement conditions for the user. Award any newly earned ones.

    Condition checks:
    - "first_blood": profile has any blood work field non-null (ldl, hdl, etc.)
    - "face_future": profile has face_age non-null
    - "stand_tall": profile posture_score_pct > 80
    - "time_traveler": agent_logs has action containing 'future_self'
    - "know_thyself": profile has phq9_score non-null
    - "age_bender": compare current bio_age_overall with first recorded value, improvement > 1
    - "data_complete": count non-null fields in profile / total fields > 0.9
    - "multi_source": count distinct sources in data_sources where last_synced_at is not null >= 5
    - "week_warrior": current_streak >= 7
    - "month_master": current_streak >= 30

    Insert new achievements (ignore if already exists via UNIQUE constraint).
    Return list of newly earned badge_ids.
    """
```

---

## File 6: `backend/family.py` — Family Groups & Health Flags

### Functions

```python
import string
import random
import uuid

async def create_family(name: str, creator_user_id: str, db: aiosqlite.Connection) -> dict:
    """Create a family group.

    1. Generate a unique family ID (uuid4 hex[:8]).
    2. Generate a 6-character join code: uppercase letters + digits, check uniqueness.
    3. Insert into families table.
    4. Add creator to family_members with relationship='self', role='admin'.
    5. Update users.family_id for the creator.
    6. Return {id, name, join_code, created_by}.
    """

async def join_family(join_code: str, user_id: str, relationship: str,
                      privacy_level: str, db: aiosqlite.Connection) -> dict:
    """Join an existing family group.

    1. Look up family by join_code. Raise ValueError if not found.
    2. Insert into family_members with given relationship and privacy_level, role='member'.
    3. Update users.family_id.
    4. Call update_family_flags(family_id, db) to re-derive family history.
    5. Return family info dict.
    """

async def get_family_dashboard(family_id: str, db: aiosqlite.Connection) -> dict:
    """Get family dashboard with member info respecting privacy levels.

    Returns:
    {
        "family": {id, name, join_code},
        "members": [
            {
                "user_id": str,
                "name": str,
                "relationship": str,
                "role": str,
                "privacy_level": str,
                # If privacy_level == "full": include bio_age, all scores
                # If privacy_level == "summary": include bio_age, mental_wellness_score only
                # If privacy_level == "none": only name and relationship
                "bio_age_overall": float | None,
                "mental_wellness_score": float | None,
                ...
            }
        ],
        "health_flags": [
            {"condition": str, "evidence": str, "severity": str, "detected_at": str}
        ],
    }
    """

async def update_family_flags(family_id: str, db: aiosqlite.Connection) -> None:
    """Scan all family members' profiles and derive family health conditions.

    For each member, check these conditions against their profile:
    - "diabetes": fasting_glucose > 100 OR hba1c > 5.7
    - "heart_disease": ldl > 160 OR total_cholesterol > 240
    - "hypertension": blood_pressure_systolic > 130 OR blood_pressure_diastolic > 85
    - "mental_health": phq9_score > 10
    - "thyroid": tsh > 4.5 OR tsh < 0.4

    For each detected condition:
    1. Insert/replace into family_health_flags with evidence string and severity.
    2. Update OTHER members' family_* boolean flags in their profiles.
       For example, if member A has diabetes detected, set family_diabetes=1 for all OTHER members.

    Severity levels:
    - "borderline": value is within 10% above threshold
    - "moderate": value is 10-30% above threshold
    - "severe": value is >30% above threshold
    """
```

---

## File 7: `backend/specialists.py` — Condition-to-Specialist Mapping

This file is **pure Python**, no database, no async. Takes a profile dict, returns recommendations.

### Specialist Map

```python
SPECIALIST_MAP: list[dict] = [
    {
        "specialist": "cardiologist",
        "triggers": [
            {"metric": "ldl", "threshold": 160, "op": ">", "reason": "Very high LDL cholesterol"},
            {"metric": "total_cholesterol", "threshold": 240, "op": ">", "reason": "High total cholesterol"},
            {"metric": "blood_pressure_systolic", "threshold": 140, "op": ">", "reason": "Stage 2 hypertension (systolic)"},
            {"metric": "blood_pressure_diastolic", "threshold": 90, "op": ">", "reason": "Stage 2 hypertension (diastolic)"},
            {"metric": "resting_hr", "threshold": 100, "op": ">", "reason": "Tachycardia at rest"},
        ],
        "hospitals": [
            "Narayana Institute of Cardiac Sciences, Bommasandra",
            "Jayadeva Institute of Cardiovascular Sciences, Jayanagar",
            "Manipal Hospital, Old Airport Road",
        ]
    },
    {
        "specialist": "endocrinologist",
        "triggers": [
            {"metric": "fasting_glucose", "threshold": 126, "op": ">=", "reason": "Diabetic-range fasting glucose"},
            {"metric": "hba1c", "threshold": 6.5, "op": ">=", "reason": "Diabetic-range HbA1c"},
            {"metric": "tsh", "threshold": 4.5, "op": ">", "reason": "Possible hypothyroidism"},
            {"metric": "tsh", "threshold": 0.4, "op": "<", "reason": "Possible hyperthyroidism"},
            {"metric": "vitamin_d", "threshold": 10, "op": "<", "reason": "Severe vitamin D deficiency"},
        ],
        "hospitals": [
            "Bangalore Endocrinology & Diabetes Research Centre",
            "M.S. Ramaiah Memorial Hospital, MSRIT Post",
            "Apollo Hospital, Bannerghatta Road",
        ]
    },
    {
        "specialist": "psychiatrist",
        "triggers": [
            {"metric": "phq9_score", "threshold": 15, "op": ">=", "reason": "Moderately severe depression (PHQ-9)"},
        ],
        "hospitals": [
            "NIMHANS, Hosur Road",
            "Cadabams Hospitals, Whitefield",
            "The Mind Research Foundation, Indiranagar",
        ]
    },
    {
        "specialist": "psychologist",
        "triggers": [
            {"metric": "phq9_score", "threshold": 10, "op": ">=", "reason": "Moderate depression (PHQ-9)"},
            {"metric": "stress_level", "threshold": 8, "op": ">=", "reason": "High chronic stress"},
        ],
        "hospitals": [
            "NIMHANS, Hosur Road",
            "Mpower, Indiranagar",
            "Amaha (online platform)",
        ]
    },
    {
        "specialist": "pulmonologist",
        "triggers": [
            {"metric": "blood_oxygen_pct", "threshold": 94, "op": "<", "reason": "Low blood oxygen saturation"},
            {"metric": "respiratory_rate", "threshold": 20, "op": ">", "reason": "Elevated respiratory rate"},
        ],
        "hospitals": [
            "St. John's Medical College Hospital, Koramangala",
            "Aster CMI Hospital, Hebbal",
            "Fortis Hospital, Bannerghatta Road",
        ]
    },
    {
        "specialist": "orthopedist",
        "triggers": [
            {"metric": "posture_score_pct", "threshold": 50, "op": "<", "reason": "Very poor posture score"},
            {"metric": "walking_asymmetry_pct", "threshold": 8, "op": ">", "reason": "Significant gait asymmetry"},
        ],
        "hospitals": [
            "Sparsh Hospital, Infantry Road",
            "Hosmat Hospital, Richmond Road",
            "Sakra World Hospital, Bellandur",
        ]
    },
    {
        "specialist": "nephrologist",
        "triggers": [
            {"metric": "creatinine", "threshold": 1.3, "op": ">", "reason": "Elevated creatinine (kidney function)"},
        ],
        "hospitals": [
            "BGS Global Hospitals, Uttarahalli",
            "Manipal Hospital, Old Airport Road",
            "Columbia Asia, Hebbal",
        ]
    },
    {
        "specialist": "hepatologist",
        "triggers": [
            {"metric": "sgpt_alt", "threshold": 56, "op": ">", "reason": "Elevated liver enzyme (ALT)"},
            {"metric": "sgot_ast", "threshold": 40, "op": ">", "reason": "Elevated liver enzyme (AST)"},
        ],
        "hospitals": [
            "Aster CMI Hospital, Hebbal",
            "Manipal Hospital, Old Airport Road",
            "Apollo Hospital, Seshadripuram",
        ]
    },
]
```

### Functions

```python
def check_specialist_needs(profile: dict) -> list[dict]:
    """Check all specialist triggers against the profile.

    For each specialist in SPECIALIST_MAP, check all triggers.
    If any trigger fires, include that specialist in results (only once per specialist,
    but list all triggered reasons).

    Returns list of:
    {
        "specialist": str,
        "reasons": [str],        # all triggered reasons
        "metrics": [{metric, value, threshold}],
        "urgency": "routine" | "soon" | "urgent",  # based on how far above threshold
        "hospitals": [str],
    }

    Urgency logic:
    - "urgent": any metric > 1.5x threshold (or < 0.5x for "<" operators)
    - "soon": any metric > 1.2x threshold
    - "routine": otherwise
    """
```

---

## File 8: `backend/reminder_engine.py` — Data Freshness & Medical Reminders

### Constants

```python
DATA_REFRESH_INTERVALS: dict[str, int] = {
    "healthkit": 2,        # days
    "meal": 1,
    "water": 1,
    "posture": 7,
    "faceage": 30,
    "blood_report": 90,    # or 180 if values normal
    "cultfit": 30,
    "mental_checkin": 7,
    "spotify": 3,
}
```

### Functions

```python
async def get_reminders(user_id: str, db: aiosqlite.Connection) -> list[dict]:
    """Generate all reminders for a user.

    Combines data freshness reminders + medical checkup reminders.

    Returns list of:
    {
        "type": "data_freshness" | "medical_checkup",
        "source": str,            # e.g., "healthkit", "blood_report", "vitamin_d_retest"
        "message": str,           # human-readable reminder
        "urgency": "low" | "medium" | "high",
        "days_overdue": int,      # how many days past the refresh interval
        "last_synced": str | None,  # ISO datetime
    }

    Data freshness checks:
    1. Query data_sources for the user.
    2. For each source, compute days since last_synced_at.
    3. For "blood_report": use 180 days if all blood values are in normal range, else 90 days.
    4. If overdue, create a reminder. Urgency:
       - overdue by < 50%: "low"
       - overdue by 50-100%: "medium"
       - overdue by > 100%: "high"

    Medical checkup reminders:
    1. If vitamin_d < 20 and last_vitd_test_date > 90 days ago: remind to retest.
    2. If fasting_glucose > 100 and last_glucose_test_date > 90 days ago: remind.
    3. If last_general_checkup_date > 365 days ago or is null: remind for annual checkup.
    4. If LDL > 130: blood panel every 3 months instead of 6.
    """
```

---

## File 9: `backend/alerts.py` — Critical Threshold Detection & Doctor Alerts

### Constants

```python
CRITICAL_THRESHOLDS: list[dict] = [
    {"metric": "blood_pressure_systolic", "threshold": 180, "op": ">", "severity": "critical", "message": "Hypertensive crisis — systolic BP {value}"},
    {"metric": "blood_pressure_diastolic", "threshold": 120, "op": ">", "severity": "critical", "message": "Hypertensive crisis — diastolic BP {value}"},
    {"metric": "fasting_glucose", "threshold": 250, "op": ">", "severity": "critical", "message": "Dangerously high blood glucose: {value} mg/dL"},
    {"metric": "resting_hr", "threshold": 120, "op": ">", "severity": "critical", "message": "Resting heart rate critically high: {value} bpm"},
    {"metric": "resting_hr", "threshold": 40, "op": "<", "severity": "critical", "message": "Resting heart rate critically low: {value} bpm"},
    {"metric": "blood_oxygen_pct", "threshold": 90, "op": "<", "severity": "critical", "message": "Blood oxygen dangerously low: {value}%"},
    {"metric": "phq9_score", "threshold": 20, "op": ">", "severity": "critical", "message": "Severe depression score (PHQ-9): {value}"},
    {"metric": "ldl", "threshold": 190, "op": ">", "severity": "high", "message": "Very high LDL cholesterol: {value} mg/dL"},
    {"metric": "hba1c", "threshold": 9, "op": ">", "severity": "high", "message": "Very high HbA1c: {value}%"},
]

CRISIS_RESOURCES_INDIA: dict[str, str] = {
    "Vandrevala Foundation": "1860-2662-345",
    "iCall": "9152987821",
    "AASRA": "9820466726",
}
```

### Functions

```python
def check_critical_values(profile: dict) -> list[dict]:
    """Check all critical thresholds against the profile.

    Returns list of:
    {
        "metric": str,
        "value": float,
        "threshold": float,
        "severity": "critical" | "high",
        "message": str,  # with {value} replaced
        "requires_doctor_alert": bool,  # True if severity == "critical"
        "crisis_resources": dict | None,  # included if metric is phq9_score
    }
    """

async def process_alerts(user_id: str, profile: dict, db: aiosqlite.Connection) -> list[dict]:
    """Run check_critical_values, log alerts to DB, return them.

    For each alert:
    1. Insert into alerts table.
    2. If requires_doctor_alert and profile has doctor_email: call send_doctor_alert.
    3. Return the list of alerts with IDs.
    """

async def send_doctor_alert(user_id: str, alert: dict, db: aiosqlite.Connection) -> bool:
    """Send an email alert to the user's doctor.

    Uses smtplib with SMTP_HOST, SMTP_PORT, SMTP_USER, SMTP_PASS from environment variables.
    If env vars are missing, log a warning and return False (don't crash).

    Email content includes:
    - Patient name and ID
    - The critical metric, value, and threshold
    - Timestamp
    - Recommendation to follow up

    Updates the alert record with doctor_notified=1 and doctor_email_sent_at.
    Returns True if sent successfully, False otherwise.
    """
```

---

## File 10: `backend/activity.py` — Workouts, Targets, Inactivity Detection

### Constants

```python
WORKOUT_IMPACT_MAP: dict[str, dict[str, float]] = {
    "running":          {"cv": -0.3, "neuro": -0.1},
    "walking":          {"cv": -0.15},
    "weight_training":  {"msk": -0.3, "met": -0.1},
    "yoga":             {"msk": -0.2, "neuro": -0.2},
    "hiit":             {"cv": -0.4, "met": -0.15},
    "swimming":         {"cv": -0.3, "msk": -0.15},
    "cycling":          {"cv": -0.25, "msk": -0.1},
}
```

### Functions

```python
async def log_workout(user_id: str, workout_data: dict, db: aiosqlite.Connection) -> dict:
    """Log a workout with computed bio-age impacts.

    1. Look up workout type in WORKOUT_IMPACT_MAP. If not found, default to {"cv": -0.1}.
    2. Scale impacts by duration: impact * (duration_min / 30). Cap each at 2x base impact.
    3. Insert into workouts table with cv_impact, msk_impact, met_impact, neuro_impact.
    4. Return the workout record with ID.
    """

async def get_workout_summary(user_id: str, days: int, db: aiosqlite.Connection) -> dict:
    """Summarize workouts over the last N days.

    Returns:
    {
        "total_sessions": int,
        "total_minutes": int,
        "total_calories": float,
        "workout_types": {type: count},
        "impact_totals": {"cv": float, "msk": float, "met": float, "neuro": float},
        "avg_sessions_per_week": float,
    }
    """

def workout_targets(profile: dict) -> dict:
    """Generate profile-aware weekly workout recommendations.

    Logic:
    - Base: 150 min moderate OR 75 min vigorous per week (WHO guideline).
    - If bio_age_cardiovascular > chrono age: add +1 cardio session recommendation.
    - If bio_age_musculoskeletal > chrono age: add +1 strength session.
    - If bio_age_neurological > chrono age: add +1 yoga/mindfulness session.
    - If BMI > 25: prioritize HIIT and running.
    - If posture_score_pct < 70: recommend yoga/stretching.
    - If vo2max < 35: prioritize zone 2 cardio (walking, cycling).

    Returns:
    {
        "weekly_target_min": int,
        "recommended_sessions": [
            {"type": str, "frequency": str, "duration_min": int, "reason": str}
        ],
        "priority_areas": [str],  # e.g., ["cardiovascular", "flexibility"]
    }
    """

def check_inactivity(profile: dict, current_hour: int) -> dict | None:
    """Check if user is behind on daily activity and should be nudged.

    Logic:
    - Expected steps by hour = (steps_avg_7d / 16) * hours_awake (assume wake at 7am).
    - If current steps < 60% of expected: return nudge.
    - If exercise_min < 10 and it's past 6pm: return nudge.
    - Otherwise return None.

    Returns (if nudge needed):
    {
        "type": "step_nudge" | "exercise_nudge",
        "message": str,
        "steps_behind": int | None,
        "suggested_activity": str,  # e.g., "Take a 15-minute walk"
    }
    """
```

---

## Implementation Requirements

1. **All files must be syntactically valid Python 3.11+** and importable.
2. Use `from __future__ import annotations` in every file.
3. Every public function must have a docstring.
4. Every function must have complete type hints (parameters and return type).
5. Use `aiosqlite` for all database operations. Use `async with aiosqlite.connect(DB_PATH) as db:` pattern inside each function, OR accept a `db: aiosqlite.Connection` parameter.
6. For `database.py`, functions that are called externally should create their own connection. Functions called internally (like seed) can share connections.
7. Use `uuid.uuid4().hex[:8]` for generating IDs where needed.
8. Handle None/missing values gracefully everywhere - never crash on missing data.
9. Use `datetime.date.today()` and `datetime.datetime.now()` for date/time operations.
10. The `formulas.py` and `specialists.py` files must be pure (no async, no DB imports).
11. Create `backend/__init__.py` that exports key functions for convenience.

## Output Structure

Create these files:
```
backend/
  __init__.py
  database.py
  health_state.py
  formulas.py
  gamification.py
  family.py
  specialists.py
  reminder_engine.py
  alerts.py
  activity.py
```

Generate all 10 files completely. Do not use placeholder comments like "# TODO" or "# implement later". Every function must be fully implemented.
