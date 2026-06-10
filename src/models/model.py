import os
import random

import spotipy

from .auth import Auth
from .track import Track


class Model:
    def __init__(self):
        self.auth = Auth()

    # ── Auth ──────────────────────────────────────────────────────────────────

    def connect(self):
        """Open the Spotify OAuth flow, store the authenticated client and user."""
        client_id = os.getenv("SPOTIPY_CLIENT_ID")
        client_secret = os.getenv("SPOTIPY_CLIENT_SECRET")
        redirect_url = os.getenv("REDIRECT_URI", "http://localhost:8888/callback")
        scope = "playlist-read-private playlist-read-collaborative"

        oauth = spotipy.SpotifyOAuth(
            client_id=client_id,
            client_secret=client_secret,
            redirect_uri=redirect_url,
            scope=scope,
        )
        token = oauth.get_access_token(as_dict=False)
        client = spotipy.Spotify(auth=token)
        user = client.current_user()
        self.auth.login(client, {"username": user["display_name"] or user["id"]})

    @property
    def _client(self) -> spotipy.Spotify:
        return self.auth.client

    # ── Playlists ─────────────────────────────────────────────────────────────

    def user_playlists(self, limit: int = 50, offset: int = 0) -> dict[str, str]:
        """Return {playlist_name: playlist_uri} for the current user."""
        return {
            item["name"]: item["uri"]
            for item in self._client.current_user_playlists(
                limit=limit, offset=offset
            )["items"]
        }

    def parse_raw_playlist(self, playlist_id: str, limit: int = 100) -> list[Track]:
        """Convert a playlist into a list of Track objects."""
        songs = []
        for track in self._client.playlist_items(playlist_id, limit=limit)["items"]:
            track_info = track["track"]
            if not track_info:
                continue
            songs.append(
                Track(
                    name=track_info["name"],
                    album=track_info["album"]["name"],
                    artists=[a["name"] for a in track_info["artists"]],
                    uri=track_info["uri"],
                )
            )
        return songs

    # ── Quiz ──────────────────────────────────────────────────────────────────

    def build_question(self, tracks: list[Track]) -> dict:
        """Pick a random track and return a question dict with 4 choices.

        Returns:
            {
                "track": Track,
                "choices": [str, str, str, str],   # shuffled track names
                "answer": str,                      # correct track name
            }
        """
        correct = random.choice(tracks)
        wrong_pool = [t for t in tracks if t.uri != correct.uri]
        wrong = random.sample(wrong_pool, min(3, len(wrong_pool)))
        choices = [t.name for t in wrong] + [correct.name]
        random.shuffle(choices)
        return {"track": correct, "choices": choices, "answer": correct.name}
