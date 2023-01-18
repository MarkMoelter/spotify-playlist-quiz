import logging

from controller.get_playlist import parse_playlist_dict
from model import Model


# TODO: Move functionality to controller after messing around
# TODO: Add URI to Song objects
def main():
    TEST_PLAYLIST_ID = '0MiNiiLm7aSYZGW5RV3kR5'

    model = Model()
    playlist = model.get_user_playlist(TEST_PLAYLIST_ID)
    tracks = parse_playlist_dict(playlist)

    print(len(tracks))
    for song in tracks:
        print(song.name)


if __name__ == '__main__':
    logging.basicConfig(filename='quiz.log', level=logging.DEBUG)
    main()
