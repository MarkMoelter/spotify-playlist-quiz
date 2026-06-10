from tkinter import Frame, Label
from tkinter import ttk
from . import theme


class SignInView(Frame):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, bg=theme.BG, **kwargs)

        self.grid_columnconfigure(0, weight=1)

        Label(self, text="🎵  Spotify Playlist Quiz", **theme.LABEL_KW,
              font=theme.FONT_TITLE).grid(row=0, column=0, pady=(60, 8))

        Label(self, text="Connect your Spotify account to start.",
              **theme.LABEL_DIM).grid(row=1, column=0, pady=(0, 30))

        self.signin_btn = ttk.Button(self, text="Connect with Spotify",
                                     style="Green.TButton")
        self.signin_btn.grid(row=2, column=0, pady=6, ipadx=10)

        self.status_label = Label(self, text="", **theme.LABEL_DIM)
        self.status_label.grid(row=3, column=0, pady=(10, 0))
