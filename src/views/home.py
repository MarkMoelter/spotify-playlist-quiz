from tkinter import BooleanVar, Frame, Label
from tkinter import ttk
from . import theme

QUIZ_LENGTHS = [5, 10, 15, 20]


class HomeView(Frame):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, bg=theme.BG, **kwargs)

        self.grid_columnconfigure(1, weight=1)

        # ── Top bar ───────────────────────────────────────────────────────────
        self.greeting = Label(self, text="", **theme.LABEL_DIM)
        self.greeting.grid(row=0, column=0, padx=(16, 8), pady=14, sticky="w")

        Label(self, text="Spotify Quiz",
              **theme.LABEL_BASE, font=theme.FONT_HEADER).grid(row=0, column=1, pady=14)

        self.signout_btn = ttk.Button(self, text="Sign Out", style="Sub.TButton")
        self.signout_btn.grid(row=0, column=2, padx=(8, 16), pady=14)

        ttk.Separator(self, orient="horizontal").grid(
            row=1, column=0, columnspan=3, sticky="ew", padx=16)

        # ── Playlist selector ─────────────────────────────────────────────────
        Label(self, text="Choose a playlist",
              **theme.LABEL_BASE, font=theme.FONT_HEADER).grid(
            row=2, column=0, columnspan=3, pady=(24, 8))

        self.playlists = ttk.Combobox(self, state="readonly", width=36)
        self.playlists.grid(row=3, column=0, columnspan=2,
                            padx=(16, 8), pady=4, sticky="ew")

        self.select_playlist_btn = ttk.Button(self, text="Start Quiz →",
                                              style="Green.TButton")
        self.select_playlist_btn.grid(row=3, column=2, padx=(0, 16), pady=4)

        # ── Settings ──────────────────────────────────────────────────────────
        ttk.Separator(self, orient="horizontal").grid(
            row=4, column=0, columnspan=3, sticky="ew", padx=16, pady=(16, 0))

        Label(self, text="Settings",
              **theme.LABEL_BASE, font=theme.FONT_HEADER).grid(
            row=5, column=0, columnspan=3, pady=(10, 6))

        settings_frame = Frame(self, bg=theme.BG)
        settings_frame.grid(row=6, column=0, columnspan=3, pady=(0, 8))

        # Quiz length
        Label(settings_frame, text="Questions per quiz:", **theme.LABEL_KW).grid(
            row=0, column=0, padx=(0, 8), sticky="w")
        self.quiz_length = ttk.Combobox(
            settings_frame,
            values=[str(n) for n in QUIZ_LENGTHS],
            state="readonly",
            width=5,
        )
        self.quiz_length.set("10")
        self.quiz_length.grid(row=0, column=1, padx=(0, 24))

        # Artist hint toggle
        self.show_artist = BooleanVar(value=True)
        ttk.Checkbutton(
            settings_frame,
            text="Show artist name during quiz",
            variable=self.show_artist,
            onvalue=True, offvalue=False,
        ).grid(row=0, column=2)

        # ── Bottom bar: status left, leaderboard right ────────────────────────
        bottom = Frame(self, bg=theme.BG)
        bottom.grid(row=7, column=0, columnspan=3, sticky="ew", padx=16, pady=(4, 12))
        bottom.grid_columnconfigure(0, weight=1)

        self.status_label = Label(bottom, text="", **theme.LABEL_DIM)
        self.status_label.grid(row=0, column=0, sticky="w")

        self.leaderboard_btn = ttk.Button(bottom, text="🏆 Leaderboard",
                                          style="Sub.TButton")
        self.leaderboard_btn.grid(row=0, column=1, sticky="e")
