import json

import spotipy

import api_secrets
from track_data import TrackData

test_playlist_id = '0MiNiiLm7aSYZGW5RV3kR5'
total_songs = 100


def track_artist(playlist_items: dict, song_idx: int) -> list[str]:
    """
    Get the artist for a track given the playlist and song index.

    :param playlist_items: Items within the playlist
    :param song_idx: The index for the song you want to reference.
    :return: The artist of the indexed song.
    """

    artist_list = playlist_items['items'][song_idx]['track']['artists']
    return [artist['name'] for artist in artist_list]


def track_name(playlist_items: dict, song_idx: int) -> str:
    """
    Get the song for a track given the playlist and song index.

    :param playlist_items: Items within the playlist
    :param song_idx: The index for the song you want to reference.
    :return: The name of the indexed song.
    """
    return playlist_items['items'][song_idx]['track']['name']


def authorization(client_id, client_secret, redirect_uri) -> spotipy.Spotify:
    """
    Use the API IDs to create a spotify object.

    :return: Spotify client object
    """
    token = spotipy.SpotifyOAuth(
        client_id, client_secret, redirect_uri
    ).get_access_token(as_dict=False)

    return spotipy.Spotify(auth=token)


def quiz_dict(track_limit) -> dict:
    """
    Simplify the spotify playlist data into track name and artist.
    Store in a dictionary with the following format. [Name: Artist]

    :param track_limit: Number of tracks in the playlist to retrieve.
    :return: Dictionary containing track names and artists.
    """
    spot_obj = authorization(
        api_secrets.client_id,
        api_secrets.client_secret,
        api_secrets.redirect_uri
    )

    # generate the full list of tracks in the playlist
    playlist_dict = spot_obj.playlist_items(test_playlist_id, limit=track_limit)

    # create dict of track: artist
    return {
        track_name(playlist_dict, song_number):
            track_artist(playlist_dict, song_number)
        for song_number in range(track_limit)
    }


def main():
    song_dict = quiz_dict(total_songs)
    print(json.dumps(song_dict, indent=4))  # track name and artist dict

    playlist = authorization(
        api_secrets.client_id,
        api_secrets.client_secret,
        api_secrets.redirect_uri
    ).playlist_items(test_playlist_id, limit=100)

    # print(json.dumps(playlist, indent=4))

    song_idx = 72

    track = TrackData(playlist)

    print(track.name(song_idx))
    print(track.album(song_idx))
    print(track.artist(song_idx))


if __name__ == '__main__':
    main()
