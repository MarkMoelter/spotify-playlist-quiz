from tkinter import BooleanVar, Frame, Label
from tkinter import ttk
from . import theme


class HomeView(Frame):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, bg=theme.BG, **kwargs)

        self.grid_columnconfigure(1, weight=1)

        # ── Top bar: greeting left, title centre, sign-out right ──────────────
        self.greeting = Label(self, text="", **theme.LABEL_DIM)
        self.greeting.grid(row=0, column=0, padx=(16, 8), pady=14, sticky="w")

        Label(self, text="Spotify Quiz",
              **theme.LABEL_BASE, font=theme.FONT_HEADER).grid(row=0, column=1, pady=14)

        self.signout_btn = ttk.Button(self, text="Sign Out", style="Sub.TButton")
        self.signout_btn.grid(row=0, column=2, padx=(8, 16), pady=14)

        # ── Divider ───────────────────────────────────────────────────────────
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
            row=5, column=0, columnspan=3, sticky="ew", padx=16, pady=(16, 0))

        Label(self, text="Settings", **theme.LABEL_DIM).grid(
            row=6, column=0, columnspan=3, pady=(8, 4))

        # BooleanVar so the controller can read the value without touching tkinter
        self.show_artist = BooleanVar(value=True)
        self.show_artist_chk = ttk.Checkbutton(
            self,
            text="Show artist name during quiz",
            variable=self.show_artist,
            onvalue=True, offvalue=False,
        )
        self.show_artist_chk.grid(row=7, column=0, columnspan=3, pady=(0, 8))

        # Status label: shows loading states and error messages
        self.status_label = Label(self, text="", **theme.LABEL_DIM)
        self.status_label.grid(row=8, column=0, columnspan=3, pady=(4, 0))
