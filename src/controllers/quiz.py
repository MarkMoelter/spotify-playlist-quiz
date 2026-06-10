from src.audio import AudioPlayer
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

        self._audio = AudioPlayer()
        # AudioPlayer calls on_status from a background thread.
        # Tkinter widgets must only be updated from the main thread.
        # frame.after(0, fn) schedules fn to run on the main thread at the
        # next opportunity — this is the standard Tkinter thread-bridge pattern.
        self._audio.on_status = lambda s: self.frame.after(0, self._on_audio_status, s)

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
        self.frame.prompt.config(text="Listen to the preview — which song is it?")
        self.frame.artist_label.config(text=f"Artist: {q['track'].artists[0]}")
        self.frame.feedback_label.config(text="")
        self.frame.next_btn.grid_remove()
        self.frame.audio_status.config(text="")

        for i, btn in enumerate(self.frame.choice_btns):
            choice = q["choices"][i] if i < len(q["choices"]) else ""
            btn.config(
                text=choice,
                state="normal",
                bg="SystemButtonFace",
                command=lambda c=choice: self._answer(c),
            )

        # Wire the play button to replay the preview on demand
        preview_url = q["track"].preview_url
        self.frame.play_btn.config(
            state="normal",
            command=lambda: self._audio.play(preview_url),
        )

        # Auto-play as soon as the question appears
        self._audio.play(preview_url)

    def _on_audio_status(self, status: str):
        """Update the audio status label. Runs on the main thread via frame.after()."""
        messages = {
            "loading": "Loading preview…",
            "playing": "▶  Playing…",
            "done": "",
            "unavailable": "No preview available for this track.",
        }
        self.frame.audio_status.config(text=messages.get(status, ""))

        # Disable the play button while audio is actively loading or playing
        # so the user can't stack multiple simultaneous downloads
        if status in ("loading", "playing"):
            self.frame.play_btn.config(state="disabled")
        else:
            self.frame.play_btn.config(state="normal")

    def _answer(self, chosen: str):
        # Stop the preview — the answer has been given, no need to keep playing
        self._audio.stop()
        self.frame.play_btn.config(state="disabled")

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
        self._audio.stop()
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
        self.frame.audio_status.config(text="")
        self.frame.feedback_label.config(text="")
        self.frame.play_btn.config(state="disabled")
        for btn in self.frame.choice_btns:
            btn.grid_remove()
        self.frame.next_btn.config(text="Back to Home", command=self._back_home)
        self.frame.next_btn.grid()

    def _back_home(self):
        for btn in self.frame.choice_btns:
            btn.grid()
            btn.config(bg="SystemButtonFace")
        self.frame.play_btn.config(state="normal")
        self.view.switch("home")
