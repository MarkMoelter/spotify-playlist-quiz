class Track:
    def __init__(self, playlist: dict, track_idx: int):
        self._playlist = playlist
        self._track_idx = track_idx

    @property
    def name(self) -> str:
        """
        Get the name of the track
        :return: The name of the track.
        """
        return self._playlist['items'][self._track_idx]['track']['name']

    @property
    def artists(self) -> list[str]:
        """
        Get the artists of the track.
        :return: A list of artists.
        """
        return [
            artist['name']
            for artist in self._playlist['items'][self._track_idx]['track']['artists']
        ]

    @property
    def album(self) -> str:
        """c
        Get the album of the track.
        :return: The album the track belongs to.
        """
        return self._playlist['items'][self._track_idx]['track']['album']['name']
