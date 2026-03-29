from __future__ import annotations

from copy import deepcopy
from typing import Any


def _clamp(value: float, low: float, high: float) -> float:
    """Clamp a floating-point value to the provided range."""

    return max(low, min(high, value))


def _safe_ratio(numerator: float | None, denominator: float | None) -> float | None:
    """Return a ratio when both values exist and denominator is non-zero."""

    if numerator is None or denominator in (None, 0):
        return None
    return numerator / denominator


def _num(value: Any, default: float = 0.0) -> float:
    """Convert nullable or loosely typed numeric values into safe floats."""

    if value in (None, ""):
        return float(default)
    try:
        return float(value)
    except (TypeError, ValueError):
        return float(default)


def _positive_num(value: Any, default: float) -> float:
    """Return a positive numeric value or a safe default."""

    numeric = _num(value, default)
    return numeric if numeric > 0 else float(default)


def cardiovascular_delta(profile: dict[str, Any]) -> float:
    """Calculate cardiovascular age delta from profile data."""

    score: float = 0.0
    hdl = profile.get("hdl")
    if hdl is not None:
        score += 1.5 if hdl < 40 else -1.5 if hdl >= 60 else 0.0
    ldl = profile.get("ldl")
    if ldl is not None:
        score += -1.0 if ldl < 100 else 0.0 if ldl < 130 else 1.0 if ldl < 160 else 2.0
    triglycerides = profile.get("triglycerides")
    if triglycerides is not None:
        score += 0.0 if triglycerides < 150 else 0.5 if triglycerides < 200 else 1.5
    resting_hr = profile.get("resting_hr")
    if resting_hr is not None:
        score += -1.0 if resting_hr < 60 else 0.0 if resting_hr <= 72 else 0.5 if resting_hr <= 84 else 1.5
    hrv_ms = profile.get("hrv_ms")
    if hrv_ms is not None:
        score += -1.0 if hrv_ms >= 50 else 0.0 if hrv_ms >= 30 else 1.5
    vo2max = profile.get("vo2max")
    if vo2max is not None:
        score += -1.5 if vo2max >= 45 else -0.5 if vo2max >= 35 else 0.5 if vo2max >= 25 else 1.5
    steps_avg = profile.get("steps_avg_7d")
    if steps_avg is not None:
        score += -1.0 if steps_avg >= 10000 else -0.5 if steps_avg >= 7500 else 0.0 if steps_avg >= 5000 else 1.0
    exercise_min = profile.get("exercise_min")
    if exercise_min is not None:
        score += -1.0 if exercise_min >= 45 else -0.5 if exercise_min >= 30 else 0.0 if exercise_min >= 15 else 1.0
    systolic = profile.get("blood_pressure_systolic")
    if systolic is not None:
        score += -0.5 if systolic < 120 else 0.0 if systolic < 130 else 1.0 if systolic < 140 else 2.0
    return _clamp(score, -8.0, 8.0)


def metabolic_delta(profile: dict[str, Any]) -> float:
    """Calculate metabolic age delta from profile data."""

    score: float = 0.0
    bmi = profile.get("bmi")
    if bmi is not None:
        if bmi < 18.5:
            score += 0.5
        elif bmi < 23:
            score += -0.5
        elif bmi < 25:
            score += 0.0
        elif bmi < 30:
            score += 1.0
        else:
            score += 2.0
    visceral_fat = profile.get("visceral_fat_kg")
    if visceral_fat is not None:
        score += -0.5 if visceral_fat < 1 else 0.0 if visceral_fat <= 2 else 1.5
    fasting_glucose = profile.get("fasting_glucose")
    if fasting_glucose is not None:
        score += -0.5 if fasting_glucose < 85 else 0.0 if fasting_glucose < 100 else 1.5 if fasting_glucose < 126 else 3.0
    hba1c = profile.get("hba1c")
    if hba1c is not None:
        score += -0.5 if hba1c < 5.4 else 0.0 if hba1c < 5.7 else 1.5 if hba1c < 6.5 else 3.0
    vitamin_d = profile.get("vitamin_d")
    if vitamin_d is not None:
        score += -0.5 if vitamin_d >= 30 else 0.0 if vitamin_d >= 20 else 1.5
    b12 = profile.get("b12")
    if b12 is not None:
        score += -0.5 if b12 >= 300 else 0.0 if b12 >= 200 else 1.0
    tsh = profile.get("tsh")
    if tsh is not None:
        score += 0.0 if 0.5 <= tsh <= 4.0 else 1.0
    weight = profile.get("weight_kg")
    height = profile.get("height_cm")
    age = profile.get("age")
    sex = (profile.get("sex") or "").lower()
    bmr = profile.get("bmr")
    if all(value is not None for value in (weight, height, age, bmr)) and sex in {"male", "female"}:
        expected = 10 * float(weight) + 6.25 * float(height) - 5 * int(age) + (5 if sex == "male" else -161)
        if bmr > expected * 1.05:
            score += -0.5
        elif bmr < expected * 0.95:
            score += 0.5
    return _clamp(score, -8.0, 8.0)


