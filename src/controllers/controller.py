from src.models.leaderboard import LeaderboardModel
from src.models.model import Model
from src.views.view import View
from .home import HomeController
from .leaderboard import LeaderboardController
from .quiz import QuizController
from .sign_in import SignInController
from .sign_up import SignUpController


class Controller:
    def __init__(self, model: Model, view: View):
        self.view = view
        self.model = model
        self.lb_model = LeaderboardModel()

        self.signin_controller = SignInController(model, view)
        self.signup_controller = SignUpController(model, view)
        self.home_controller = HomeController(model, view)
        self.quiz_controller = QuizController(model, self.lb_model, view)
        self.lb_controller = LeaderboardController(self.lb_model, view)

        self.view._on_start_quiz = self.quiz_controller.start
        self.view._on_show_leaderboard = self.lb_controller.show
        self.model.auth.add_event_listener("auth_changed", self._auth_state_listener)

        # Wire home screen leaderboard button
        self.view.frames["home"].leaderboard_btn.config(
            command=self.lb_controller.show)
        # Wire quiz results home button
        self.view.frames["quiz"].home_btn.config(
            command=self.quiz_controller._back_home)

    def _auth_state_listener(self, auth):
        if auth.is_logged_in:
            self.home_controller.update_view()
            self.view.switch("home")
        else:
            self.signin_controller.reset()
            self.view.switch("signin")

    def start(self):
        if self.model.auth.is_logged_in:
            self.view.switch("home")
        else:
            self.view.switch("signin")
        self.view.start_mainloop()
