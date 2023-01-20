import tkinter as tk
from tkinter import ttk


class View(tk.Frame):
    def __init__(self, root):
        super().__init__(root)
        self.root = root

    def render_title_page(self, playlists: tuple[str, ...]):
        """Display the title page and its elements."""
        title_label = tk.Label(self, text='Playlist Quiz')
        question_radio = tk.Radiobutton(self, text='Questions')

        # playlist selection
        n = tk.StringVar(self)
        playlist_select = ttk.Combobox(self, textvariable=n)
        playlist_select['values'] = playlists
        playlist_select.current()

        start = tk.Button(self, text='Start Quiz')
