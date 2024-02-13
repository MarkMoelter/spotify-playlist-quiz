import os

import spotipy  # type: ignore

from .auth import Auth
from .track import Track


class Model:
    def __init__(self):
        self.auth = Auth()

    @staticmethod
    def get_client() -> spotipy.Spotify:
        """Authorize an API token using the user's credentials"""

        client_id = os.getenv('SPOTIPY_CLIENT_ID')
        client_secret = os.getenv('SPOTIPY_CLIENT_SECRET')
        redirect_url = os.getenv('REDIRECT_URI')

        oauth = spotipy.SpotifyOAuth(client_id, client_secret, redirect_url)
        access_token = oauth.get_access_token(as_dict=False)
        return spotipy.Spotify(auth=access_token)

    def user_playlists(self) -> list[dict]:
        """
        Get each of the user's playlists as
        a dictionary of the name and the uri.
        :return: A list of the user's playlists.
        """
        raise NotImplementedError

    def playlist_by_id(self, playlist_id: str, track_limit: int = 50) -> dict:
        """Get a single playlist by its id.

        :param playlist_id: The id of the playlist to retrieve
        :param track_limit: The maximum number of items to retrieve
        :return: A dictionary of the playlist items
        """
        return self.get_client().playlist_items(playlist_id, limit=track_limit)

    def parse_raw_playlist(self,
                           playlist_id: str,
                           limit: int = 100) -> list[Track]:
        """
        Convert the raw dictionary into a list of songs.

        :param playlist_id: The identifier of the playlist.
        :param limit: The maximum number of items to return.
        :return: A list of tracks.
        """
        songs = []
        playlist = self.get_client().playlist_items(playlist_id, limit=limit)
        for track in playlist['items']:
            track_info = track['track']

            name = track_info['name']
            album = track_info['album']

            # collect all artists for a track
            artists = [artist['name'] for artist in track_info['artists']]

            songs.append(Track(name, album, artists))
        return songs
