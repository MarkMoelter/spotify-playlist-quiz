from src.models.track import Track

QUESTIONS_PER_ROUND = 10


class QuizController:
    def __init__(self, model, view):
        self.model = model
        self.view = view
        self.frame = self.view.frames["quiz"]
        self._tracks: list[Track] = []
        self._questions: list[dict] = []
        self._current: int = 0
        self._score: int = 0

    def start(self, tracks: list[Track]):
        """Begin a new quiz round with the given track list."""
        self._tracks = tracks
        n = min(QUESTIONS_PER_ROUND, len(tracks))
        self._questions = [self.model.build_question(tracks) for _ in range(n)]
        self._current = 0
        self._score = 0
        self._show_question()
        self.view.switch("quiz")

    def _show_question(self):
        q = self._questions[self._current]
        total = len(self._questions)

        self.frame.progress_label.config(
            text=f"Question {self._current + 1} of {total}  |  Score: {self._score}"
        )
        self.frame.prompt.config(text="Which song is this?")
        self.frame.artist_label.config(
            text=f"Artist: {q['track'].artists[0]}"
        )
        self.frame.feedback_label.config(text="")
        self.frame.next_btn.grid_remove()

        for i, btn in enumerate(self.frame.choice_btns):
            choice = q["choices"][i] if i < len(q["choices"]) else ""
            btn.config(
                text=choice,
                state="normal",
                bg="SystemButtonFace",
                command=lambda c=choice: self._answer(c),
            )

    def _answer(self, chosen: str):
        q = self._questions[self._current]
        correct = q["answer"]

        # Disable all buttons so the user can't answer twice
        for btn in self.frame.choice_btns:
            btn.config(state="disabled")
            if btn["text"] == correct:
                btn.config(bg="#4caf50")  # green = correct answer
            elif btn["text"] == chosen and chosen != correct:
                btn.config(bg="#f44336")  # red = wrong pick

        if chosen == correct:
            self._score += 1
            self.frame.feedback_label.config(text="Correct!", fg="green")
        else:
            self.frame.feedback_label.config(
                text=f'Wrong — it was "{correct}"', fg="red"
            )

        last = self._current == len(self._questions) - 1
        self.frame.next_btn.config(
            text="See Results" if last else "Next",
            command=self._finish if last else self._next,
        )
        self.frame.next_btn.grid()

    def _next(self):
        self._current += 1
        self._show_question()

    def _finish(self):
        total = len(self._questions)
        pct = self._score * 100 // total
        rating = (
            "Perfect!" if pct == 100
            else "Great job!" if pct >= 70
            else "Not bad!" if pct >= 40
            else "Keep listening!"
        )
        self.frame.progress_label.config(
            text=f"Quiz complete!  {self._score}/{total}  ({pct}%)  {rating}"
        )
        self.frame.prompt.config(text="")
        self.frame.artist_label.config(text="")
        self.frame.feedback_label.config(text="")
        for btn in self.frame.choice_btns:
            btn.grid_remove()
        self.frame.next_btn.config(text="Back to Home", command=self._back_home)
        self.frame.next_btn.grid()

    def _back_home(self):
        for btn in self.frame.choice_btns:
            btn.grid()
            btn.config(bg="SystemButtonFace")
        self.view.switch("home")
