from .observable import ObservableModel


class Auth(ObservableModel):
    def __init__(self):
        super().__init__()
        self.is_logged_in = False
        self.current_user = None
        self.client = None  # spotipy.Spotify instance set after OAuth

    def login(self, client, user: dict):
        self.client = client
        self.is_logged_in = True
        self.current_user = user
        self.trigger_event("auth_changed")

    def logout(self):
        self.client = None
        self.is_logged_in = False
        self.current_user = None
        self.trigger_event("auth_changed")
