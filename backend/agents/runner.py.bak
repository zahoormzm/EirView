from __future__ import annotations

import json
import time
from datetime import datetime
from typing import Any, AsyncGenerator


MAX_AGENT_ITERATIONS: int = 6


def _truncate_payload(input_data: dict[str, Any]) -> dict[str, Any]:
    """Trim long chat histories and oversized text before sending to the model."""

    payload = dict(input_data)
    history = payload.get("history")
    if isinstance(history, list):
        payload["history"] = history[-6:]
    message = payload.get("message")
    if isinstance(message, str):
        payload["message"] = message[-1200:]
    return payload


async def run_agent(agent_module: Any, user_id: str, input_data: dict[str, Any], db: Any) -> dict[str, Any]:
    """Run a bounded Anthropic-style tool-use loop or deterministic fallback."""

    from backend.ai_router import ai_router

    messages: list[dict[str, Any]] = [{"role": "user", "content": json.dumps(_truncate_payload(input_data))}]
    all_traces: list[dict[str, Any]] = []
    total_tokens_in = 0
    total_tokens_out = 0
    for _ in range(MAX_AGENT_ITERATIONS):
        start = time.time()
        response = ai_router._call_claude(
            system=agent_module.SYSTEM_PROMPT,
            messages=messages,
            tools=getattr(agent_module, "TOOLS", None),
            max_tokens=ai_router.default_max_tokens,
        )
        latency = int((time.time() - start) * 1000)
        usage = getattr(response, "usage", None)
        total_tokens_in += int(getattr(usage, "input_tokens", 0))
        total_tokens_out += int(getattr(usage, "output_tokens", 0))
        await db.execute(
            "INSERT INTO agent_logs (user_id, agent_name, action, tokens_in, tokens_out, latency_ms, model) VALUES (?,?,?,?,?,?,?)",
            (user_id, agent_module.NAME, "tool_use_round", getattr(usage, "input_tokens", 0), getattr(usage, "output_tokens", 0), latency, ai_router.claude_model),
        )
        await db.commit()
        if getattr(response, "stop_reason", "end_turn") == "end_turn":
            text = "".join(getattr(block, "text", "") for block in getattr(response, "content", []))
            return {"result": text, "traces": all_traces, "tokens_in": total_tokens_in, "tokens_out": total_tokens_out}
        tool_results: list[dict[str, Any]] = []
        for block in getattr(response, "content", []):
            if getattr(block, "type", "") != "tool_use":
                continue
            result = await execute_tool(block.name, block.input, user_id, db)
            trace = {"agent": agent_module.NAME, "tool": block.name, "input": block.input, "output": result, "timestamp": datetime.now().isoformat()}
            all_traces.append(trace)
            await db.execute(
                "INSERT INTO agent_logs (user_id, agent_name, action, tool_name, tool_input, tool_output, model) VALUES (?,?,?,?,?,?,?)",
                (user_id, agent_module.NAME, "tool_call", block.name, json.dumps(block.input), json.dumps(result), ai_router.claude_model),
            )
            await db.commit()
            tool_results.append({"type": "tool_result", "tool_use_id": block.id, "content": json.dumps(result)})
        messages.append({"role": "assistant", "content": getattr(response, "content", [])})
        messages.append({"role": "user", "content": tool_results})
    return {"result": "Agent reached max iterations", "traces": all_traces, "tokens_in": total_tokens_in, "tokens_out": total_tokens_out}


async def stream_agent(agent_module: Any, user_id: str, input_data: dict[str, Any], db: Any) -> AsyncGenerator[str, None]:
    """Stream an agent response as SSE."""

    from backend.ai_router import ai_router

    messages: list[dict[str, Any]] = [{"role": "user", "content": json.dumps(_truncate_payload(input_data))}]
    for _ in range(MAX_AGENT_ITERATIONS):
        with ai_router.stream_claude(
            system=agent_module.SYSTEM_PROMPT,
            messages=messages,
            tools=getattr(agent_module, "TOOLS", None),
            max_tokens=ai_router.chat_max_tokens,
        ) as stream:
            for event in stream:
                if getattr(event, "type", "") == "content_block_delta" and hasattr(event, "delta") and hasattr(event.delta, "text"):
                    yield f"data: {json.dumps({'type': 'text', 'content': event.delta.text})}\n\n"
            response = stream.get_final_message()
        usage = getattr(response, "usage", None)
        await db.execute(
            "INSERT INTO agent_logs (user_id, agent_name, action, tokens_in, tokens_out, model) VALUES (?,?,?,?,?,?)",
            (user_id, agent_module.NAME, "stream_round", getattr(usage, "input_tokens", 0), getattr(usage, "output_tokens", 0), ai_router.claude_model),
        )
        await db.commit()
        if getattr(response, "stop_reason", "end_turn") == "end_turn":
            yield f"data: {json.dumps({'type': 'done'})}\n\n"
            return
        tool_results: list[dict[str, Any]] = []
        for block in getattr(response, "content", []):
            if getattr(block, "type", "") != "tool_use":
                continue
            result = await execute_tool(block.name, block.input, user_id, db)
            yield f"data: {json.dumps({'type': 'tool', 'name': block.name, 'result': result})}\n\n"
            tool_results.append({"type": "tool_result", "tool_use_id": block.id, "content": json.dumps(result)})
        messages.append({"role": "assistant", "content": getattr(response, "content", [])})
        messages.append({"role": "user", "content": tool_results})
    yield f"data: {json.dumps({'type': 'done'})}\n\n"


async def execute_tool(tool_name: str, tool_input: dict[str, Any], user_id: str, db: Any) -> dict[str, Any]:
    """Route tool calls to actual implementations."""

    from backend.tools import calculation_tools, context_tools, data_tools, spotify_tools

    registry: dict[str, Any] = {
        "calculate_bio_age": calculation_tools.calculate_bio_age,
        "project_risk": calculation_tools.project_risk,
        "simulate_habit_change": calculation_tools.simulate_habit_change,
        "mental_wellness_score": calculation_tools.mental_wellness_score,
        "nutrition_targets": calculation_tools.nutrition_targets,
        "score_meal": calculation_tools.score_meal,
        "workout_targets": calculation_tools.workout_targets,
        "parse_blood_pdf": data_tools.parse_blood_pdf,
        "parse_cultfit_image": data_tools.parse_cultfit_image,
        "parse_apple_health_xml": data_tools.parse_apple_health_xml,
        "validate_ranges": data_tools.validate_ranges,
        "update_profile": data_tools.update_profile,
        "get_profile": context_tools.get_profile,
        "get_weather": context_tools.get_weather,
        "get_nutrition_targets": context_tools.get_nutrition_targets,
        "get_recent_meals": context_tools.get_recent_meals,
        "get_workout_targets": context_tools.get_workout_targets,
        "rank_impact": context_tools.rank_impact,
        "get_reminders": context_tools.get_reminders,
        "check_specialists": context_tools.check_specialists,
        "get_spotify_mood": spotify_tools.get_spotify_mood,
        "get_cross_signals": spotify_tools.get_cross_signals,
    }
    handler = registry.get(tool_name)
    if handler is None:
        return {"error": f"Unknown tool: {tool_name}"}
    return await handler(user_id=user_id, db=db, **tool_input)