def musculoskeletal_delta(profile: dict[str, Any]) -> float:
    """Calculate musculoskeletal age delta from profile data."""

    score: float = 0.0
    sex = (profile.get("sex") or "").lower()
    muscle_ratio = _safe_ratio(profile.get("muscle_mass_kg"), profile.get("weight_kg"))
    if muscle_ratio is not None and sex in {"male", "female"}:
        if sex == "male":
            score += -1.0 if muscle_ratio >= 0.40 else 0.0 if muscle_ratio >= 0.35 else 1.5
        else:
            score += -1.0 if muscle_ratio >= 0.32 else 0.0 if muscle_ratio >= 0.28 else 1.5
    bone_mass = profile.get("bone_mass_kg")
    if bone_mass is not None and sex in {"male", "female"}:
        if sex == "male":
            score += -0.5 if bone_mass >= 3.0 else 1.0 if bone_mass < 2.5 else 0.0
        else:
            score += -0.5 if bone_mass >= 2.5 else 1.0 if bone_mass < 2.0 else 0.0
    posture_score = profile.get("posture_score_pct")
    if posture_score is not None:
        score += -1.0 if posture_score >= 80 else 0.0 if posture_score >= 60 else 1.5
    asymmetry = profile.get("walking_asymmetry_pct")
    if asymmetry is not None:
        score += -0.5 if asymmetry < 3 else 0.0 if asymmetry <= 5 else 1.0
    return _clamp(score, -6.0, 6.0)


def neurological_delta(profile: dict[str, Any]) -> float:
    """Calculate neurological age delta from profile data."""

    score: float = 0.0
    sleep = profile.get("sleep_hours")
    if sleep is not None:
        score += -1.0 if 7 <= sleep <= 9 else 0.0 if sleep >= 6 else 1.5 if sleep < 6 else 0.5
    deep_sleep = profile.get("sleep_deep_pct")
    if deep_sleep is not None:
        score += -0.5 if deep_sleep >= 20 else 0.0 if deep_sleep >= 13 else 1.0
    phq9 = profile.get("phq9_score")
    if phq9 is not None:
        if phq9 <= 4:
            score += -0.5
        elif phq9 <= 9:
            score += 0.0
        elif phq9 <= 14:
            score += 1.0
        elif phq9 <= 19:
            score += 2.0
        else:
            score += 3.0
    stress = profile.get("stress_level")
    if stress is not None:
        score += -0.5 if stress <= 3 else 0.0 if stress <= 6 else 1.0 if stress <= 8 else 2.0
    screen = profile.get("screen_time_hours")
    if screen is not None:
        score += -0.5 if screen < 4 else 0.0 if screen <= 8 else 0.5 if screen <= 12 else 1.0
    exam_stress = profile.get("exam_stress")
    if exam_stress is not None:
        score += 0.0 if exam_stress <= 3 else 0.3 if exam_stress <= 6 else 0.7 if exam_stress <= 8 else 1.5
    study_hours = profile.get("study_hours_daily")
    if study_hours is not None:
        score += 0.0 if study_hours <= 6 else 0.3 if study_hours <= 10 else 1.0
    return _clamp(score, -6.0, 6.0)


