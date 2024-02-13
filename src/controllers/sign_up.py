class SignUpController:
    def __init__(self, model, view):
        self.model = model
        self.view = view
        self.frame = self.view.frames["signup"]
        self._bind()

    def _bind(self):
        self.frame.signup_btn.config(command=self.signup)
        self.frame.signin_btn.config(command=self.signin)

    def signin(self):
        self.view.switch("signin")

    def signup(self):
        data = {
            "fullname": self.frame.fullname_input.get(),
            "username": self.frame.username_input.get(),
            "password": self.frame.password_input.get(),
            "has_agreed": self.frame.has_agreed.get(),
        }
        print(data)
        self.model.auth.login(data)
