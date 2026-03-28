from __future__ import annotations

import json
import os
import tempfile
from contextlib import asynccontextmanager
from datetime import datetime
from typing import Any

from dotenv import load_dotenv
from fastapi import FastAPI, File, Form, HTTPException, Request, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse

from backend.activity import check_inactivity, get_workout_summary, get_workouts, get_workout_targets, log_workout
from backend.agents import coach, collector, mental_health, mirror, runner, time_machine
from backend.ai_router import ai_router
from backend.alerts import check_alerts, notify_doctor, process_alerts
from backend.database import (
    create_user,
    get_all_users,
    get_db,
    get_meals,
    get_profile_dict,
    get_risk_projections,
    get_water_today,
    init_db,
    log_meal as db_log_meal,
    log_water as db_log_water,
    save_risk_projections,
    update_profile_fields,
)
from backend.family import create_family, get_family_dashboard, join_family
from backend.formulas import calculate_bio_age, mental_wellness_score, nutrition_targets, simulate_habit_change
from backend.gamification import get_gamification_summary, get_leaderboard, process_action
from backend.parsers import analyze_meal_photo, parse_apple_health_xml
from backend.reports import build_doctor_report, render_doctor_report_text
from backend.reminder_engine import check_reminders
from backend.specialists import check_specialists

load_dotenv()

CORS_ORIGINS = [
    origin.strip()
    for origin in os.getenv("EIRVIEW_CORS_ORIGINS", "http://127.0.0.1:5173,http://localhost:5173").split(",")
    if origin.strip()
]


@asynccontextmanager
async def lifespan(app: FastAPI) -> Any:
    """Initialize persistent resources on startup."""

    await init_db()
    yield


app = FastAPI(title="EirView API", version="1.0.0", lifespan=lifespan)
app.add_middleware(CORSMiddleware, allow_origins=CORS_ORIGINS, allow_credentials=True, allow_methods=["*"], allow_headers=["*"])


