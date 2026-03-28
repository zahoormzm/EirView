from __future__ import annotations

import base64
import json
import os
import re
from collections import defaultdict
from datetime import datetime, timedelta
from typing import Any

from backend.database import get_profile_dict

LAB_ALIASES: dict[str, list[str]] = {
    "ldl": ["ldl", "ldl cholesterol", "low density lipoprotein"],
    "hdl": ["hdl", "hdl cholesterol", "high density lipoprotein"],
    "triglycerides": ["triglycerides", "triglyceride"],
    "total_cholesterol": ["total cholesterol", "cholesterol total"],
    "vitamin_d": ["vitamin d", "25 oh vitamin d", "25-oh vitamin d", "25 hydroxy vitamin d"],
    "b12": ["vitamin b12", "b12", "cobalamin"],
    "tsh": ["tsh", "thyroid stimulating hormone"],
    "ferritin": ["ferritin", "iron stores"],
    "fasting_glucose": ["fasting glucose", "glucose fasting", "glucose"],
    "hba1c": ["hba1c", "hb a1c", "glycated hemoglobin", "hemoglobin a1c"],
    "hemoglobin": ["hemoglobin", "haemoglobin", "hb"],
    "creatinine": ["creatinine", "serum creatinine"],
    "sgpt_alt": ["sgpt", "alt", "alanine aminotransferase", "alanine transaminase"],
    "sgot_ast": ["sgot", "ast", "aspartate aminotransferase", "aspartate transaminase"],
}

COMMON_LAB_FIELDS: list[str] = [
    "ldl",
    "hdl",
    "triglycerides",
    "total_cholesterol",
    "fasting_glucose",
    "hba1c",
    "vitamin_d",
    "b12",
    "tsh",
    "ferritin",
    "hemoglobin",
    "creatinine",
    "sgpt_alt",
    "sgot_ast",
]


def _extract_json_blob(text: str) -> Any | None:
    text = (text or "").strip()
    if not text:
        return None
    candidates = [text]
    object_match = re.search(r"\{.*\}", text, re.DOTALL)
    array_match = re.search(r"\[.*\]", text, re.DOTALL)
    if object_match:
        candidates.append(object_match.group())
    if array_match:
        candidates.append(array_match.group())
    for candidate in candidates:
        try:
            return json.loads(candidate)
        except json.JSONDecodeError:
            continue
    return None


def _normalize_lab_name(name: str) -> str | None:
    cleaned = re.sub(r"[^a-z0-9]+", " ", (name or "").lower()).strip()
    if not cleaned:
        return None
    for metric, aliases in LAB_ALIASES.items():
        if cleaned == metric:
            return metric
        if any(alias in cleaned for alias in aliases):
            return metric
    return None


def _extract_numeric_value(value: Any) -> float | None:
    if value in (None, ""):
        return None
    if isinstance(value, (int, float)):
        return float(value)
    match = re.search(r"-?\d+(?:\.\d+)?", str(value))
    return float(match.group()) if match else None


def _coerce_tests(payload: Any) -> tuple[list[dict[str, Any]], dict[str, Any]]:
    metadata: dict[str, Any] = {}
    if isinstance(payload, dict):
        metadata = {key: value for key, value in payload.items() if key != "tests"}
        if isinstance(payload.get("tests"), list):
            return [item for item in payload["tests"] if isinstance(item, dict)], metadata
        rows: list[dict[str, Any]] = []
        for key, value in payload.items():
            if key == "tests":
                continue
            if isinstance(value, dict):
                row = {"name": value.get("name") or key, **value}
            else:
                row = {"name": key, "value": value}
            rows.append(row)
        return rows, metadata
    if isinstance(payload, list):
        return [item if isinstance(item, dict) else {"name": str(item), "value": None} for item in payload], metadata
    return [], metadata


def _fallback_extract_tests_from_text(text: str) -> list[dict[str, Any]]:
    tests: list[dict[str, Any]] = []
    seen: set[tuple[str, float | None]] = set()
    for line in [segment.strip() for segment in text.splitlines() if segment.strip()]:
        metric = _normalize_lab_name(line)
        value = _extract_numeric_value(line)
        if metric is None or value is None:
            continue
        key = (metric, value)
        if key in seen:
            continue
        seen.add(key)
        unit_match = re.search(r"(mg/dL|g/dL|ng/mL|pg/mL|mIU/L|U/L|IU/L|%)", line, re.IGNORECASE)
        tests.append(
            {
                "name": metric,
                "value": value,
                "unit": unit_match.group(1) if unit_match else None,
                "reference_range": None,
                "flag": None,
                "source": "fallback_text",
            }
        )
    return tests


