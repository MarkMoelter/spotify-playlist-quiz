from tkinter import Frame, Label, Entry, Checkbutton, BooleanVar
from tkinter import ttk
from . import theme


class SignUpView(Frame):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, bg=theme.BG, **kwargs)

        self.grid_columnconfigure(0, weight=0)
        self.grid_columnconfigure(1, weight=1)

        Label(self, text="Create a new account",
              **theme.LABEL_BASE, font=theme.FONT_HEADER).grid(
            row=0, column=0, columnspan=2, pady=(20, 16))

        for row, field in enumerate(["Full Name", "Username"], start=1):
            Label(self, text=field, **theme.LABEL_KW).grid(
                row=row, column=0, padx=(20, 8), pady=4, sticky="w")

        self.fullname_input = Entry(self, bg=theme.SURFACE, fg=theme.TEXT,
                                    insertbackground=theme.TEXT, relief="flat")
        self.fullname_input.grid(row=1, column=1, padx=(0, 20), pady=4, sticky="ew")

        self.username_input = Entry(self, bg=theme.SURFACE, fg=theme.TEXT,
                                    insertbackground=theme.TEXT, relief="flat")
        self.username_input.grid(row=2, column=1, padx=(0, 20), pady=4, sticky="ew")

        Label(self, text="Password", **theme.LABEL_KW).grid(
            row=3, column=0, padx=(20, 8), pady=4, sticky="w")
        self.password_input = Entry(self, show="*", bg=theme.SURFACE, fg=theme.TEXT,
                                    insertbackground=theme.TEXT, relief="flat")
        self.password_input.grid(row=3, column=1, padx=(0, 20), pady=4, sticky="ew")

        self.has_agreed = BooleanVar()
        self.agreement = Checkbutton(
            self,
            text="I've agreed to the Terms & Conditions",
            variable=self.has_agreed,
            onvalue=True, offvalue=False,
            bg=theme.BG, fg=theme.TEXT_DIM,
            selectcolor=theme.SURFACE,
            activebackground=theme.BG,
            font=theme.FONT_BODY,
        )
        self.agreement.grid(row=4, column=1, padx=0, pady=(8, 4), sticky="w")

        self.signup_btn = ttk.Button(self, text="Sign Up", style="Green.TButton")
        self.signup_btn.grid(row=5, column=1, pady=(4, 12), sticky="w")

        Label(self, text="Already have an account?", **theme.LABEL_DIM).grid(
            row=6, column=1, sticky="w", pady=(0, 2))
        self.signin_btn = ttk.Button(self, text="Sign In", style="Sub.TButton")
        self.signin_btn.grid(row=7, column=1, sticky="w", pady=(0, 16))
