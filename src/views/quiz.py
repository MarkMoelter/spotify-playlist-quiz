from tkinter import Frame, Label
from tkinter import ttk
from . import theme


class QuizView(Frame):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, bg=theme.BG, **kwargs)

        self.grid_columnconfigure(0, weight=1)

        # ── Progress bar + score ──────────────────────────────────────────────
        self.progress_label = Label(self, text="", **theme.LABEL_DIM)
        self.progress_label.grid(row=0, column=0, pady=(12, 0))

        self.progress_bar = ttk.Progressbar(self, orient="horizontal",
                                            mode="determinate", length=460)
        self.progress_bar.grid(row=1, column=0, padx=30, pady=(4, 10), sticky="ew")

        # ── Prompt ────────────────────────────────────────────────────────────
        self.prompt = Label(self, text="", wraplength=460,
                            **theme.LABEL_BASE, font=theme.FONT_HEADER)
        self.prompt.grid(row=2, column=0, padx=10, pady=(4, 2))

        self.artist_label = Label(self, text="", **theme.LABEL_DIM)
        self.artist_label.grid(row=3, column=0, padx=10, pady=(0, 8))

        # ── Audio controls ────────────────────────────────────────────────────
        self.play_btn = ttk.Button(self, text="▶  Play Preview",
                                   style="Sub.TButton")
        self.play_btn.grid(row=4, column=0, pady=(0, 2))

        self.audio_status = Label(self, text="", **theme.LABEL_DIM)
        self.audio_status.grid(row=5, column=0, pady=(0, 10))

        # ── Answer buttons ────────────────────────────────────────────────────
        # We store the style name alongside the button so the controller can
        # swap styles (Choice → Correct / Wrong) without touching geometry.
        self.choice_btns: list[ttk.Button] = []
        for i in range(4):
            btn = ttk.Button(self, text="", style="Choice.TButton")
            btn.grid(row=6 + i, column=0, padx=40, pady=3, sticky="ew")
            self.choice_btns.append(btn)

        # ── Feedback + next ───────────────────────────────────────────────────
        self.feedback_label = Label(self, text="",
                                    **theme.LABEL_BASE, font=("Helvetica", 11, "bold"))
        self.feedback_label.grid(row=10, column=0, pady=(8, 2))

        self.next_btn = ttk.Button(self, text="Next", style="Green.TButton")
        self.next_btn.grid(row=11, column=0, pady=(4, 4))
        self.next_btn.grid_remove()

        # "Back to Home" shown alongside leaderboard button on results screen
        self.home_btn = ttk.Button(self, text="← Home", style="Sub.TButton")
        self.home_btn.grid(row=12, column=0, pady=(0, 12))
        self.home_btn.grid_remove()
