from .home import HomeView
from .quiz import QuizView
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
        self._add_frame(QuizView, "quiz")

        self._on_start_quiz = None  # set by Controller

    def _add_frame(self, Frame, name):
        self.frames[name] = Frame(self.root)
        self.frames[name].grid(row=0, column=0, sticky="nsew")
        self.frames[name].grid_columnconfigure(0, weight=1)

    def switch(self, name):
        self.frames[name].tkraise()

    def start_quiz(self, tracks, show_artist: bool = True):
        if self._on_start_quiz:
            self._on_start_quiz(tracks, show_artist=show_artist)

    def start_mainloop(self):
        self.root.mainloop()
