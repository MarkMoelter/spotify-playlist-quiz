import threading


class SignInController:
    def __init__(self, model, view):
        self.model = model
        self.view = view
        self.frame = self.view.frames["signin"]
        self._bind()

    def _bind(self):
        self.frame.signin_btn.config(command=self.signin)

    def signin(self):
        self.frame.signin_btn.config(state="disabled")
        self.frame.status_label.config(text="Opening Spotify login in your browser…")
        # Run OAuth in a background thread so the Tkinter loop stays responsive
        threading.Thread(target=self._do_oauth, daemon=True).start()

    def _do_oauth(self):
        try:
            self.model.connect()
        except Exception as e:
            self.frame.after(0, self._on_error, str(e))

    def _on_error(self, message: str):
        self.frame.status_label.config(text=f"Error: {message}")
        self.frame.signin_btn.config(state="normal")
