class TrackData:
    def __init__(self, items: dict):
        self.items = items

    def song_name(self, track_idx: int) -> str:
        return self.items['items'][track_idx]['track']['name']

    def artist(self, track_idx: int) -> list[str]:
        return [
            artist['name']
            for artist in self.items['items'][track_idx]['track']['artists']
        ]

    def album(self, track_idx: int) -> str:
        return self.items['items'][track_idx]['track']['album']['name']

