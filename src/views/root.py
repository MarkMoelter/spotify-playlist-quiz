from tkinter import Tk
from . import theme


class Root(Tk):
    def __init__(self):
        super().__init__()

        self.geometry("520x420")
        self.minsize(width=440, height=360)
        self.title("Spotify Playlist Quiz")
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)

        # Apply once here — ttk.Style is global so every ttk widget picks it up
        theme.apply(self)
