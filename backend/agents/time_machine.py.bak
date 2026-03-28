from __future__ import annotations

NAME: str = "time_machine"

SYSTEM_PROMPT: str = """You project health futures for EirView.

Show current risk trajectory, compare it with a proposed change, and describe the most meaningful long-term difference in a motivating, concrete way."""

TOOLS: list[dict] = [
    {"name": "project_risk", "description": "Project health risks over N years.", "input_schema": {"type": "object", "properties": {"years": {"type": "integer"}}}},
    {"name": "simulate_habit_change", "description": "Simulate a proposed habit change.", "input_schema": {"type": "object", "properties": {"changes": {"type": "object"}}, "required": ["changes"]}},
    {"name": "get_profile", "description": "Get the current user profile.", "input_schema": {"type": "object", "properties": {}}},
]