def _calculate_bio_age_base(profile: dict[str, Any]) -> dict[str, Any]:
    """Calculate biological age values without secondary ranking lookups."""

    chrono = profile.get("age", profile.get("chronological_age", 25)) or 25
    cv = cardiovascular_delta(profile)
    met = metabolic_delta(profile)
    msk = musculoskeletal_delta(profile)
    neuro = neurological_delta(profile)
    overall = chrono + (0.30 * cv + 0.25 * met + 0.20 * msk + 0.25 * neuro)
    result = {
        "overall": round(overall, 1),
        "cardiovascular": round(chrono + cv, 1),
        "metabolic": round(chrono + met, 1),
        "musculoskeletal": round(chrono + msk, 1),
        "neurological": round(chrono + neuro, 1),
        "deltas": {
            "cv": round(cv, 2),
            "met": round(met, 2),
            "msk": round(msk, 2),
            "neuro": round(neuro, 2),
        },
    }
    result["overall_bio_age"] = result["overall"]
    result["sub_ages"] = {
        "cardiovascular": result["cardiovascular"],
        "metabolic": result["metabolic"],
        "musculoskeletal": result["musculoskeletal"],
        "neurological": result["neurological"],
    }
    result["delta"] = round(result["overall"] - chrono, 1)
    return result


def calculate_bio_age(profile: dict[str, Any]) -> dict[str, Any]:
    """Calculate biological age from health profile data."""

    result = _calculate_bio_age_base(profile)
    result["contributing_factors"] = rank_impact(profile)["top_changes"]
    return result


def project_risk(profile: dict[str, Any], years: int = 15) -> list[dict[str, Any]]:
    """Project health risks over future years using biomarker-based multipliers."""

    diabetes_base = 0.002
    cvd_base = 0.001
    metabolic_base = 0.002
    mental_base = 0.003
    fasting_glucose = _num(profile.get("fasting_glucose"))
    hba1c = _num(profile.get("hba1c"))
    bmi = _num(profile.get("bmi"))
    exercise_hours_week = _num(profile.get("exercise_hours_week"))
    ldl = _num(profile.get("ldl"))
    blood_pressure_systolic = _num(profile.get("blood_pressure_systolic"))
    hdl = _num(profile.get("hdl"), 999)
    visceral_fat_kg = _num(profile.get("visceral_fat_kg"))
    triglycerides = _num(profile.get("triglycerides"))
    phq9_score = _num(profile.get("phq9_score"))
    sleep_hours = _num(profile.get("sleep_hours"), 8)
    stress_level = _num(profile.get("stress_level"))
    vitamin_d = _num(profile.get("vitamin_d"), 30)
    exam_stress = _num(profile.get("exam_stress"))
    study_hours_daily = _num(profile.get("study_hours_daily"))
    diabetes_mult = 1.0
    if fasting_glucose > 100:
        diabetes_mult *= 2.5
    if hba1c > 5.7:
        diabetes_mult *= 2.0
    if bmi > 25:
        diabetes_mult *= 1.5
    if profile.get("family_diabetes"):
        diabetes_mult *= 2.0
    if exercise_hours_week < 2.5:
        diabetes_mult *= 1.3
    cvd_mult = 1.0
    if ldl > 130:
        cvd_mult *= 1.8
    if blood_pressure_systolic > 130:
        cvd_mult *= 1.5
    if hdl < 40:
        cvd_mult *= 1.5
    if profile.get("smoking") == "current":
        cvd_mult *= 2.5
    if profile.get("family_heart"):
        cvd_mult *= 1.8
    metabolic_mult = 1.0
    if bmi > 25:
        metabolic_mult *= 1.5
    if visceral_fat_kg > 2:
        metabolic_mult *= 1.5
    if triglycerides > 150:
        metabolic_mult *= 1.3
    mental_mult = 1.0
    if phq9_score > 10:
        mental_mult *= 2.0
    if sleep_hours < 6:
        mental_mult *= 1.5
    if stress_level > 7:
        mental_mult *= 1.3
    if vitamin_d < 20:
        mental_mult *= 1.3
    if profile.get("family_mental"):
        mental_mult *= 1.5
    if exam_stress > 7:
        mental_mult *= 1.3
    if study_hours_daily > 8 and sleep_hours < 6:
        mental_mult *= 1.4
    results: list[dict[str, Any]] = []
    for year in range(1, years + 1):
        results.append(
            {
                "year": year,
                "diabetes_risk": round(min(1 - (1 - diabetes_base * diabetes_mult) ** year, 0.95), 4),
                "cvd_risk": round(min(1 - (1 - cvd_base * cvd_mult) ** year, 0.95), 4),
                "metabolic_risk": round(min(1 - (1 - metabolic_base * metabolic_mult) ** year, 0.95), 4),
                "mental_decline_risk": round(min(1 - (1 - mental_base * mental_mult) ** year, 0.95), 4),
            }
        )
    return results


