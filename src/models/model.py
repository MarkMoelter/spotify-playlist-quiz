import spotipy

from .auth import Auth


class Model:
    def __init__(self):
        self.auth = Auth()

    @staticmethod
    def get_client() -> spotipy.Spotify:
        """Authorize an API token using the user's credentials"""

        oauth = spotipy.SpotifyOAuth()
        access_token = oauth.get_access_token(as_dict=False)
        return spotipy.Spotify(auth=access_token)

    def user_playlists(self) -> list[dict]:
        """Get each of the user's playlists as a dictionary of the name and the uri."""
        raise NotImplementedError

    def playlist_by_id(self, playlist_id: str, track_limit: int = 50) -> dict:
        """Get a single playlist by its id.

        :param playlist_id: The id of the playlist to retrieve
        :param track_limit: The maximum number of items to retrieve
        :return: A dictionary of the playlist items
        """
        return self.client.playlist_items(playlist_id, limit=track_limit)
