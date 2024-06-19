class HomeController:
    def __init__(self, model, view):
        self.model = model
        self.view = view
        self.frame = self.view.frames["home"]
        self._bind()

    def _bind(self):
        self.frame.signout_btn.config(command=self.logout)
        self.frame.playlists["values"] = [
            playlist for playlist in self.model.user_playlists().keys()
        ]

    def logout(self):
        self.model.auth.logout()

    def update_view(self):
        current_user = self.model.auth.current_user
        if current_user:
            username = current_user["username"]
            self.frame.greeting.config(text=f"Welcome, {username}!")
        else:
            self.frame.greeting.config(text="Not logged in")