def mental_wellness_score(profile: dict[str, Any]) -> dict[str, Any]:
    """Calculate mental wellness score (0-100) with detailed breakdown."""

    score = 100.0
    penalties: dict[str, float] = {}
    phq9 = _num(profile.get("phq9_score"))
    penalties["phq9_penalty"] = round(min(phq9 * 3, 30), 1)
    sleep = _num(profile.get("sleep_hours"), 7.5)
    penalties["sleep_penalty"] = round(15 if sleep < 6 else (7 - sleep) * 15 if sleep < 7 else 0, 1)
    stress = _num(profile.get("stress_level"), 5)
    penalties["stress_penalty"] = round(min(max(0, (stress - 4) * 2.5), 15), 1)
    screen = _num(profile.get("screen_time_hours"), 6)
    penalties["screen_penalty"] = round(min(max(0, (screen - 6) * 1.67), 10), 1)
    exam_stress = _num(profile.get("exam_stress"))
    study_hrs = _num(profile.get("study_hours_daily"))
    academic_penalty = 0.0
    if exam_stress > 6:
        academic_penalty += (exam_stress - 6) * 1.5
    if study_hrs > 8:
        academic_penalty += min(study_hrs - 8, 2) * 2
    penalties["academic_penalty"] = round(min(academic_penalty, 10), 1)
    exercise = _num(profile.get("exercise_min"), 30)
    penalties["exercise_penalty"] = 10.0 if exercise < 15 else 5.0 if exercise < 30 else 0.0
    posture = _num(profile.get("posture_score_pct"), 70)
    penalties["posture_penalty"] = round(min(max(0, (60 - posture) / 12), 5), 1)
    vitd = _num(profile.get("vitamin_d"), 30)
    penalties["vitd_penalty"] = 10.0 if vitd and vitd < 20 else 5.0 if vitd and vitd < 30 else 0.0
    hrv = _num(profile.get("hrv_ms"), 40)
    penalties["hrv_penalty"] = 5.0 if hrv and hrv < 20 else 3.0 if hrv and hrv < 30 else 0.0
    for value in penalties.values():
        score -= value
    breakdown_list = [{"name": key.replace("_penalty", "").replace("_", " ").title(), "penalty": value} for key, value in penalties.items() if value > 0]
    return {"score": round(max(score, 0), 1), "breakdown": penalties, "breakdown_list": breakdown_list}


