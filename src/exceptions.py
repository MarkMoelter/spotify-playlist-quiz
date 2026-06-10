"""
App-level exceptions.

These sit between raw library errors (spotipy, network) and the UI.
Controllers catch these and translate them into user-facing messages.
Unexpected exceptions (bugs) are NOT caught here — they bubble up so
the developer can see them in logs.
"""


class SpotifyQuizError(Exception):
    """Base class — catch this if you want to handle any app error."""


class AuthError(SpotifyQuizError):
    """OAuth failed or credentials are missing/invalid."""


class NetworkError(SpotifyQuizError):
    """A network request failed (timeout, no connection, etc.)."""


class PlaylistError(SpotifyQuizError):
    """A playlist could not be loaded or has too few tracks."""
