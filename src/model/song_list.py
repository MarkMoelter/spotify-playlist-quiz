import spotipy

import song


def get_playlist(
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


def song_list(playlist_dict: dict) -> list[song.Song]:
    """Convert the playlist into a list of song objects"""
    songs = []
    for track in playlist_dict['items']:
        name = track['track']['name']
        album = track['track']['album']

        # collect all artists for a track
        artists = []
        for artist in track['track']['artists']:
            artists.append(artist['name'])

        songs.append(song.Song(name, album, artists))

    return songs
