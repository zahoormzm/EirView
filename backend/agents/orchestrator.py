from __future__ import annotations

NAME: str = "orchestrator"

SYSTEM_PROMPT: str = """You are the EirView orchestrator. Route health inputs to specialist agents.

ROUTING RULES:
- For file uploads (blood PDF, Cult.fit image, Apple Health XML) -> call_collector
- After new data is ingested -> call_mirror then call_coach
- For habit change simulations -> call_time_machine
- For mood questions or emotional check-ins -> call_mental_health
- For general health questions -> call_coach

Always explain which agents you are calling and why."""

TOOLS: list[dict] = [
    {"name": "call_collector", "description": "Parse and validate health data uploads.", "input_schema": {"type": "object", "properties": {"data_type": {"type": "string"}, "content": {"type": "string"}}, "required": ["data_type", "content"]}},
    {"name": "call_mirror", "description": "Calculate biological age and explanation.", "input_schema": {"type": "object", "properties": {"user_id": {"type": "string"}}, "required": ["user_id"]}},
    {"name": "call_time_machine", "description": "Project future health risks.", "input_schema": {"type": "object", "properties": {"user_id": {"type": "string"}, "changes": {"type": "object"}}, "required": ["user_id"]}},
    {"name": "call_coach", "description": "Generate recommendations.", "input_schema": {"type": "object", "properties": {"user_id": {"type": "string"}}, "required": ["user_id"]}},
    {"name": "call_mental_health", "description": "Assess mental wellness through conversation.", "input_schema": {"type": "object", "properties": {"user_id": {"type": "string"}, "message": {"type": "string"}}, "required": ["user_id", "message"]}},
]
