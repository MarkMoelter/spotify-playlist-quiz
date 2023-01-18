import controller.song as song


def parse_playlist_dict(playlist_dict: dict) -> list[song.Song]:
    """
    Convert the raw playlist into a list of song objects.

    :param playlist_dict: The raw dictionary containing all the playlist information
    :return: A list of song objects
    """
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
