from __future__ import annotations

NAME: str = "collector"

SYSTEM_PROMPT: str = """You parse and validate health data from various sources for EirView.

Parse uploads, validate extracted values, update the profile, and note anomalies or cross-domain concerns."""

TOOLS: list[dict] = [
    {"name": "parse_blood_pdf", "description": "Extract blood report lab values.", "input_schema": {"type": "object", "properties": {"file_path": {"type": "string"}}, "required": ["file_path"]}},
    {"name": "parse_cultfit_image", "description": "Extract body composition from Cult.fit screenshots.", "input_schema": {"type": "object", "properties": {"file_path": {"type": "string"}}, "required": ["file_path"]}},
    {"name": "parse_apple_health_xml", "description": "Extract Apple Health metrics from export.xml.", "input_schema": {"type": "object", "properties": {"file_path": {"type": "string"}}, "required": ["file_path"]}},
    {"name": "validate_ranges", "description": "Validate values against reference ranges.", "input_schema": {"type": "object", "properties": {"values": {"type": "object"}}, "required": ["values"]}},
    {"name": "update_profile", "description": "Update the user's profile with extracted values.", "input_schema": {"type": "object", "properties": {"updates": {"type": "object"}}, "required": ["updates"]}},
]
