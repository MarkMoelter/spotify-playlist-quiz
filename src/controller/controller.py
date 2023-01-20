import logging

from controller.song import Song
from model import Model
from view import View


class Controller:
    def __init__(self, model: Model, view: View):
        logging.info('Initializing Controller')
        self.model = model
        self.view = view

    def parse_raw_playlist(self, playlist_id: str) -> list[Song]:
        """
        Convert the raw dictionary into a list of songs.

        :param playlist_id: The identifier of the playlist.
        :return: A list of song objects
        """
        # TODO: Add URI to Song objects
        raw_playlist = self.model.playlist_by_id(playlist_id)
        tracks: list = raw_playlist['items']

        songs = []
        for track in tracks:
            track_info = track['track']

            name = track_info['name']
            album = track_info['album']

            # collect all artists for a track
            artists = [artist['name'] for artist in track_info['artists']]

            songs.append(Song(name, album, artists))
        return songs
