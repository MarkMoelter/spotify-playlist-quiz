import spotipy


def playlist_from_api(
        api_client: spotipy.Spotify,
        playlist_id: str,
        limit: int = 50,

) -> dict:
    """
    Gather the items from a specified playlist using a spotify API client.

    :param api_client: API client for spotify.
    :param playlist_id: The id of the playlist to retrieve
    :param limit: The maximum number of items to retrieve
    :return: A dictionary of the playlist items
    """
    return api_client.playlist_items(playlist_id, limit=limit)
