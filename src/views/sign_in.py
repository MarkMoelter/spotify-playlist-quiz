from tkinter import Frame, Label, Button


class SignInView(Frame):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.grid_columnconfigure(0, weight=1)

        self.header = Label(self, text="Spotify Playlist Quiz")
        self.header.grid(row=0, column=0, padx=10, pady=(40, 10))

        self.subheader = Label(self, text="Connect your Spotify account to start.")
        self.subheader.grid(row=1, column=0, padx=10, pady=(0, 20))

        self.signin_btn = Button(self, text="Connect with Spotify")
        self.signin_btn.grid(row=2, column=0, padx=10, pady=10)

        self.status_label = Label(self, text="")
        self.status_label.grid(row=3, column=0, padx=10, pady=10)
