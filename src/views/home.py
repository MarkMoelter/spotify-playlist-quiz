from tkinter import Frame, Label, Button
from tkinter import ttk


class HomeView(Frame):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.grid_columnconfigure(0, weight=1)

        self.greeting = Label(self, text="")
        self.greeting.grid(row=0, column=0, padx=10, pady=10, sticky="ew")

        self.header = Label(self, text="Song Quiz")
        self.header.grid(row=0, column=1, padx=10, pady=10, sticky="ew")

        self.signout_btn = Button(self, text="Sign Out")
        self.signout_btn.grid(row=0, column=2, padx=10, pady=10)

        self.playlist_cb = Label(self, text="Playlists")
        self.playlist_cb.grid(row=1, column=0, padx=10, pady=10, sticky="ew")

        self.playlists = ttk.Combobox(self)
        self.playlists.grid(row=1, column=1, padx=10, pady=10, sticky="ew")

        self.select_playlist_btn = Button(self, text="Select Playlist")
        self.select_playlist_btn.grid(row=1, column=2, padx=10, pady=10)