def _normalize_lab_payload(payload: Any, fallback_text: str = "") -> dict[str, Any]:
    tests, metadata = _coerce_tests(payload)
    if not tests and fallback_text:
        tests = _fallback_extract_tests_from_text(fallback_text)
    normalized_tests: list[dict[str, Any]] = []
    recognized_fields: dict[str, float | str | None] = {}
    unmapped_tests: list[dict[str, Any]] = []
    for row in tests:
        name = row.get("name") or row.get("test") or row.get("analyte") or row.get("marker") or "Unknown test"
        metric = _normalize_lab_name(str(name))
        value = _extract_numeric_value(row.get("value"))
        test_entry = {
            "name": str(name),
            "metric": metric,
            "value": value,
            "unit": row.get("unit") or row.get("units"),
            "reference_range": row.get("reference_range") or row.get("reference") or row.get("range"),
            "flag": row.get("flag") or row.get("status") or row.get("interpretation"),
        }
        normalized_tests.append(test_entry)
        if metric:
            if value is not None:
                recognized_fields[metric] = value
        else:
            unmapped_tests.append(test_entry)
    if normalized_tests:
        recognized_fields["last_blood_report_date"] = datetime.now().date().isoformat()
    missing_common_tests = [field for field in COMMON_LAB_FIELDS if field not in recognized_fields]
    return {
        "profile_updates": recognized_fields,
        "recognized_fields": {key: value for key, value in recognized_fields.items() if key != "last_blood_report_date"},
        "lab_tests": normalized_tests,
        "unmapped_tests": unmapped_tests,
        "missing_common_tests": missing_common_tests,
        "source_summary": {
            "tests_found": len(normalized_tests),
            "recognized_count": len([key for key in recognized_fields if key != "last_blood_report_date"]),
            "unmapped_count": len(unmapped_tests),
            "report_date": metadata.get("report_date") or metadata.get("collected_at"),
            "lab_name": metadata.get("lab_name") or metadata.get("laboratory"),
        },
    }


async def parse_blood_pdf(file_path: str, user_id: str, db: Any) -> dict:
    """Extract a flexible lab panel from a blood report PDF and normalize known metrics."""

    _ = user_id, db
    pdf_bytes = b""
    try:
        from backend.ai_router import ai_router

        with open(file_path, "rb") as handle:
            pdf_bytes = handle.read()
        b64 = base64.b64encode(pdf_bytes).decode()
        response = ai_router._call_claude(
            system=(
                "Extract every blood/lab test present in the uploaded report. "
                "Return strict JSON only with this shape: "
                "{\"tests\": [{\"name\": str, \"value\": number|null, \"unit\": str|null, "
                "\"reference_range\": str|null, \"flag\": str|null}], "
                "\"report_date\": str|null, \"lab_name\": str|null}. "
                "Do not invent tests that are not present. If the report is partial, return only the tests shown."
            ),
            messages=[
                {
                    "role": "user",
                    "content": [
                        {"type": "document", "source": {"type": "base64", "media_type": "application/pdf", "data": b64}},
                        {"type": "text", "text": "Extract all visible lab tests. Partial panels are valid. Include unknown tests in the tests array too."},
                    ],
                }
            ],
            tools=None,
            max_tokens=ai_router.extraction_max_tokens,
        )
        text = "".join(getattr(block, "text", "") for block in getattr(response, "content", []))
        payload = _extract_json_blob(text)
        if payload is not None:
            return _normalize_lab_payload(payload, fallback_text=pdf_bytes.decode("latin-1", errors="ignore"))
    except Exception:
        pass
    if not pdf_bytes and os.path.exists(file_path):
        with open(file_path, "rb") as handle:
            pdf_bytes = handle.read()
    return _normalize_lab_payload({}, fallback_text=pdf_bytes.decode("latin-1", errors="ignore"))


async def parse_cultfit_image(file_path: str, user_id: str, db: Any) -> dict:
    """Extract body composition from a Cult.fit image using Gemini or fallback."""

    _ = user_id, db
    try:
        from backend.ai_router import ai_router

        with open(file_path, "rb") as handle:
            image_bytes = handle.read()
        response = await ai_router.route(
            task="collector_cultfit",
            system="Extract body composition values and return strict JSON.",
            messages=[{"role": "user", "content": "Extract all values."}],
            image=image_bytes,
        )
        text = getattr(response, "text", "") or "".join(getattr(block, "text", "") for block in getattr(response, "content", []))
        match = re.search(r"\{.*\}", text, re.DOTALL)
        if match:
            return json.loads(match.group())
    except Exception:
        pass
    return {"weight_kg": None, "bmi": None, "bmr": None, "body_fat_pct": None, "visceral_fat_kg": None, "muscle_mass_kg": None, "body_water_pct": None, "protein_kg": None, "bone_mass_kg": None, "body_age_device": None}


