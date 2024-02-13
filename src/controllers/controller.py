from src.models.model import Model
from src.views.view import View
from .quiz import QuizController
from .sign_in import SignInController
from .sign_up import SignUpController


class Controller:
    def __init__(self, model: Model, view: View):
        self.view = view
        self.model = model
        self.signin_controller = SignInController(model, view)
        self.signup_controller = SignUpController(model, view)
        self.home_controller = QuizController(model, view)

        self.model.auth.add_event_listener(
            "auth_changed", self.auth_state_listener
        )

    def auth_state_listener(self, data):
        if data.is_logged_in:
            self.home_controller.update_view()
            self.view.switch("quiz")
        else:
            self.view.switch("signin")

    def start(self):
        # self.models.auth.load_auth_state()
        if self.model.auth.is_logged_in:
            self.view.switch("quiz")
        else:
            self.view.switch("signin")

        self.view.start_mainloop()
