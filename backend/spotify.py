from __future__ import annotations

import base64
import hashlib
import hmac
import json
import os
import time
from typing import Any

try:
    import spotipy  # type: ignore
    from spotipy.oauth2 import SpotifyOAuth  # type: ignore
except Exception:  # pragma: no cover - optional dependency
    spotipy = None
    SpotifyOAuth = None

from backend.database import get_profile_dict

SPOTIFY_STATE_SECRET = os.getenv("SPOTIFY_STATE_SECRET") or os.getenv("SPOTIFY_CLIENT_SECRET", "eirview-spotify-state")
SPOTIFY_STATE_TTL_SECONDS = 900

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


def _clamp_unit(value: float) -> float:
    """Clamp a proxy metric to the 0-1 range."""

    return max(0.0, min(1.0, float(value)))


def _estimate_features_from_tracks(items: list[dict[str, Any]]) -> tuple[float, float, float, int, str]:
    """Estimate mood metrics from recent-track metadata when audio features are unavailable."""

    tracks = [item.get("track") or {} for item in items if isinstance(item, dict)]
    if not tracks:
        return 0.42, 0.55, 0.61, 0, "empty_fallback"
    count = len(tracks)
    popularity_values = [(track.get("popularity") or 50) / 100 for track in tracks]
    duration_values = [track.get("duration_ms") or 180000 for track in tracks]
    explicit_values = [1.0 if track.get("explicit") else 0.0 for track in tracks]
    artist_count_values = [len(track.get("artists") or []) or 1 for track in tracks]
    avg_popularity = sum(popularity_values) / count
    avg_duration = sum(duration_values) / count
    avg_explicit = sum(explicit_values) / count
    avg_artist_count = sum(artist_count_values) / count
    energy = _clamp_unit(0.35 + avg_popularity * 0.45 + (1.0 if avg_duration < 210000 else 0.7 if avg_duration < 260000 else 0.45) * 0.2)
    danceability = _clamp_unit(0.3 + avg_popularity * 0.35 + avg_explicit * 0.15 + (0.15 if avg_artist_count > 1.2 else 0.05))
    valence = _clamp_unit(0.28 + avg_popularity * 0.4 + (0.18 if avg_duration < 200000 else 0.08 if avg_duration < 260000 else -0.04) - avg_explicit * 0.05)
    return round(valence, 4), round(energy, 4), round(danceability, 4), count, "metadata_fallback"


def generate_spotify_oauth_state(user_id: str) -> str:
    """Create a signed short-lived OAuth state that encodes the user id."""

    issued_at = str(int(time.time()))
    payload = f"{user_id}:{issued_at}"
    signature = hmac.new(SPOTIFY_STATE_SECRET.encode("utf-8"), payload.encode("utf-8"), hashlib.sha256).hexdigest()[:24]
    token = base64.urlsafe_b64encode(f"{payload}:{signature}".encode("utf-8")).decode("utf-8").rstrip("=")
    return token


def resolve_spotify_oauth_state(state: str) -> str:
    """Validate and decode the Spotify OAuth state token."""

    if not state:
        raise ValueError("Missing Spotify OAuth state")
    padded = state + "=" * (-len(state) % 4)
    try:
        decoded = base64.urlsafe_b64decode(padded.encode("utf-8")).decode("utf-8")
        user_id, issued_at, signature = decoded.split(":", 2)
    except Exception as exc:
        raise ValueError("Invalid Spotify OAuth state") from exc
    payload = f"{user_id}:{issued_at}"
    expected = hmac.new(SPOTIFY_STATE_SECRET.encode("utf-8"), payload.encode("utf-8"), hashlib.sha256).hexdigest()[:24]
    if not hmac.compare_digest(signature, expected):
        raise ValueError("Invalid Spotify OAuth state signature")
    if int(time.time()) - int(issued_at) > SPOTIFY_STATE_TTL_SECONDS:
        raise ValueError("Spotify OAuth state expired")
    return user_id


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
        sync_mode = "sdk_unavailable_fallback"
    else:  # pragma: no cover - external API integration
        sp = spotipy.Spotify(auth=token)
        results = sp.current_user_recently_played(limit=50)
        if not results or not results.get("items"):
            return {"error": "No recently played tracks found"}
        track_ids = []
        seen_ids: set[str] = set()
        for item in results["items"]:
            track_id = item.get("track", {}).get("id")
            if track_id and track_id not in seen_ids:
                seen_ids.add(track_id)
                track_ids.append(track_id)
        try:
            feature_rows: list[dict[str, Any]] = []
            for start in range(0, len(track_ids), 100):
                batch = track_ids[start:start + 100]
                response = sp.audio_features(batch)
                if response:
                    feature_rows.extend([item for item in response if item is not None])
            if not feature_rows:
                raise RuntimeError("Spotify audio features returned no usable data")
            count = len(feature_rows)
            avg_valence = round(sum(item["valence"] for item in feature_rows) / count, 4)
            avg_energy = round(sum(item["energy"] for item in feature_rows) / count, 4)
            avg_danceability = round(sum(item["danceability"] for item in feature_rows) / count, 4)
            sync_mode = "audio_features"
        except Exception:
            avg_valence, avg_energy, avg_danceability, count, sync_mode = _estimate_features_from_tracks(results["items"])
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
        "sync_mode": sync_mode,
        "baseline_valence": round(float(baseline_valence), 4),
        "valence_shift": round(avg_valence - float(baseline_valence), 4),
        "flagged": flagged,
        "cross_signals": cross_signals,
        "flag_reason": f"Valence dropped below baseline and was confirmed by {', '.join(cross_signals)}" if flagged else None,
    }
