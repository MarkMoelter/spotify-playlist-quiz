import spotipy


class Model:
    def __init__(self, client_id: str, client_secret: str, redirect_uri: str):
        self.client_id = client_id
        self.client_secret = client_secret
        self.redirect_uri = redirect_uri

    def spotify_client(self) -> spotipy.Spotify:
        """Authorize an API token using the user's credentials"""

        oauth = spotipy.SpotifyOAuth(self.client_id, self.client_secret, self.redirect_uri)
        access_token = oauth.get_access_token(as_dict=False)
        return spotipy.Spotify(auth=access_token)

    def all_user_playlists(self) -> list[dict]:
        """Get each of the user's playlists"""
        raise NotImplementedError

    def get_user_playlist(self, playlist_id: str, track_limit: int = 50) -> dict:
        """Get a single playlist by its id.

        :param playlist_id: The id of the playlist to retrieve
        :param track_limit: The maximum number of items to retrieve
        :return: A dictionary of the playlist items
        """
        client = self.spotify_client()
        return client.playlist_items(playlist_id, limit=track_limit)
