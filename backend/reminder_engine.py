from __future__ import annotations

from datetime import date, datetime
from typing import Any

import aiosqlite

DATA_REFRESH_INTERVALS: dict[str, int] = {
    "healthkit": 2,
    "meal": 1,
    "water": 1,
    "posture": 7,
    "faceage": 30,
    "blood_report": 90,
    "cultfit": 30,
    "mental_checkin": 7,
    "spotify": 3,
}

URGENCY_RANK: dict[str, int] = {"low": 0, "medium": 1, "high": 2}


def _parse_dt(value: str | None) -> datetime | None:
    """Parse a stored datetime/date string into a datetime."""

    if not value:
        return None
    for fmt in ("%Y-%m-%d %H:%M:%S.%f", "%Y-%m-%d %H:%M:%S", "%Y-%m-%d"):
        try:
            return datetime.strptime(value[: len(fmt)], fmt)
        except ValueError:
            continue
    try:
        return datetime.fromisoformat(value)
    except ValueError:
        return None


async def get_reminders(user_id: str, db: aiosqlite.Connection) -> list[dict[str, Any]]:
    """Generate all reminders for a user."""

    reminders: list[dict[str, Any]] = []
    profile = await (await db.execute("SELECT * FROM profiles WHERE user_id=?", (user_id,))).fetchone()
    source_rows = await (await db.execute("SELECT * FROM data_sources WHERE user_id=?", (user_id,))).fetchall()
    normal_blood = True
    if profile:
        normal_blood = all(
            [
                (profile["ldl"] is None or profile["ldl"] <= 100),
                (profile["vitamin_d"] is None or profile["vitamin_d"] >= 20),
                (profile["fasting_glucose"] is None or profile["fasting_glucose"] <= 100),
                (profile["hba1c"] is None or profile["hba1c"] <= 5.7),
            ]
        )
    for row in source_rows:
        source = row["source"]
        interval = row["refresh_interval_days"] or DATA_REFRESH_INTERVALS.get(source, 7)
        if source == "blood_report":
            interval = 180 if normal_blood else 90
        last_synced = _parse_dt(row["last_synced_at"])
        if not last_synced:
            overdue = interval
        else:
            overdue = max((datetime.now() - last_synced).days - interval, 0)
        if overdue <= 0:
            continue
        urgency = "low" if overdue < interval * 0.5 else "medium" if overdue <= interval else "high"
        reminders.append(
            {
                "type": "data_freshness",
                "source": source,
                "message": f"{source.replace('_', ' ').title()} data is overdue for refresh.",
                "urgency": urgency,
                "days_overdue": overdue,
                "last_synced": row["last_synced_at"],
            }
        )
    def medical(source: str, message: str, days_overdue: int) -> None:
        urgency = "high" if days_overdue > 30 else "medium"
        reminders.append({"type": "medical_checkup", "source": source, "message": message, "urgency": urgency, "days_overdue": days_overdue, "last_synced": None})
    if profile:
        vitd_test = _parse_dt(profile["last_vitd_test_date"])
        if (profile["vitamin_d"] or 100) < 20 and vitd_test and (date.today() - vitd_test.date()).days > 90:
            medical("vitamin_d_retest", "Vitamin D is low and retesting is overdue.", (date.today() - vitd_test.date()).days - 90)
        glucose_test = _parse_dt(profile["last_glucose_test_date"])
        if (profile["fasting_glucose"] or 0) > 100 and glucose_test and (date.today() - glucose_test.date()).days > 90:
            medical("glucose_retest", "Elevated fasting glucose should be rechecked.", (date.today() - glucose_test.date()).days - 90)
        general_checkup = _parse_dt(profile["last_general_checkup_date"])
        if general_checkup is None or (date.today() - general_checkup.date()).days > 365:
            medical("general_checkup", "Annual general checkup is due.", 0 if general_checkup is None else (date.today() - general_checkup.date()).days - 365)
        blood_test = _parse_dt(profile["last_blood_report_date"])
        blood_interval = 90 if (profile["ldl"] or 0) > 130 else 180
        if blood_test and (date.today() - blood_test.date()).days > blood_interval:
            medical("blood_panel", "Blood lipid panel follow-up is due.", (date.today() - blood_test.date()).days - blood_interval)
    return sorted(reminders, key=lambda item: (URGENCY_RANK.get(item["urgency"], 0), item["days_overdue"]), reverse=True)


async def check_reminders(user_id: str, db: aiosqlite.Connection) -> list[dict[str, Any]]:
    """Compatibility alias for reminder generation."""

    return await get_reminders(user_id, db)
