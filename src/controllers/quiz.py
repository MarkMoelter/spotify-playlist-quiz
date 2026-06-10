import random
import threading

from src.exceptions import NetworkError, PlaylistError
from src.models.track import Track
from src.views import theme

PLAYBACK_SECONDS = 15


class QuizController:
    def __init__(self, model, leaderboard_model, view):
        self.model = model
        self.lb = leaderboard_model
        self.view = view
        self.frame = self.view.frames["quiz"]
        self._tracks: list[Track] = []
        self._questions: list[dict] = []
        self._current: int = 0
        self._score: int = 0
        self._pause_timer: threading.Timer | None = None
        self._show_artist: bool = True
        self._playlist_name: str = ""

    def start(self, tracks: list[Track], show_artist: bool = True,
              num_questions: int = 10, playlist_name: str = ""):
        self._tracks = tracks
        self._show_artist = show_artist
        self._playlist_name = playlist_name
        n = min(num_questions, len(tracks))
        selected = random.sample(tracks, n)
        self._questions = [self.model.build_question(tracks, correct=t) for t in selected]
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
        self.frame.progress_bar["maximum"] = total
        self.frame.progress_bar["value"] = self._current
        self.frame.prompt.config(text="Listen to the track — which song is it?")
        self.frame.artist_label.config(
            text=f"Artist:  {q['track'].artists[0]}" if self._show_artist
            else "Artist hidden — can you guess?"
        )
        self.frame.feedback_label.config(text="", fg=theme.TEXT)
        self.frame.audio_status.config(text="")
        self.frame.next_btn.grid_remove()

        for i, btn in enumerate(self.frame.choice_btns):
            choice = q["choices"][i] if i < len(q["choices"]) else ""
            btn.config(text=choice, style="Choice.TButton", state="normal",
                       command=lambda c=choice: self._answer(c))

        self.frame.play_btn.config(state="normal",
                                   command=lambda: self._play(q["track"].uri))
        self._play(q["track"].uri)

    # ── Playback ──────────────────────────────────────────────────────────────

    def _play(self, uri: str):
        self._cancel_pause_timer()
        self.frame.play_btn.config(state="disabled")
        self.frame.audio_status.config(text="Starting playback…")
        threading.Thread(target=self._do_play, args=(uri,), daemon=True).start()

    def _do_play(self, uri: str):
        try:
            self.model.play_track(uri, self.model.get_active_device())
            self.frame.after(0, self._on_playing)
        except (NetworkError, PlaylistError) as e:
            self.frame.after(0, self._on_play_error, str(e))

    def _on_playing(self):
        self.frame.audio_status.config(
            text=f"▶  Playing…  (pauses in {PLAYBACK_SECONDS}s)")
        self.frame.play_btn.config(state="normal")
        self._pause_timer = threading.Timer(PLAYBACK_SECONDS, self._auto_pause)
        self._pause_timer.daemon = True
        self._pause_timer.start()

    def _auto_pause(self):
        self.model.pause_playback()
        self.frame.after(0, self.frame.audio_status.config,
                         {"text": "⏸  Paused — make your guess!"})

    def _on_play_error(self, message: str):
        self.frame.audio_status.config(text=message)
        self.frame.play_btn.config(state="normal")

    def _cancel_pause_timer(self):
        if self._pause_timer:
            self._pause_timer.cancel()
            self._pause_timer = None

    # ── Answering ─────────────────────────────────────────────────────────────

    def _answer(self, chosen: str):
        self._cancel_pause_timer()
        threading.Thread(target=self.model.pause_playback, daemon=True).start()
        self.frame.play_btn.config(state="disabled")
        self.frame.audio_status.config(text="")

        q = self._questions[self._current]
        correct = q["answer"]

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

        if not self._show_artist:
            self.frame.artist_label.config(text=f"Artist:  {q['track'].artists[0]}")

        last = self._current == len(self._questions) - 1
        self.frame.next_btn.config(
            text="See Results" if last else "Next  →",
            command=self._finish if last else self._next,
        )
        self.frame.next_btn.grid()

    def _next(self):
        self._current += 1
        self._show_question()

    # ── Results ───────────────────────────────────────────────────────────────

    def _finish(self):
        self._cancel_pause_timer()
        threading.Thread(target=self.model.pause_playback, daemon=True).start()

        total = len(self._questions)
        pct = self._score * 100 // total
        rating = (
            "Perfect! 🎯" if pct == 100
            else "Great job! 🎵" if pct >= 70
            else "Not bad! 👍" if pct >= 40
            else "Keep listening! 🎧"
        )

        # Save to leaderboard before showing results
        self.lb.save(
            playlist=self._playlist_name,
            score=self._score,
            total=total,
            show_artist=self._show_artist,
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

        # Show two buttons: view leaderboard or go home
        self.frame.next_btn.config(text="🏆 Leaderboard",
                                   command=self._view_leaderboard)
        self.frame.next_btn.grid()
        self.frame.home_btn.grid()

    def _view_leaderboard(self):
        self._reset_choice_btns()
        # Delegate to leaderboard controller via the view callback
        if self.view._on_show_leaderboard:
            self.view._on_show_leaderboard()

    def _back_home(self):
        self._reset_choice_btns()
        self.view.switch("home")

    def _reset_choice_btns(self):
        for btn in self.frame.choice_btns:
            btn.grid()
            btn.config(style="Choice.TButton")
        self.frame.play_btn.config(state="normal")
        self.frame.home_btn.grid_remove()
