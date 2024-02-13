from .observable import ObservableModel


class Auth(ObservableModel):
    def __init__(self):
        super().__init__()
        self.is_logged_in = False
        self.current_user = None

    def login(self, user):
        self.is_logged_in = True
        self.current_user = user
        self.trigger_event("auth_changed")

    def logout(self):
        self.is_logged_in = False
        self.current_user = None
        self.trigger_event("auth_changed")
