import tempfile
import threading
import urllib.request

# pygame is only imported once and initialised once — it's expensive to set up.
# We do it lazily the first time play() is called rather than at import time,
# so importing this module doesn't slow down the app if audio is never used.
_pygame_ready = False


def _ensure_pygame():
    global _pygame_ready
    if not _pygame_ready:
        import pygame
        pygame.mixer.init()
        _pygame_ready = True


class AudioPlayer:
    """Download and play a Spotify preview URL (30-second MP3).

    All network and playback work runs on a background thread so the
    Tkinter main thread is never blocked.
    """

    def __init__(self):
        self._lock = threading.Lock()
        self._current_thread: threading.Thread | None = None
        # Callback signatures:
        #   on_status(str)  — called with "loading", "playing", "done", "unavailable"
        self.on_status = None

    def play(self, url: str | None):
        """Stop any current playback and start playing the given URL.

        Passing None (no preview available) immediately reports "unavailable".
        """
        self.stop()

        if not url:
            self._notify("unavailable")
            return

        # daemon=True means this thread won't prevent the app from closing
        t = threading.Thread(target=self._download_and_play, args=(url,), daemon=True)
        with self._lock:
            self._current_thread = t
        t.start()

    def stop(self):
        """Stop playback immediately. Safe to call even if nothing is playing."""
        if not _pygame_ready:
            return
        import pygame
        # stop() is thread-safe per pygame docs
        pygame.mixer.music.stop()

    def _download_and_play(self, url: str):
        self._notify("loading")
        try:
            # Write the MP3 to a temp file — pygame needs a file path, not raw bytes.
            # delete=False because pygame holds the file open while playing;
            # we clean it up manually in the finally block after playback ends.
            with tempfile.NamedTemporaryFile(suffix=".mp3", delete=False) as f:
                tmp_path = f.name
                urllib.request.urlretrieve(url, tmp_path)

            _ensure_pygame()
            import pygame

            pygame.mixer.music.load(tmp_path)
            pygame.mixer.music.play()
            self._notify("playing")

            # Block this background thread until the clip finishes or is stopped.
            # We poll instead of using pygame events because pygame's event system
            # is not safe to use from a non-main thread on all platforms.
            clock = pygame.time.Clock()
            while pygame.mixer.music.get_busy():
                clock.tick(10)  # check 10 times per second, low CPU cost

            self._notify("done")
        except Exception:
            self._notify("unavailable")
        finally:
            # Clean up the temp file whether playback succeeded or not
            import os
            try:
                os.unlink(tmp_path)
            except Exception:
                pass

    def _notify(self, status: str):
        if self.on_status:
            self.on_status(status)
