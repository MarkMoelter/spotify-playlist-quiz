import logging
import threading

from src.exceptions import NetworkError, PlaylistError

logger = logging.getLogger("my_app")


class HomeController:
    def __init__(self, model, view):
        self.model = model
        self.view = view
        self.frame = self.view.frames["home"]
        self._playlist_map: dict[str, str] = {}
        self._bind()

    def _bind(self):
        self.frame.signout_btn.config(command=self.logout)
        self.frame.select_playlist_btn.config(command=self.select_playlist)

    def update_view(self):
        """Called after successful login — updates greeting and loads playlists."""
        current_user = self.model.auth.current_user
        if current_user:
            self.frame.greeting.config(text=f"Welcome, {current_user['username']}!")

        self._set_status("Loading playlists…")
        self.frame.select_playlist_btn.config(state="disabled")
        # Network call on background thread — same pattern as OAuth
        threading.Thread(target=self._fetch_playlists, daemon=True).start()

    def _fetch_playlists(self):
        try:
            playlists = self.model.user_playlists()
            self.frame.after(0, self._on_playlists_loaded, playlists)
        except (NetworkError, PlaylistError) as e:
            # Expected errors: show a friendly message
            self.frame.after(0, self._set_status, str(e))
        except Exception as e:
            # Unexpected errors: log the full detail, show a generic message
            logger.exception("Unexpected error loading playlists")
            self.frame.after(0, self._set_status, "Something went wrong loading playlists.")

    def _on_playlists_loaded(self, playlists: dict[str, str]):
        self._playlist_map = playlists
        self.frame.playlists["values"] = list(playlists.keys())
        self.frame.playlists.current(0)
        self.frame.select_playlist_btn.config(state="normal")
        self._set_status("")

    def select_playlist(self):
        name = self.frame.playlists.get()
        if not name or name not in self._playlist_map:
            return

        self._set_status("Loading tracks…")
        self.frame.select_playlist_btn.config(state="disabled")
        playlist_id = self._playlist_map[name].split(":")[-1]
        threading.Thread(
            target=self._fetch_tracks, args=(playlist_id,), daemon=True
        ).start()

    def _fetch_tracks(self, playlist_id: str):
        try:
            tracks = self.model.parse_raw_playlist(playlist_id)
            self.frame.after(0, self._on_tracks_loaded, tracks)
        except (NetworkError, PlaylistError) as e:
            self.frame.after(0, self._on_track_error, str(e))
        except Exception:
            logger.exception("Unexpected error loading tracks")
            self.frame.after(0, self._on_track_error, "Something went wrong loading tracks.")

    def _on_tracks_loaded(self, tracks):
        self._set_status(f"{len(tracks)} tracks loaded.")
        self.frame.select_playlist_btn.config(state="normal")
        self.view.start_quiz(
            tracks,
            show_artist=self.frame.show_artist.get(),
            num_questions=int(self.frame.quiz_length.get()),
            playlist_name=self.frame.playlists.get(),
        )

    def _on_track_error(self, message: str):
        self._set_status(message)
        self.frame.select_playlist_btn.config(state="normal")

    def logout(self):
        self.model.auth.logout()

    def _set_status(self, text: str):
        self.frame.status_label.config(text=text)
