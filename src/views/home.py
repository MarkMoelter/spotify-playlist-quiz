from tkinter import Frame, Label
from tkinter import ttk
from . import theme


class HomeView(Frame):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, bg=theme.BG, **kwargs)

        self.grid_columnconfigure(1, weight=1)

        # ── Top bar: greeting left, title centre, sign-out right ──────────────
        self.greeting = Label(self, text="", **theme.LABEL_DIM)
        self.greeting.grid(row=0, column=0, padx=(16, 8), pady=14, sticky="w")

        Label(self, text="Spotify Quiz", **theme.LABEL_KW,
              font=theme.FONT_HEADER).grid(row=0, column=1, pady=14)

        self.signout_btn = ttk.Button(self, text="Sign Out", style="Sub.TButton")
        self.signout_btn.grid(row=0, column=2, padx=(8, 16), pady=14)

        # ── Divider ───────────────────────────────────────────────────────────
        ttk.Separator(self, orient="horizontal").grid(
            row=1, column=0, columnspan=3, sticky="ew", padx=16)

        # ── Playlist selector ─────────────────────────────────────────────────
        Label(self, text="Choose a playlist", **theme.LABEL_KW,
              font=theme.FONT_HEADER).grid(
            row=2, column=0, columnspan=3, pady=(24, 8))

        self.playlists = ttk.Combobox(self, state="readonly", width=36)
        self.playlists.grid(row=3, column=0, columnspan=2,
                            padx=(16, 8), pady=4, sticky="ew")

        self.select_playlist_btn = ttk.Button(self, text="Start Quiz →",
                                              style="Green.TButton")
        self.select_playlist_btn.grid(row=3, column=2, padx=(0, 16), pady=4)