def nutrition_targets(profile: dict[str, Any]) -> dict[str, Any]:
    """Calculate personalized daily nutrition targets based on profile data."""

    weight = _positive_num(profile.get("weight_kg"), 70)
    bmr = _positive_num(profile.get("bmr"), round(weight * 30))
    calories = round(bmr * 1.4) if bmr else round(weight * 30)
    muscle_ratio = max(0.0, _num(profile.get("muscle_mass_kg")) / weight) if weight else 0
    protein_mult = 1.5 if muscle_ratio < 0.35 else 1.2
    protein_g = round(weight * protein_mult)
    ldl = _num(profile.get("ldl"), 100)
    sat_fat_g = 10 if ldl > 160 else 11 if ldl > 130 else 13 if ldl > 100 else 16
    fiber_g = 30
    temp = max(0.0, _num(profile.get("temperature_c"), 28))
    water_ml = round(weight * 35 + max(0, temp - 25) * 100)
    vitd_ug = 50 if _num(profile.get("vitamin_d"), 30) < 20 else 15
    b12_ug = 100 if _num(profile.get("b12"), 300) < 300 else 2.4
    fat_g = round(calories * 0.25 / 9)
    carbs_g = round((calories - protein_g * 4 - fat_g * 9) / 4)
    return {
        "calories": calories,
        "protein_g": protein_g,
        "carbs_g": carbs_g,
        "fat_g": fat_g,
        "sat_fat_g": sat_fat_g,
        "fiber_g": fiber_g,
        "water_ml": water_ml,
        "vitamin_d_ug": vitd_ug,
        "b12_ug": b12_ug,
        "calories_per_meal": round(calories / 3),
        "reasoning": [
            f"Sat fat limited to {sat_fat_g}g because LDL is {ldl} mg/dL.",
            f"Protein target set to {protein_g}g from weight and muscle ratio.",
        ],
    }


def simulate_habit_change(profile: dict[str, Any], changes: dict[str, Any]) -> dict[str, Any]:
    """Apply hypothetical lifestyle changes and recalculate bio age."""

    modified = {**profile}
    if "sleep" in changes:
        modified["sleep_hours"] = float(changes["sleep"])
    if "exercise" in changes:
        modified["exercise_hours_week"] = float(changes["exercise"])
        modified["exercise_min"] = int(float(changes["exercise"]) * 60 / 7)
    if "screen_time" in changes:
        modified["screen_time_hours"] = float(changes["screen_time"])
    if "stress" in changes:
        modified["stress_level"] = float(changes["stress"])
    if "exam_stress" in changes:
        modified["exam_stress"] = float(changes["exam_stress"])
    if "diet" in changes:
        modified["diet_quality"] = {1: "poor", 2: "average", 3: "good", 4: "excellent"}.get(int(changes["diet"]), "average")
    modified.update({key: value for key, value in changes.items() if key not in {"sleep", "exercise", "screen_time", "stress", "exam_stress", "diet"}})
    current = _calculate_bio_age_base(profile)
    projected = _calculate_bio_age_base(modified)
    return {
        "current": current,
        "projected": projected,
        "improvement": round(current["overall"] - projected["overall"], 1),
        "new_risk_projections": project_risk(modified),
    }


def score_meal(profile: dict[str, Any], meal: dict[str, Any]) -> dict[str, Any]:
    """Score a meal against personalized nutrition targets."""

    total = meal.get("total", meal)
    targets = nutrition_targets(profile)
    score = 100.0
    flags: list[str] = []
    sat_fat = float(total.get("sat_fat_g", 0) or 0)
    calories = float(total.get("calories", 0) or 0)
    fiber = float(total.get("fiber_g", 0) or 0)
    protein = float(total.get("protein_g", 0) or 0)
    if sat_fat > targets["sat_fat_g"]:
        score -= min(25.0, (sat_fat - targets["sat_fat_g"]) * 4)
        flags.append(f"Saturated fat is above your daily target ({sat_fat}g vs {targets['sat_fat_g']}g).")
    if calories > targets["calories_per_meal"] * 1.2:
        score -= min(20.0, (calories - targets["calories_per_meal"]) / 20)
        flags.append("Calories are heavy for a single meal.")
    if fiber < 5:
        score -= 10
        flags.append("Fiber is low for this meal.")
    if protein < max(15, targets["protein_g"] / 4):
        score -= 8
        flags.append("Protein is lower than ideal.")
    if _num(profile.get("fasting_glucose")) > 100 and float(total.get("carbs_g", 0) or 0) > 60:
        score -= 12
        flags.append("High carbohydrate load for elevated fasting glucose.")
    suggestions: list[str] = []
    if fiber < 5:
        suggestions.append("Add vegetables, legumes, or fruit for fiber.")
    if protein < max(15, targets["protein_g"] / 4):
        suggestions.append("Add a lean protein source.")
    if sat_fat > targets["sat_fat_g"]:
        suggestions.append("Swap fried or creamy items for lower saturated fat options.")
    return {"score": round(max(score, 0), 1), "flags": flags, "suggestions": suggestions, "targets": targets}


