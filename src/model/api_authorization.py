import spotipy


def api_authorization(
        client_id: str,
        client_secret: str,
        redirect_uri: str
) -> spotipy.Spotify:
    """
    Use API IDs to create a spotify object.

    :return: Spotify client object
    """
    token = spotipy.SpotifyOAuth(client_id, client_secret, redirect_uri).get_access_token(as_dict=False)
    return spotipy.Spotify(auth=token)
