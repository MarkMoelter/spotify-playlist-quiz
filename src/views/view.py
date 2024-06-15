from .home import HomeView
from .root import Root
from .sign_in import SignInView
from .sign_up import SignUpView


class View:
    def __init__(self):
        self.root = Root()
        self.frames = {}

        self._add_frame(SignInView, "signin")
        self._add_frame(SignUpView, "signup")
        self._add_frame(HomeView, "home")

    def _add_frame(self, Frame, name):
        self.frames[name] = Frame(self.root)
        self.frames[name].grid(row=0, column=0, sticky="nsew")

    def switch(self, name):
        frame = self.frames[name]
        frame.tkraise()

    def start_mainloop(self):
        self.root.mainloop()
