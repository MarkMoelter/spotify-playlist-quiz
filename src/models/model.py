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
        redirect_url = os.getenv("REDIRECT_URI", "http://localhost:8888/callback")

        if not client_id or not client_secret:
            raise AuthError(
                "SPOTIPY_CLIENT_ID and SPOTIPY_CLIENT_SECRET must be set in your .env file."
            )

        scope = "playlist-read-private playlist-read-collaborative"
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

    # ── Quiz ──────────────────────────────────────────────────────────────────

    def build_question(self, tracks: list[Track]) -> dict:
        """Pick a random track and return a question dict with 4 choices."""
        correct = random.choice(tracks)
        wrong_pool = [t for t in tracks if t.uri != correct.uri]
        wrong = random.sample(wrong_pool, min(3, len(wrong_pool)))
        choices = [t.name for t in wrong] + [correct.name]
        random.shuffle(choices)
        return {"track": correct, "choices": choices, "answer": correct.name}