async def analyze_meal_photo(image_bytes: bytes, user_id: str, db: Any) -> dict:
    """Analyze a meal photo with Gemini identification and USDA grounding when possible."""

    from backend.formulas import nutrition_targets

    items = [{"item": "Detected meal", "portion_g": 300}]
    try:
        from backend.ai_router import ai_router

        response = await ai_router.route(
            task="collector_meal_photo",
            system="Identify visible foods and estimated portions as strict JSON array.",
            messages=[{"role": "user", "content": "Analyze this meal."}],
            image=image_bytes,
        )
        text = getattr(response, "text", "") or "".join(getattr(block, "text", "") for block in getattr(response, "content", []))
        match = re.search(r"\[.*\]", text, re.DOTALL)
        if match:
            items = json.loads(match.group())
    except Exception:
        pass
    total = {"calories": 0.0, "protein_g": 0.0, "carbs_g": 0.0, "fat_g": 0.0, "sat_fat_g": 0.0, "fiber_g": 0.0}
    item_details: list[dict[str, Any]] = []
    try:
        import httpx

        async with httpx.AsyncClient() as client:
            for item in items:
                item_name = item.get("item", "food")
                portion_g = float(item.get("portion_g", 100))
                cached = await (await db.execute("SELECT * FROM usda_foods WHERE description LIKE ? LIMIT 1", (f"%{item_name}%",))).fetchone()
                usda = dict(cached) if cached else None
                if usda is None:
                    resp = await client.get(
                        "https://api.nal.usda.gov/fdc/v1/foods/search",
                        params={"query": item_name, "api_key": os.getenv("USDA_API_KEY", "DEMO_KEY"), "pageSize": 1},
                        timeout=5,
                    )
                    foods = resp.json().get("foods", [])
                    if not foods:
                        continue
                    food = foods[0]
                    nutrients = {n["nutrientName"]: n.get("value", 0) for n in food.get("foodNutrients", [])}
                    usda = {
                        "fdc_id": food["fdcId"],
                        "description": food["description"],
                        "calories_per_100g": nutrients.get("Energy", 0),
                        "protein_per_100g": nutrients.get("Protein", 0),
                        "fat_per_100g": nutrients.get("Total lipid (fat)", 0),
                        "carbs_per_100g": nutrients.get("Carbohydrate, by difference", 0),
                        "sat_fat_per_100g": nutrients.get("Fatty acids, total saturated", 0),
                        "fiber_per_100g": nutrients.get("Fiber, total dietary", 0),
                    }
                    await db.execute(
                        "INSERT OR REPLACE INTO usda_foods (fdc_id, description, calories_per_100g, protein_per_100g, fat_per_100g, carbs_per_100g, sat_fat_per_100g, fiber_per_100g) VALUES (?,?,?,?,?,?,?,?)",
                        (usda["fdc_id"], usda["description"], usda["calories_per_100g"], usda["protein_per_100g"], usda["fat_per_100g"], usda["carbs_per_100g"], usda["sat_fat_per_100g"], usda["fiber_per_100g"]),
                    )
                    await db.commit()
                scale = portion_g / 100
                detail = {"item": item_name, "portion_g": portion_g, "usda_id": usda.get("fdc_id"), "usda_description": usda.get("description")}
                mapping = [("calories", "calories_per_100g"), ("protein_g", "protein_per_100g"), ("fat_g", "fat_per_100g"), ("carbs_g", "carbs_per_100g"), ("sat_fat_g", "sat_fat_per_100g"), ("fiber_g", "fiber_per_100g")]
                for key, usda_key in mapping:
                    value = round(float(usda.get(usda_key, 0) or 0) * scale, 1)
                    detail[key] = value
                    total[key] = round(total[key] + value, 1)
                item_details.append(detail)
    except Exception:
        item_details = [{"item": "Detected meal", "portion_g": 300, "calories": 450, "protein_g": 18, "carbs_g": 55, "fat_g": 16, "sat_fat_g": 5, "fiber_g": 6, "usda_id": None, "usda_description": "Fallback estimate"}]
        total = {"calories": 450, "protein_g": 18, "carbs_g": 55, "fat_g": 16, "sat_fat_g": 5, "fiber_g": 6}
    profile = await get_profile_dict(user_id, db) or {}
    targets = nutrition_targets(profile)
    flags: list[str] = []
    if total["sat_fat_g"] > targets.get("sat_fat_g", 13):
        flags.append(f"Saturated fat {total['sat_fat_g']}g exceeds your {targets.get('sat_fat_g', 13)}g target.")
    if total["calories"] > targets.get("calories_per_meal", 700):
        flags.append("Calories are above your target for one meal.")
    if total["fiber_g"] < 5:
        flags.append("Fiber is low for this meal.")
    return {"items": item_details, "total": total, "flags": flags, "grounding": "USDA FoodData Central"}


