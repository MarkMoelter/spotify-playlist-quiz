from src.audio import AudioPlayer
from src.models.track import Track
from src.views import theme

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
        # Bridge background-thread status updates to the Tkinter main thread
        self._audio.on_status = lambda s: self.frame.after(0, self._on_audio_status, s)

    def start(self, tracks: list[Track]):
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
            text=f"Question {self._current + 1} of {total}  ·  Score: {self._score}"
        )
        # Progress bar tracks how far through the quiz we are
        self.frame.progress_bar["maximum"] = total
        self.frame.progress_bar["value"] = self._current

        self.frame.prompt.config(text="Listen to the preview — which song is it?")
        self.frame.artist_label.config(text=f"Artist:  {q['track'].artists[0]}")
        self.frame.feedback_label.config(text="", fg=theme.TEXT)
        self.frame.audio_status.config(text="")
        self.frame.next_btn.grid_remove()

        for i, btn in enumerate(self.frame.choice_btns):
            choice = q["choices"][i] if i < len(q["choices"]) else ""
            btn.config(text=choice, style="Choice.TButton",
                       state="normal",
                       command=lambda c=choice: self._answer(c))

        preview_url = q["track"].preview_url
        self.frame.play_btn.config(state="normal",
                                   command=lambda: self._audio.play(preview_url))
        self._audio.play(preview_url)

    def _on_audio_status(self, status: str):
        messages = {
            "loading":     "Loading preview…",
            "playing":     "▶  Playing…",
            "done":        "",
            "unavailable": "No preview available for this track.",
        }
        self.frame.audio_status.config(text=messages.get(status, ""))
        # Prevent stacking multiple downloads by disabling the button while busy
        busy = status in ("loading", "playing")
        self.frame.play_btn.config(state="disabled" if busy else "normal")

    def _answer(self, chosen: str):
        self._audio.stop()
        self.frame.play_btn.config(state="disabled")

        q = self._questions[self._current]
        correct = q["answer"]

        # ttk buttons can't take bg= directly — we swap named styles instead.
        # The styles "Correct.TButton" and "Wrong.TButton" are defined in theme.py.
        for btn in self.frame.choice_btns:
            btn.config(state="disabled")
            if btn["text"] == correct:
                btn.config(style="Correct.TButton")
            elif btn["text"] == chosen and chosen != correct:
                btn.config(style="Wrong.TButton")

        if chosen == correct:
            self._score += 1
            self.frame.feedback_label.config(text="✓  Correct!", fg=theme.SUCCESS)
        else:
            self.frame.feedback_label.config(
                text=f'✗  Wrong — it was "{correct}"', fg=theme.DANGER)

        last = self._current == len(self._questions) - 1
        self.frame.next_btn.config(
            text="See Results" if last else "Next  →",
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
            "Perfect! 🎯" if pct == 100
            else "Great job! 🎵" if pct >= 70
            else "Not bad! 👍" if pct >= 40
            else "Keep listening! 🎧"
        )
        self.frame.progress_bar["value"] = total
        self.frame.progress_label.config(
            text=f"Score: {self._score}/{total}  ({pct}%)  —  {rating}"
        )
        self.frame.prompt.config(text="Quiz complete!")
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
            btn.config(style="Choice.TButton")
        self.frame.play_btn.config(state="normal")
        self.view.switch("home")
