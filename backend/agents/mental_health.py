from __future__ import annotations

NAME: str = "mental_health"

SYSTEM_PROMPT: str = """You assess mental wellness through empathetic conversation for EirView.

Use the user's health profile, mood signals, and recent habits to respond warmly, safely, and concretely. Escalate gently toward professional support if severe distress is suggested."""

TOOLS: list[dict] = [
    {"name": "get_profile", "description": "Get relevant biological and behavioral mental-health context.", "input_schema": {"type": "object", "properties": {}}},
    {"name": "mental_wellness_score", "description": "Calculate the mental wellness score.", "input_schema": {"type": "object", "properties": {}}},
    {"name": "get_recent_meals", "description": "Check recent meals for emotional eating patterns.", "input_schema": {"type": "object", "properties": {"days": {"type": "integer"}}}},
    {"name": "get_spotify_mood", "description": "Get Spotify mood trend data.", "input_schema": {"type": "object", "properties": {}}},
    {"name": "get_cross_signals", "description": "Get cross-domain mood signals.", "input_schema": {"type": "object", "properties": {}}},
    {"name": "update_profile", "description": "Persist mental wellness updates.", "input_schema": {"type": "object", "properties": {"updates": {"type": "object"}}, "required": ["updates"]}},
]
