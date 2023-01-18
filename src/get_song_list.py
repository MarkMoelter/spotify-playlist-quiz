import song


def get_song_list(playlist_dict: dict) -> list[song.Song]:
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
