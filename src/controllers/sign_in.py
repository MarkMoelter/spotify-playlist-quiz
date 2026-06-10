import logging
import threading

from src.exceptions import AuthError, NetworkError

logger = logging.getLogger("my_app")


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
        threading.Thread(target=self._do_oauth, daemon=True).start()

    def _do_oauth(self):
        try:
            self.model.connect()
            # Success — auth_changed event fires automatically via Auth.login(),
            # which triggers Controller._auth_state_listener to switch screens.
        except (AuthError, NetworkError) as e:
            # Expected: bad credentials, no network, user closed the browser, etc.
            self.frame.after(0, self._on_error, str(e))
        except Exception:
            # Unexpected: log full traceback for the developer, show generic message
            logger.exception("Unexpected error during OAuth")
            self.frame.after(0, self._on_error,
                             "An unexpected error occurred. Check the logs.")

    def reset(self):
        """Restore the sign-in screen to its initial state — called on logout."""
        self.frame.signin_btn.config(state="normal")
        self.frame.status_label.config(text="")

    def _on_error(self, message: str):
        self.frame.status_label.config(text=message)
        self.frame.signin_btn.config(state="normal")
