class SignInController:
    def __init__(self, model, view):
        self.model = model
        self.view = view
        self.frame = self.view.frames["signin"]
        self._bind()

    def _bind(self):
        self.frame.signin_btn.config(command=self.signin)
        self.frame.signup_btn.config(command=self.signup)

    def signup(self):
        self.view.switch("signup")

    def signin(self):
        username = self.frame.username_input.get()
        pasword = self.frame.password_input.get()
        data = {"username": username, "password": pasword}
        print(data)  # of course we don't want to print the password in a real app!
        self.frame.password_input.delete(0, last=len(pasword))
        self.model.auth.login(data)
