import os
import random

import spotipy
from requests.exceptions import ConnectionError, Timeout

from .auth import Auth
from .track import Track
from src.exceptions import AuthError, NetworkError, PlaylistError


class Model:
    def __init__(self):
        self.auth = Auth()

    # ── Auth ──────────────────────────────────────────────────────────────────

    def connect(self):
        """Open the Spotify OAuth flow, store the authenticated client and user.

        Raises:
            AuthError: credentials missing or OAuth was rejected.
            NetworkError: could not reach Spotify's servers.
        """
        client_id = os.getenv("SPOTIPY_CLIENT_ID")
        client_secret = os.getenv("SPOTIPY_CLIENT_SECRET")
        redirect_url = os.getenv("REDIRECT_URI", "http://127.0.0.1:8888/callback")

        if not client_id or not client_secret:
            raise AuthError(
                "SPOTIPY_CLIENT_ID and SPOTIPY_CLIENT_SECRET must be set in your .env file."
            )

        scope = (
            "playlist-read-private "
            "playlist-read-collaborative "
            "user-modify-playback-state "  # needed to start/pause playback
            "user-read-playback-state"     # needed to check active devices
        )
        try:
            oauth = spotipy.SpotifyOAuth(
                client_id=client_id,
                client_secret=client_secret,
                redirect_uri=redirect_url,
                scope=scope,
            )
            token = oauth.get_access_token(as_dict=False)
            if not token:
                raise AuthError("Spotify did not return an access token. Try again.")

            client = spotipy.Spotify(auth=token)
            user = client.current_user()
        except (ConnectionError, Timeout):
            raise NetworkError("Could not reach Spotify. Check your internet connection.")
        except spotipy.SpotifyException as e:
            # 401 = bad credentials, 403 = wrong scope, etc.
            raise AuthError(f"Spotify rejected the login ({e.http_status}).")
        except AuthError:
            raise  # already the right type, don't wrap it
        except Exception as e:
            raise AuthError(f"Login failed: {e}") from e

        self.auth.login(client, {"username": user["display_name"] or user["id"]})

    @property
    def _client(self) -> spotipy.Spotify:
        return self.auth.client

    # ── Playlists ─────────────────────────────────────────────────────────────

    def user_playlists(self, limit: int = 50, offset: int = 0) -> dict[str, str]:
        """Return {playlist_name: playlist_uri} for the current user.

        Raises:
            NetworkError: request failed.
            PlaylistError: account has no playlists.
        """
        try:
            items = self._client.current_user_playlists(
                limit=limit, offset=offset
            )["items"]
        except (ConnectionError, Timeout):
            raise NetworkError("Lost connection while loading playlists.")
        except spotipy.SpotifyException as e:
            raise NetworkError(f"Spotify error loading playlists ({e.http_status}).")

        if not items:
            raise PlaylistError("No playlists found on this account.")

        return {item["name"]: item["uri"] for item in items}

    def parse_raw_playlist(self, playlist_id: str, limit: int = 100) -> list[Track]:
        """Convert a playlist into a list of Track objects.

        Raises:
            NetworkError: request failed.
            PlaylistError: playlist has fewer than 4 playable tracks.
        """
        try:
            raw = self._client.playlist_items(playlist_id, limit=limit)["items"]
        except (ConnectionError, Timeout):
            raise NetworkError("Lost connection while loading tracks.")
        except spotipy.SpotifyException as e:
            raise NetworkError(f"Spotify error loading tracks ({e.http_status}).")

        songs = []
        for track in raw:
            track_info = track.get("track")
            if not track_info:
                continue
            songs.append(
                Track(
                    name=track_info["name"],
                    album=track_info["album"]["name"],
                    artists=[a["name"] for a in track_info["artists"]],
                    uri=track_info["uri"],
                    preview_url=track_info.get("preview_url"),
                )
            )

        if len(songs) < 4:
            raise PlaylistError(
                "This playlist needs at least 4 tracks to generate a quiz."
            )
        return songs

    # ── Playback ──────────────────────────────────────────────────────────────

    def get_active_device(self) -> str | None:
        """Return the ID of the user's active Spotify device, or None."""
        try:
            devices = self._client.devices().get("devices", [])
            # Prefer the currently active device; fall back to the first available
            for d in devices:
                if d["is_active"]:
                    return d["id"]
            return devices[0]["id"] if devices else None
        except Exception:
            return None

    def play_track(self, uri: str, device_id: str | None = None):
        """Start playing a track on the given device (or the active device).

        Raises:
            NetworkError: Spotify API call failed.
            PlaylistError: no active device found.
        """
        if device_id is None:
            device_id = self.get_active_device()
        if device_id is None:
            raise PlaylistError(
                "No active Spotify device found. Open Spotify on your phone or "
                "desktop and play something briefly, then try again."
            )
        try:
            self._client.start_playback(device_id=device_id, uris=[uri])
        except (ConnectionError, Timeout):
            raise NetworkError("Lost connection while starting playback.")
        except spotipy.SpotifyException as e:
            if e.http_status == 403:
                raise PlaylistError("Spotify Premium is required for playback control.")
            raise NetworkError(f"Spotify playback error ({e.http_status}).")

    def pause_playback(self, device_id: str | None = None):
        """Pause playback. Silently ignored if nothing is playing."""
        try:
            self._client.pause_playback(device_id=device_id)
        except Exception:
            pass  # not playing, no device, etc. — all fine to ignore

    # ── Quiz ──────────────────────────────────────────────────────────────────

    def build_questions(self, tracks: list[Track],
                        selected: list[Track]) -> list[dict]:
        """Build one question per selected track, varying wrong choices across the round.

        Building all questions together (rather than one at a time) lets us track
        which names have already appeared as distractors and prefer fresh ones for
        each new question — so the same song doesn't show up as a wrong choice over
        and over.
        """
        # Deduplicate the entire track list by name — covers/remixes with the
        # same title count as one candidate regardless of URI.
        unique_by_name: dict[str, Track] = {}
        for t in tracks:
            if t.name not in unique_by_name:
                unique_by_name[t.name] = t

        used_as_wrong: set[str] = set()
        questions: list[dict] = []

        for correct in selected:
            # Only exclude THIS question's answer — not all selected answers.
            # Excluding all selected answers was shrinking the pool too aggressively
            # on small playlists, causing blank choice slots.
            pool = [name for name in unique_by_name if name != correct.name]

            # Split into unused-this-round vs already-used, shuffle each
            # independently so fallback choices are also random (not always the
            # same tracks in the same order).
            unused = [n for n in pool if n not in used_as_wrong]
            reused = [n for n in pool if n in used_as_wrong]
            random.shuffle(unused)
            random.shuffle(reused)

            # Take up to 3, preferring fresh names
            wrong_names = (unused + reused)[:3]
            used_as_wrong.update(wrong_names)

            choices = wrong_names + [correct.name]
            random.shuffle(choices)
            questions.append({"track": correct, "choices": choices,
                               "answer": correct.name})

        return questions
