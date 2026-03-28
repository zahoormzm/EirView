from __future__ import annotations

import os
from collections import defaultdict
from typing import Any

from backend.database import get_profile_dict, get_recent_meals_db


async def get_profile(user_id: str, db: Any, **kwargs: Any) -> dict:
    """Get the complete health profile for a user."""

    _ = kwargs
    profile = await get_profile_dict(user_id, db)
    return profile or {"error": f"No profile found for user {user_id}"}


async def get_weather(user_id: str, db: Any, **kwargs: Any) -> dict:
    """Fetch current weather or return Bangalore defaults."""

    _ = user_id, db, kwargs
    try:
        import httpx

        api_key = os.getenv("OPENWEATHERMAP_API_KEY", "")
        if not api_key:
            raise ValueError("Missing key")
        async with httpx.AsyncClient() as client:
            weather_resp = await client.get(
                "https://api.openweathermap.org/data/2.5/weather",
                params={"lat": 12.9716, "lon": 77.5946, "appid": api_key, "units": "metric"},
                timeout=5,
            )
            weather_data = weather_resp.json()
            result = {
                "temp_c": weather_data["main"]["temp"],
                "humidity_pct": weather_data["main"]["humidity"],
                "description": weather_data.get("weather", [{}])[0].get("description", "Unknown"),
                "wind_speed_mps": weather_data.get("wind", {}).get("speed", 0),
                "aqi": 85,
                "uv_index": 7,
            }
            return result
    except Exception:
        return {"temp_c": 28, "humidity_pct": 65, "aqi": 85, "uv_index": 7, "description": "Partly cloudy (cached)", "wind_speed_mps": 3}


async def get_nutrition_targets(user_id: str, db: Any, **kwargs: Any) -> dict:
    """Get blood-work-aware nutrition targets for the user."""

    _ = kwargs
    profile = await get_profile_dict(user_id, db)
    from backend.formulas import nutrition_targets

    return nutrition_targets(profile or {})


async def get_recent_meals(user_id: str, db: Any, days: int = 3, **kwargs: Any) -> dict:
    """Get recent meals and aggregate daily totals."""

    _ = kwargs
    meals = await get_recent_meals_db(user_id, days, db)
    daily_totals: dict[str, Any] = defaultdict(lambda: {"calories": 0, "protein_g": 0, "carbs_g": 0, "fat_g": 0, "sat_fat_g": 0, "fiber_g": 0, "meal_count": 0})
    for meal in meals:
        bucket = daily_totals[meal["date"]]
        for key in ("calories", "protein_g", "carbs_g", "fat_g", "sat_fat_g", "fiber_g"):
            bucket[key] += meal["nutrition"].get(key, 0)
        bucket["meal_count"] += 1
    return {"meals": meals, "daily_totals": dict(daily_totals)}


async def get_workout_targets(user_id: str, db: Any, **kwargs: Any) -> dict:
    """Get profile-aware workout recommendations."""

    _ = kwargs
    profile = await get_profile_dict(user_id, db)
    from backend.formulas import workout_targets

    return workout_targets(profile or {})


async def rank_impact(user_id: str, db: Any, **kwargs: Any) -> dict:
    """Rank possible health improvements by bio age impact."""

    _ = kwargs
    profile = await get_profile_dict(user_id, db)
    from backend.formulas import rank_impact

    return rank_impact(profile or {})


async def get_reminders(user_id: str, db: Any, **kwargs: Any) -> dict:
    """Get pending reminders."""

    _ = kwargs
    from backend.reminder_engine import check_reminders

    return {"reminders": await check_reminders(user_id, db)}


async def check_specialists(user_id: str, db: Any, **kwargs: Any) -> dict:
    """Check if specialist consultations are recommended."""

    _ = kwargs
    profile = await get_profile_dict(user_id, db)
    from backend.specialists import check_specialists as cs

    return {"specialists": cs(profile or {})}
