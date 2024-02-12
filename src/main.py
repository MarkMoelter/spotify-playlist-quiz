import json

import spotipy

from src import secrets
from track import Track

test_playlist_id = '0MiNiiLm7aSYZGW5RV3kR5'
total_songs = 100


def main():
    playlist = authorization(
        secrets.client_id,
        secrets.client_secret,
        secrets.redirect_uri
    ).playlist_items(test_playlist_id, limit=100)

    print(json.dumps(playlist, indent=4))

    song_idx = 72

    track = Track(playlist, song_idx)

    print(track.name)
    print(track.album)
    print(track.artists)


def authorization(client_id, client_secret, redirect_uri) -> spotipy.Spotify:
    """
    Use the API IDs to create a spotify object.

    :return: Spotify client object
    """
    token = spotipy.SpotifyOAuth(
        client_id, client_secret, redirect_uri
    ).get_access_token(as_dict=False)

    return spotipy.Spotify(auth=token)


type Song = str
type Artists = list[str]

if __name__ == '__main__':
    main()
