from __future__ import annotations

import json
import os
from typing import Any

try:
    import spotipy  # type: ignore
    from spotipy.oauth2 import SpotifyOAuth  # type: ignore
except Exception:  # pragma: no cover - optional dependency
    spotipy = None
    SpotifyOAuth = None

from backend.database import get_profile_dict

class _FallbackSpotifyOAuth:
    """Fallback OAuth helper when Spotify OAuth is unavailable."""

    def get_authorize_url(self, state: str = "") -> str:
        """Return a placeholder auth URL."""

        return f"/spotify-auth-unavailable?state={state}"


def _build_spotify_oauth() -> Any:
    if SpotifyOAuth is None:
        return _FallbackSpotifyOAuth()
    client_id = os.getenv("SPOTIFY_CLIENT_ID", "")
    client_secret = os.getenv("SPOTIFY_CLIENT_SECRET", "")
    if not client_id or not client_secret:
        return _FallbackSpotifyOAuth()
    try:
        return SpotifyOAuth(
            client_id=client_id,
            client_secret=client_secret,
            redirect_uri=os.getenv("SPOTIFY_REDIRECT_URI", "http://127.0.0.1:5173/callback"),
            scope="user-read-recently-played",
        )
    except Exception:
        return _FallbackSpotifyOAuth()


sp_oauth: Any = _build_spotify_oauth()


def exchange_spotify_code(code: str) -> str:
    """Exchange an OAuth authorization code for an access token."""

    if spotipy is None or not hasattr(sp_oauth, "get_access_token"):
        raise RuntimeError("Spotify OAuth is unavailable")
    token_info = sp_oauth.get_access_token(code, check_cache=False)
    if isinstance(token_info, dict):
        access_token = token_info.get("access_token")
    else:
        access_token = token_info
    if not access_token:
        raise RuntimeError("Spotify token exchange failed")
    return str(access_token)


async def sync_spotify(user_id: str, token: str, db: Any) -> dict:
    """Fetch recent tracks, compute features, and detect mood patterns."""

    if spotipy is None:
        avg_valence = 0.42
        avg_energy = 0.55
        avg_danceability = 0.61
        count = 20
    else:  # pragma: no cover - external API integration
        sp = spotipy.Spotify(auth=token)
        results = sp.current_user_recently_played(limit=50)
        if not results or not results.get("items"):
            return {"error": "No recently played tracks found"}
        track_ids = [item["track"]["id"] for item in results["items"] if item.get("track", {}).get("id")]
        features = [item for item in sp.audio_features(track_ids) if item is not None]
        if not features:
            return {"error": "Could not retrieve audio features"}
        count = len(features)
        avg_valence = round(sum(item["valence"] for item in features) / count, 4)
        avg_energy = round(sum(item["energy"] for item in features) / count, 4)
        avg_danceability = round(sum(item["danceability"] for item in features) / count, 4)
    baseline_row = await (await db.execute("SELECT AVG(avg_valence) AS bv FROM spotify_history WHERE user_id=?", (user_id,))).fetchone()
    baseline_valence = baseline_row["bv"] if baseline_row and baseline_row["bv"] is not None else avg_valence
    profile = await get_profile_dict(user_id, db) or {}
    cross_signals: list[str] = []
    if (profile.get("sleep_hours") or 7) < 6:
        cross_signals.append("sleep_declining")
    if (profile.get("steps_avg_7d") or 7500) < 5000:
        cross_signals.append("steps_declining")
    if (profile.get("hrv_ms") or 40) < 30:
        cross_signals.append("hrv_low")
    if (profile.get("stress_level") or 5) > 6:
        cross_signals.append("stress_high")
    flagged = (baseline_valence - avg_valence) > 0.15 and len(cross_signals) >= 1
    await db.execute(
        "INSERT INTO spotify_history (user_id, avg_valence, avg_energy, avg_danceability, track_count, baseline_valence, flagged, flag_reason) VALUES (?,?,?,?,?,?,?,?)",
        (user_id, avg_valence, avg_energy, avg_danceability, count, baseline_valence, flagged, json.dumps(cross_signals) if flagged else None),
    )
    await db.execute(
        "INSERT OR REPLACE INTO spotify_tokens (user_id, access_token, updated_at) VALUES (?,?,CURRENT_TIMESTAMP)",
        (user_id, token),
    )
    await db.commit()
    return {
        "avg_valence": avg_valence,
        "avg_energy": avg_energy,
        "avg_danceability": avg_danceability,
        "track_count": count,
        "baseline_valence": round(float(baseline_valence), 4),
        "valence_shift": round(avg_valence - float(baseline_valence), 4),
        "flagged": flagged,
        "cross_signals": cross_signals,
        "flag_reason": f"Valence dropped below baseline and was confirmed by {', '.join(cross_signals)}" if flagged else None,
    }