def parse_apple_health_xml(file_path: str) -> dict:
    """Parse Apple Health export.xml using streaming iterparse."""

    import xml.etree.ElementTree as et

    now = datetime.now()
    week_ago = now - timedelta(days=7)
    metrics: dict[str, list[float]] = defaultdict(list)
    sleep_samples: list[dict[str, Any]] = []
    workouts: list[dict[str, Any]] = []
    type_map = {
        "HKQuantityTypeIdentifierRestingHeartRate": "resting_hr",
        "HKQuantityTypeIdentifierHeartRateVariabilitySDNN": "hrv_ms",
        "HKQuantityTypeIdentifierStepCount": "steps",
        "HKQuantityTypeIdentifierActiveEnergyBurned": "active_energy_kcal",
        "HKQuantityTypeIdentifierAppleExerciseTime": "exercise_min",
        "HKQuantityTypeIdentifierVO2Max": "vo2max",
        "HKQuantityTypeIdentifierRespiratoryRate": "respiratory_rate",
        "HKQuantityTypeIdentifierWalkingAsymmetryPercentage": "walking_asymmetry_pct",
        "HKQuantityTypeIdentifierFlightsClimbed": "flights_climbed",
        "HKQuantityTypeIdentifierOxygenSaturation": "blood_oxygen_pct",
    }
    for _, elem in et.iterparse(file_path, events=("end",)):
        if elem.tag == "Record":
            try:
                start_dt = datetime.strptime((elem.get("startDate", "") or "")[:19], "%Y-%m-%d %H:%M:%S")
            except ValueError:
                elem.clear()
                continue
            if start_dt < week_ago:
                elem.clear()
                continue
            record_type = elem.get("type", "")
            if record_type in type_map:
                try:
                    metrics[type_map[record_type]].append(float(elem.get("value", 0)))
                except ValueError:
                    pass
            if record_type == "HKCategoryTypeIdentifierSleepAnalysis":
                sleep_samples.append({"startDate": elem.get("startDate", ""), "endDate": elem.get("endDate", ""), "value": elem.get("value", "")})
            elem.clear()
        elif elem.tag == "Workout":
            try:
                start_dt = datetime.strptime((elem.get("startDate", "") or "")[:19], "%Y-%m-%d %H:%M:%S")
                if start_dt >= week_ago:
                    workouts.append({"type": (elem.get("workoutActivityType", "") or "").replace("HKWorkoutActivityType", ""), "duration_min": round(float(elem.get("duration", 0))), "calories": round(float(elem.get("totalEnergyBurned", 0))), "date": start_dt.strftime("%Y-%m-%d")})
            except ValueError:
                pass
            elem.clear()
    result: dict[str, Any] = {}
    for key, values in metrics.items():
        if key in {"steps", "active_energy_kcal", "exercise_min", "flights_climbed"}:
            result[f"{key if key != 'steps' else 'steps'}_avg_7d"] = round(sum(values) / 7) if values else None
        else:
            result[key] = round(sum(values) / len(values), 1) if values else None
    total_sleep_seconds = 0.0
    sleep_nights = 0
    seen_dates: set[str] = set()
    for sample in sleep_samples:
        if "Asleep" not in sample.get("value", "") and "InBed" not in sample.get("value", ""):
            continue
        try:
            start_dt = datetime.strptime(sample["startDate"][:19], "%Y-%m-%d %H:%M:%S")
            end_dt = datetime.strptime(sample["endDate"][:19], "%Y-%m-%d %H:%M:%S")
        except ValueError:
            continue
        duration = (end_dt - start_dt).total_seconds()
        if duration > 0:
            total_sleep_seconds += duration
            date_key = start_dt.strftime("%Y-%m-%d")
            if date_key not in seen_dates:
                seen_dates.add(date_key)
                sleep_nights += 1
    result["sleep_hours"] = round(total_sleep_seconds / max(sleep_nights, 1) / 3600, 1) if sleep_nights else None
    result["workouts_7d"] = workouts
    return result
