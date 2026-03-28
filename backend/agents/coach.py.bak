from __future__ import annotations

NAME: str = "coach"

SYSTEM_PROMPT: str = """You generate personalized, practical health recommendations for EirView.

Use current health data, weather, meals, reminders, specialists, and workout targets to produce ranked, specific suggestions that are realistic and encouraging."""

TOOLS: list[dict] = [
    {"name": "get_profile", "description": "Get the full health profile.", "input_schema": {"type": "object", "properties": {}}},
    {"name": "get_weather", "description": "Get current weather and AQI.", "input_schema": {"type": "object", "properties": {}}},
    {"name": "get_nutrition_targets", "description": "Get personalized daily nutrition targets.", "input_schema": {"type": "object", "properties": {}}},
    {"name": "get_recent_meals", "description": "Get recent meals.", "input_schema": {"type": "object", "properties": {"days": {"type": "integer"}}}},
    {"name": "rank_impact", "description": "Rank possible improvements by bio age impact.", "input_schema": {"type": "object", "properties": {}}},
    {"name": "get_workout_targets", "description": "Get workout recommendations.", "input_schema": {"type": "object", "properties": {}}},
    {"name": "score_meal", "description": "Score a meal against profile-aware targets.", "input_schema": {"type": "object", "properties": {"meal": {"type": "object"}}, "required": ["meal"]}},
    {"name": "get_reminders", "description": "Get pending reminders.", "input_schema": {"type": "object", "properties": {}}},
    {"name": "check_specialists", "description": "Check specialist needs.", "input_schema": {"type": "object", "properties": {}}},
]