def workout_targets(profile: dict[str, Any]) -> dict[str, Any]:
    """Generate profile-aware weekly workout recommendations."""

    bio = _calculate_bio_age_base(profile)
    chrono = profile.get("age", profile.get("chronological_age", 25)) or 25
    recommended_sessions: list[dict[str, Any]] = [
        {"type": "walking", "frequency": "5x/week", "duration_min": 30, "reason": "Baseline zone 2 cardio aligned with WHO guidance."},
        {"type": "strength", "frequency": "2x/week", "duration_min": 40, "reason": "Maintain muscle mass and metabolic resilience."},
    ]
    priority_areas: list[str] = []
    if bio["cardiovascular"] > chrono:
        recommended_sessions.append({"type": "cycling", "frequency": "1x/week", "duration_min": 45, "reason": "Extra cardio to improve cardiovascular bio age."})
        priority_areas.append("cardiovascular")
    if bio["musculoskeletal"] > chrono:
        recommended_sessions.append({"type": "weight_training", "frequency": "1x/week", "duration_min": 45, "reason": "Extra strength focus for musculoskeletal age."})
        priority_areas.append("strength")
    if bio["neurological"] > chrono:
        recommended_sessions.append({"type": "yoga", "frequency": "2x/week", "duration_min": 20, "reason": "Mobility and stress regulation for neurological age."})
        priority_areas.append("flexibility")
    if (profile.get("bmi") or 0) > 25:
        recommended_sessions.append({"type": "hiit", "frequency": "1x/week", "duration_min": 20, "reason": "BMI suggests added metabolic conditioning."})
        priority_areas.append("metabolic")
    if (profile.get("posture_score_pct") or 100) < 70:
        recommended_sessions.append({"type": "yoga", "frequency": "3x/week", "duration_min": 15, "reason": "Low posture score benefits from mobility and stretching."})
    if (profile.get("vo2max") or 40) < 35:
        recommended_sessions.append({"type": "walking", "frequency": "daily", "duration_min": 35, "reason": "Low VO2max favors steady zone 2 work."})
    deduped: list[dict[str, Any]] = []
    seen: set[tuple[str, str, int]] = set()
    for session in recommended_sessions:
        key = (session["type"], session["frequency"], session["duration_min"])
        if key not in seen:
            seen.add(key)
            deduped.append(session)
    return {"weekly_target_min": 150, "recommended_sessions": deduped, "priority_areas": priority_areas or ["consistency"]}


def rank_impact(profile: dict[str, Any]) -> dict[str, Any]:
    """Rank habit changes by estimated bio-age impact."""

    candidate_changes: list[tuple[str, dict[str, Any]]] = [
        ("Sleep 8h", {"sleep_hours": 8}),
        ("10k steps", {"steps_avg_7d": 10000}),
        ("Exercise 5h/week", {"exercise_hours_week": 5, "exercise_min": 40}),
        ("Reduce stress to 4", {"stress_level": 4}),
        ("Cut screen time to 5h", {"screen_time_hours": 5}),
    ]
    ranked: list[dict[str, Any]] = []
    current = _calculate_bio_age_base(profile)["overall"]
    for label, changes in candidate_changes:
        projected = _calculate_bio_age_base({**deepcopy(profile), **changes})["overall"]
        ranked.append({"change": label, "estimated_bio_age_reduction": round(current - projected, 1), "changes": changes})
    ranked.sort(key=lambda item: item["estimated_bio_age_reduction"], reverse=True)
    return {"top_changes": ranked[:3], "ranked_changes": ranked}
