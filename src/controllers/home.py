class HomeController:
    def __init__(self, model, view):
        self.model = model
        self.view = view
        self.frame = self.view.frames["home"]
        self._playlist_map: dict[str, str] = {}  # name -> uri
        self._bind()

    def _bind(self):
        self.frame.signout_btn.config(command=self.logout)
        self.frame.select_playlist_btn.config(command=self.select_playlist)

    def update_view(self):
        """Called after successful login — loads playlists and updates greeting."""
        current_user = self.model.auth.current_user
        if current_user:
            self.frame.greeting.config(text=f"Welcome, {current_user['username']}!")
        self._load_playlists()

    def _load_playlists(self):
        self._playlist_map = self.model.user_playlists()
        self.frame.playlists["values"] = list(self._playlist_map.keys())
        if self._playlist_map:
            self.frame.playlists.current(0)

    def select_playlist(self):
        name = self.frame.playlists.get()
        if not name or name not in self._playlist_map:
            return
        uri = self._playlist_map[name]
        # Strip "spotify:playlist:" prefix to get the bare ID
        playlist_id = uri.split(":")[-1]
        tracks = self.model.parse_raw_playlist(playlist_id)
        if len(tracks) < 4:
            self.frame.greeting.config(text="Playlist too small (need 4+ tracks).")
            return
        self.view.start_quiz(tracks)

    def logout(self):
        self.model.auth.logout()
