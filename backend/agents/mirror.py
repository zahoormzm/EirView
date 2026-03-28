from __future__ import annotations

NAME: str = "mirror"

SYSTEM_PROMPT: str = """You analyze biological age for EirView and explain it warmly.

Retrieve profile data, calculate biological age across subsystems, compare face age and device age when present, and write a motivating narrative grounded in real metrics."""

TOOLS: list[dict] = [
    {"name": "calculate_bio_age", "description": "Calculate bio age and subsystem breakdown.", "input_schema": {"type": "object", "properties": {}}},
    {"name": "get_profile", "description": "Get the full user profile.", "input_schema": {"type": "object", "properties": {}}},
]
