class LeaderboardController:
    def __init__(self, leaderboard_model, view):
        self.lb = leaderboard_model
        self.view = view
        self.frame = self.view.frames["leaderboard"]
        self._bind()

    def _bind(self):
        self.frame.back_btn.config(command=self._back)
        self.frame.clear_btn.config(command=self._clear)

    def show(self):
        """Refresh and display the leaderboard."""
        self.frame.populate(self.lb.load())
        self.view.switch("leaderboard")

    def _clear(self):
        self.lb.clear()
        self.frame.populate([])

    def _back(self):
        self.view.switch("home")
