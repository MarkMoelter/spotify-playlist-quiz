from tkinter import Frame, Label, Button


class QuizView(Frame):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.grid_columnconfigure(0, weight=1)

        # Progress / score bar
        self.progress_label = Label(self, text="")
        self.progress_label.grid(row=0, column=0, padx=10, pady=(10, 0))

        # Prompt: "Which song is this?"
        self.prompt = Label(self, text="", wraplength=460)
        self.prompt.grid(row=1, column=0, padx=10, pady=(10, 4))

        # Artist hint
        self.artist_label = Label(self, text="", font=("", 10, "italic"))
        self.artist_label.grid(row=2, column=0, padx=10, pady=(0, 6))

        # Audio controls — play button + status shown side by side
        self.play_btn = Button(self, text="▶  Play Preview")
        self.play_btn.grid(row=3, column=0, pady=(0, 2))

        # Status tells the user what's happening with audio
        # ("Loading…", "Playing…", "No preview available", "")
        self.audio_status = Label(self, text="", font=("", 9, "italic"))
        self.audio_status.grid(row=4, column=0, pady=(0, 8))

        # Four answer buttons
        self.choice_btns: list[Button] = []
        for i in range(4):
            btn = Button(self, text="", wraplength=440, justify="left")
            btn.grid(row=5 + i, column=0, padx=30, pady=4, sticky="ew")
            self.choice_btns.append(btn)

        # Feedback label shown after answering
        self.feedback_label = Label(self, text="")
        self.feedback_label.grid(row=9, column=0, padx=10, pady=6)

        # Next question / finish button (hidden until answer chosen)
        self.next_btn = Button(self, text="Next")
        self.next_btn.grid(row=10, column=0, pady=(4, 10))
        self.next_btn.grid_remove()