def _serialize_rows(rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    """Return JSON-safe row dicts."""

    return [{key: value for key, value in row.items()} for row in rows]


def _trim_chat_history(history: list[dict[str, Any]], limit: int = 6) -> list[dict[str, Any]]:
    """Keep only the most recent chat turns and cap message length."""

    trimmed: list[dict[str, Any]] = []
    for item in history[-limit:]:
        trimmed.append({"role": item.get("role", "user"), "content": str(item.get("content", ""))[-1200:]})
    return trimmed


COACH_ALLOWED_KEYWORDS = {
    "health", "bio age", "biological age", "wellness", "habit", "habits", "nutrition", "food", "meal", "eat", "diet",
    "calories", "protein", "carbs", "fat", "fiber", "water", "hydration", "exercise", "workout", "training", "walk",
    "walking", "run", "running", "steps", "sleep", "stress", "recovery", "remainder", "reminder", "doctor", "specialist",
    "bp", "blood pressure", "hrv", "resting hr", "heart rate", "spo2", "oxygen", "vo2", "cholesterol", "ldl", "hdl",
    "glucose", "hba1c", "vitamin", "b12", "vitamin d", "tsh", "ferritin", "creatinine", "posture", "weight", "bmi",
    "mood", "mental", "burnout", "routine", "focus on", "what should i do", "what next", "plan", "goal", "goals",
    "improve", "reduce", "increase", "lower", "raise"
}


def _is_coach_question_in_scope(message: str) -> bool:
    """Return True when the coach message is clearly about health coaching."""

    normalized = " ".join(str(message or "").lower().split())
    if not normalized:
        return False
    return any(keyword in normalized for keyword in COACH_ALLOWED_KEYWORDS)


async def _stream_static_sse(message: str) -> Any:
    """Yield a short static SSE response."""

    yield f"data: {json.dumps({'type': 'text', 'content': message})}\n\n"
    yield f"data: {json.dumps({'type': 'done'})}\n\n"


def _enrich_specialist_recommendations(profile: dict[str, Any], specialists: list[dict[str, Any]]) -> list[dict[str, Any]]:
    """Attach doctor-report evidence for each specialist recommendation."""

    enriched: list[dict[str, Any]] = []
    for item in specialists:
        report = build_doctor_report(profile, alerts=[], specialists=[item])
        enriched.append({**item, "doctor_report": report, "doctor_report_text": render_doctor_report_text(report)})
    return enriched


@app.get("/api/users")
async def list_users() -> list[dict[str, Any]]:
    """List all users."""

    return await get_all_users()


@app.post("/api/users")
async def create_user_endpoint(request: Request) -> dict[str, Any]:
    """Create a new user."""

    data = await request.json()
    try:
        return await create_user(data["id"], data["name"], data.get("age"), data.get("sex"), data.get("height_cm"))
    except KeyError as exc:
        raise HTTPException(status_code=400, detail=f"Missing field: {exc}") from exc


@app.get("/api/profile/{user_id}")
async def get_profile_endpoint(user_id: str) -> dict[str, Any]:
    """Get the full health profile for a user."""

    db = await get_db()
    try:
        profile = await get_profile_dict(user_id, db)
        if profile is None:
            raise HTTPException(status_code=404, detail=f"User {user_id} not found")
        return profile
    finally:
        await db.close()


@app.put("/api/profile/{user_id}")
async def update_profile_endpoint(user_id: str, request: Request) -> dict[str, Any]:
    """Update specific profile fields for a user."""

    data = await request.json()
    db = await get_db()
    try:
        profile = await update_profile_fields(user_id, data, db)
        alerts = await process_alerts(user_id, profile, db)
        return {"success": True, "updated_fields": list(data.keys()), "profile": profile, "alerts": alerts}
    finally:
        await db.close()


@app.get("/api/dashboard/{user_id}")
async def get_dashboard(user_id: str) -> dict[str, Any]:
    """Get complete dashboard data for a user."""

    db = await get_db()
    try:
        profile = await get_profile_dict(user_id, db)
        if profile is None:
            raise HTTPException(status_code=404, detail=f"User {user_id} not found")
        bio_age = calculate_bio_age(profile)
        reminder_list = await check_reminders(user_id, db)
        alerts = await check_alerts(user_id, db)
        specialists = _enrich_specialist_recommendations(profile, check_specialists(profile))
        gamification = await get_gamification_summary(user_id, db)
        nutrition = nutrition_targets(profile)
        workout_summary = await get_workout_summary(user_id, db)
        workout_target_data = await get_workout_targets(user_id, db)
        meals = await get_meals(user_id)
        wellness = mental_wellness_score(profile)
        risk_rows = await get_risk_projections(user_id)
        if not risk_rows:
            from backend.formulas import project_risk

            risk_rows = project_risk(profile)
            await save_risk_projections(user_id, risk_rows)
        metrics = {
            "resting_hr": profile.get("resting_hr"),
            "hrv": profile.get("hrv_ms"),
            "steps": profile.get("steps_today"),
            "sleep": profile.get("sleep_hours"),
            "vo2max": profile.get("vo2max"),
            "spo2": profile.get("blood_oxygen_pct"),
            "exercise_min": profile.get("exercise_min"),
            "flights": profile.get("flights_climbed"),
        }
        nudge = check_inactivity(profile, datetime.now().hour)
        cross_domain = (
            "Your sleep, stress, and activity pattern suggest your neurological age would improve fastest from more consistent sleep and a small daily walk."
            if (profile.get("sleep_hours") or 0) < 7
            else "Your current pattern is stable. The biggest upside now is consistency rather than drastic change."
        )
        return {
            "profile": profile,
            "bio_age_overall": bio_age["overall"],
            "bio_age": bio_age,
            "bio_age_deltas": bio_age["deltas"],
            "face_age": profile.get("face_age"),
            "metrics": metrics,
            "step_goal": max(profile.get("steps_avg_7d") or 7500, 7500),
            "reminders": reminder_list,
            "alerts": alerts,
            "specialists": specialists,
            "gamification": gamification,
            "nutrition_targets": nutrition,
            "workout_summary": workout_summary,
            "workout_targets": workout_target_data,
            "recent_meals": meals,
            "wellness_score": wellness["score"],
            "wellness_breakdown": wellness["breakdown_list"],
            "risk_projections": risk_rows,
            "cross_domain_insight": cross_domain,
            "narrative": f"Your biological age is {bio_age['overall']} versus chronological age {profile.get('age')}. Cardiovascular and neurological patterns are currently the main leverage points.",
            "activity_nudge": nudge,
        }
    finally:
        await db.close()


@app.post("/api/ingest")
async def ingest_data(file: UploadFile = File(...), data_type: str = Form(...), user_id: str = Form(...)) -> dict[str, Any]:
    """Upload blood PDF, Cult.fit image, or Apple Health XML and update the profile."""

    db = await get_db()
    tmp_path = ""
    try:
        suffix = os.path.splitext(file.filename or "")[1] or ".tmp"
        with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as tmp:
            content = await file.read()
            tmp.write(content)
            tmp_path = tmp.name
        if data_type == "blood_pdf":
            from backend.parsers import parse_blood_pdf

            extracted = await parse_blood_pdf(tmp_path, user_id, db)
        elif data_type == "cultfit_image":
            from backend.parsers import parse_cultfit_image

            extracted = await parse_cultfit_image(tmp_path, user_id, db)
        elif data_type == "apple_health_xml":
            extracted = parse_apple_health_xml(tmp_path)
        else:
            raise HTTPException(status_code=400, detail=f"Unsupported data_type: {data_type}")
        workouts = extracted.pop("workouts_7d", []) if isinstance(extracted, dict) else []
        profile_updates = extracted.get("profile_updates", extracted) if isinstance(extracted, dict) else {}
        profile = await update_profile_fields(user_id, profile_updates if isinstance(profile_updates, dict) else {}, db)
        for workout in workouts:
            await log_workout(user_id, workout, db)
        alerts = await process_alerts(user_id, profile, db)
        specialists = _enrich_specialist_recommendations(profile, check_specialists(profile))
        mirror_result = await runner.run_agent(mirror, user_id, {}, db)
        await process_action(user_id, "data_upload", None, db)
        return {
            "success": True,
            "data_type": data_type,
            "extracted": extracted,
            "profile_updates_applied": profile_updates,
            "profile": profile,
            "alerts": alerts,
            "specialists": specialists,
            "mirror": mirror_result["result"],
            "workouts_logged": len(workouts),
        }
    finally:
        if tmp_path and os.path.exists(tmp_path):
            os.unlink(tmp_path)
        await db.close()


@app.post("/api/face-age")
async def face_age_endpoint(file: UploadFile = File(...), user_id: str = Form(...)) -> dict[str, Any]:
    """Accept a selfie image, run face age prediction, and persist it."""

    image_bytes = await file.read()
    try:
        from backend.faceage import predict_face_age

        face_age = predict_face_age(image_bytes)
    except Exception:
        face_age = 0.0
    db = await get_db()
    try:
        profile = await update_profile_fields(user_id, {"face_age": face_age}, db)
        await process_action(user_id, "selfie", None, db)
        return {"face_age": face_age, "profile": profile}
    finally:
        await db.close()


@app.post("/api/healthkit")
async def receive_healthkit(request: Request) -> dict[str, Any]:
    """Receive HealthKit-style JSON and update the profile."""

    data = await request.json()
    user_id = data.get("user_id")
    if not user_id:
        raise HTTPException(status_code=400, detail="Missing user_id")
    health_data = data.get("data", {})
    db = await get_db()
    try:
        profile = await update_profile_fields(user_id, health_data, db)
        return {"success": True, "updated_fields": list(health_data.keys()), "profile": profile}
    finally:
        await db.close()


@app.post("/api/apple-health")
async def upload_apple_health(file: UploadFile = File(...), user_id: str = Form(...)) -> dict[str, Any]:
    """Upload Apple Health export.xml, parse it, update profile, and store workouts."""

    db = await get_db()
    tmp_path = ""
    try:
        with tempfile.NamedTemporaryFile(delete=False, suffix=".xml") as tmp:
            tmp.write(await file.read())
            tmp_path = tmp.name
        health_data = parse_apple_health_xml(tmp_path)
        workouts = health_data.pop("workouts_7d", [])
        profile = await update_profile_fields(user_id, health_data, db)
        for workout in workouts:
            await log_workout(user_id, workout, db)
        return {"success": True, "metrics_updated": list(health_data.keys()), "workouts_found": len(workouts), "data": health_data, "profile": profile}
    finally:
        if tmp_path and os.path.exists(tmp_path):
            os.unlink(tmp_path)
        await db.close()


@app.post("/api/meal")
async def log_meal_endpoint(request: Request, file: UploadFile | None = File(None)) -> dict[str, Any]:
    """Log a meal via photo upload or text description."""

    db = await get_db()
    try:
        if file is not None:
            form = await request.form()
            user_id = str(form.get("user_id", "zahoor"))
            result = await analyze_meal_photo(await file.read(), user_id, db)
            await db_log_meal(user_id, result, db)
            await process_action(user_id, "meal_log", None, db)
            return result
        data = await request.json()
        user_id = data.get("user_id")
        description = data.get("description")
        if not user_id or not description:
            raise HTTPException(status_code=400, detail="Provide user_id and description")
        result = {
            "description": description,
            "items": [{"item": description, "portion_g": data.get("portion_g", 100), "calories": 350, "protein_g": 15, "carbs_g": 45, "fat_g": 10, "sat_fat_g": 3, "fiber_g": 5}],
            "total": {"calories": 350, "protein_g": 15, "carbs_g": 45, "fat_g": 10, "sat_fat_g": 3, "fiber_g": 5},
            "flags": [],
            "grounding": "USDA fallback estimate",
        }
        await db_log_meal(user_id, result, db)
        await process_action(user_id, "meal_log", None, db)
        return result
    finally:
        await db.close()


@app.post("/api/water")
async def log_water_endpoint(request: Request) -> dict[str, Any]:
    """Log water intake for a user."""

    data = await request.json()
    user_id = data.get("user_id")
    amount_ml = int(data.get("amount_ml", 250))
    if not user_id:
        raise HTTPException(status_code=400, detail="Missing user_id")
    await db_log_water(user_id, amount_ml)
    db = await get_db()
    try:
        today_total = await get_water_today(user_id)
        await process_action(user_id, "water_goal" if today_total >= 2000 else "meal_log", None, db)
        return {"success": True, "amount_ml": amount_ml, "today_total_ml": today_total, "target_ml": 2500, "pct_complete": round(today_total / 2500 * 100, 1)}
    finally:
        await db.close()


@app.post("/api/simulate")
async def simulate_endpoint(request: Request) -> dict[str, Any]:
    """Simulate the effect of a habit change on bio age and risk projections."""

    data = await request.json()
    user_id = data.get("user_id")
    changes = data.get("changes", {})
    if not user_id:
        raise HTTPException(status_code=400, detail="Missing user_id")
    db = await get_db()
    try:
        profile = await get_profile_dict(user_id, db)
        if profile is None:
            raise HTTPException(status_code=404, detail=f"User {user_id} not found")
        simulation = simulate_habit_change(profile, changes)
        narrative = await runner.run_agent(time_machine, user_id, {"changes": changes}, db)
        return {"simulation": simulation, "narrative": narrative["result"], "traces": narrative["traces"]}
    finally:
        await db.close()


@app.post("/api/chat/future")
async def chat_future(request: Request) -> StreamingResponse:
    """Future-self SSE chat endpoint."""

    data = await request.json()
    user_id = data.get("user_id", "zahoor")
    message = str(data.get("message", ""))[-1200:]
    history = _trim_chat_history(data.get("history", []))
    db = await get_db()

    async def stream_future_self() -> Any:
        try:
            profile = await get_profile_dict(user_id, db)
            bio_age = calculate_bio_age(profile or {})
            age = (profile or {}).get("age", 19)
            name = (profile or {}).get("name", "you")
            prompt = f"You are {name} at age {age + 15}, speaking to your younger self. Their bio age is {bio_age['overall']}."
            messages = history
            messages.append({"role": "user", "content": message})
            with ai_router.stream_claude(system=prompt, messages=messages, max_tokens=ai_router.chat_max_tokens) as stream:
                for event in stream:
                    if getattr(event, "type", "") == "content_block_delta" and hasattr(event.delta, "text"):
                        yield f"data: {json.dumps({'type': 'text', 'content': event.delta.text})}\n\n"
            yield f"data: {json.dumps({'type': 'done'})}\n\n"
        finally:
            await db.close()

    return StreamingResponse(stream_future_self(), media_type="text/event-stream")


@app.post("/api/chat/mental")
async def chat_mental(request: Request) -> StreamingResponse:
    """Mental-health SSE chat endpoint."""

    data = await request.json()
    db = await get_db()
    return StreamingResponse(
        runner.stream_agent(
            mental_health,
            data.get("user_id", "zahoor"),
            {"message": str(data.get("message", ""))[-1200:], "history": _trim_chat_history(data.get("history", []))},
            db,
            close_db=True,
        ),
        media_type="text/event-stream",
    )


@app.post("/api/chat/coach")
async def chat_coach(request: Request) -> StreamingResponse:
    """Coach SSE chat endpoint."""

    data = await request.json()
    message = str(data.get("message", ""))[-1200:]
    if not _is_coach_question_in_scope(message):
        return StreamingResponse(
            _stream_static_sse(
                "I’m the EirView health coach. I can help with your metrics, habits, nutrition, sleep, activity, recovery, reminders, and next-step planning."
            ),
            media_type="text/event-stream",
        )
    db = await get_db()
    return StreamingResponse(
        runner.stream_agent(
            coach,
            data.get("user_id", "zahoor"),
            {"message": message, "history": _trim_chat_history(data.get("history", []))},
            db,
            close_db=True,
        ),
        media_type="text/event-stream",
    )


@app.get("/api/transparency/{user_id}")
async def get_transparency(user_id: str) -> dict[str, Any]:
    """Return transparency data for the given user."""

    db = await get_db()
    try:
        cursor = await db.execute("SELECT * FROM agent_logs WHERE user_id=? ORDER BY timestamp DESC LIMIT 100", (user_id,))
        rows = await cursor.fetchall()
        logs = [dict(row) for row in rows]
        model_stats: dict[str, Any] = {}
        for entry in ai_router.call_log:
            model = entry["model"]
            bucket = model_stats.setdefault(model, {"calls": 0, "success": 0, "total_latency_ms": 0, "estimated_cost": 0})
            bucket["calls"] += 1
            bucket["success"] += int(bool(entry["success"]))
            bucket["total_latency_ms"] += entry["latency_ms"]
        for model, stats in model_stats.items():
            stats["avg_latency_ms"] = round(stats["total_latency_ms"] / max(stats["calls"], 1))
            stats["success_rate"] = round(stats["success"] / max(stats["calls"], 1) * 100, 1)
        return {"agent_logs": logs, "model_stats": model_stats, "recent_calls": ai_router.call_log[-50:]}
    finally:
        await db.close()


@app.get("/api/gamification/{user_id}")
async def gamification_summary(user_id: str) -> dict[str, Any]:
    """Get gamification summary."""

    db = await get_db()
    try:
        return await get_gamification_summary(user_id, db)
    finally:
        await db.close()


@app.post("/api/gamification/{user_id}/action")
async def gamification_action(user_id: str, request: Request) -> dict[str, Any]:
    """Log a gamification action."""

    data = await request.json()
    db = await get_db()
    try:
        return await process_action(user_id, data.get("action", ""), data.get("metadata"), db)
    finally:
        await db.close()


@app.get("/api/gamification/leaderboard")
async def gamification_leaderboard() -> list[dict[str, Any]]:
    """Get leaderboard data."""

    db = await get_db()
    try:
        return await get_leaderboard(db)
    finally:
        await db.close()


@app.post("/api/family")
async def create_family_endpoint(request: Request) -> dict[str, Any]:
    """Create a new family group."""

    data = await request.json()
    db = await get_db()
    try:
        return await create_family(data.get("name", "My Family"), data["created_by"], db)
    except KeyError as exc:
        raise HTTPException(status_code=400, detail=f"Missing field: {exc}") from exc
    finally:
        await db.close()


@app.post("/api/family/join")
async def join_family_endpoint(request: Request) -> dict[str, Any]:
    """Join an existing family group."""

    data = await request.json()
    db = await get_db()
    try:
        return await join_family(data["join_code"], data["user_id"], data["relationship"], data.get("privacy_level", "summary"), db)
    except KeyError as exc:
        raise HTTPException(status_code=400, detail=f"Missing field: {exc}") from exc
    finally:
        await db.close()


@app.get("/api/family/{family_id}")
async def get_family_endpoint(family_id: str) -> dict[str, Any]:
    """Get the family dashboard."""

    db = await get_db()
    try:
        return await get_family_dashboard(family_id, db)
    finally:
        await db.close()


@app.get("/api/reminders/{user_id}")
async def get_reminders_endpoint(user_id: str) -> list[dict[str, Any]]:
    """Get reminder data."""

    db = await get_db()
    try:
        return await check_reminders(user_id, db)
    finally:
        await db.close()


@app.get("/api/alerts/{user_id}")
async def get_alerts_endpoint(user_id: str) -> list[dict[str, Any]]:
    """Get health alerts."""

    db = await get_db()
    try:
        return await check_alerts(user_id, db)
    finally:
        await db.close()


@app.post("/api/alerts/{user_id}/notify-doctor")
async def notify_doctor_endpoint(user_id: str, request: Request) -> dict[str, Any]:
    """Send alert summary to the user's doctor."""

    data = await request.json()
    db = await get_db()
    try:
        alert_id = data.get("alert_id")
        alert_ids = [alert_id] if alert_id is not None else data.get("alert_ids", [])
        return await notify_doctor(user_id, data.get("doctor_email"), alert_ids, db)
    finally:
        await db.close()


@app.get("/api/specialists/{user_id}")
async def get_specialists_endpoint(user_id: str) -> list[dict[str, Any]]:
    """Get specialist recommendations."""

    db = await get_db()
    try:
        profile = await get_profile_dict(user_id, db)
        if profile is None:
            raise HTTPException(status_code=404, detail=f"User {user_id} not found")
        return _enrich_specialist_recommendations(profile, check_specialists(profile))
    finally:
        await db.close()


@app.get("/api/workouts/{user_id}")
async def get_workouts_endpoint(user_id: str) -> list[dict[str, Any]]:
    """Get recent workouts."""

    db = await get_db()
    try:
        return await get_workouts(user_id, db)
    finally:
        await db.close()


@app.post("/api/workouts/{user_id}")
async def log_workout_endpoint(user_id: str, request: Request) -> dict[str, Any]:
    """Log a new workout."""

    data = await request.json()
    db = await get_db()
    try:
        result = await log_workout(user_id, data, db)
        if (data.get("duration_min") or 0) >= 30:
            await process_action(user_id, "exercise_goal", None, db)
        return result
    finally:
        await db.close()


@app.get("/api/workouts/{user_id}/summary")
async def workout_summary_endpoint(user_id: str) -> dict[str, Any]:
    """Get workout summary."""

    db = await get_db()
    try:
        return await get_workout_summary(user_id, db)
    finally:
        await db.close()


@app.get("/api/workouts/{user_id}/targets")
async def workout_targets_endpoint(user_id: str) -> dict[str, Any]:
    """Get profile-aware workout targets."""

    db = await get_db()
    try:
        return await get_workout_targets(user_id, db)
    finally:
        await db.close()


@app.get("/api/spotify/callback")
async def spotify_callback(code: str, state: str = "") -> dict[str, Any]:
    """Handle Spotify OAuth callback and sync data."""

    from backend.spotify import exchange_spotify_code, sync_spotify

    db = await get_db()
    try:
        user_id = state or "zahoor"
        access_token = exchange_spotify_code(code)
        result = await sync_spotify(user_id, access_token, db)
        return {"success": True, "user_id": user_id, "spotify_data": result}
    finally:
        await db.close()


@app.get("/api/spotify/sync/{user_id}")
async def spotify_sync(user_id: str) -> dict[str, Any]:
    """Trigger Spotify sync or return auth URL."""

    from backend.spotify import sp_oauth, sync_spotify

    db = await get_db()
    try:
        row = await (await db.execute("SELECT access_token FROM spotify_tokens WHERE user_id=?", (user_id,))).fetchone()
        if row is None:
            return {"needs_auth": True, "auth_url": sp_oauth.get_authorize_url(state=user_id)}
        return {"success": True, "data": await sync_spotify(user_id, row["access_token"], db)}
    finally:
        await db.close()


@app.post("/api/posture")
async def receive_posture(request: Request) -> dict[str, Any]:
    """Receive posture score updates from the standalone posture runner."""

    data = await request.json()
    user_id = data.get("user_id", "zahoor")
    db = await get_db()
    try:
        await db.execute(
            "INSERT INTO posture_history (user_id, score_pct, avg_angle, is_slouching) VALUES (?,?,?,?)",
            (user_id, data.get("score_pct", 100), data.get("avg_angle", 180), data.get("is_slouching", False)),
        )
        profile = await update_profile_fields(user_id, {"posture_score_pct": data.get("score_pct", 100)}, db)
        recent = await (
            await db.execute("SELECT score_pct FROM posture_history WHERE user_id=? ORDER BY timestamp DESC LIMIT 5", (user_id,))
        ).fetchall()
        average_recent = sum(float(row["score_pct"]) for row in recent) / max(len(recent), 1)
        return {"success": True, "score_pct": data.get("score_pct", 100), "avg_recent_5": round(average_recent, 1), "nudge": average_recent < 50, "profile": profile}
    finally:
        await db.close()
