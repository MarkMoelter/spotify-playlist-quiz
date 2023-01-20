import logging

from controller import Controller
from model import Model
from view import View


def main():
    TEST_PLAYLIST_ID = '0MiNiiLm7aSYZGW5RV3kR5'

    model = Model()
    view = View()
    controller = Controller(model, view)

    tracks = controller.parse_raw_playlist(TEST_PLAYLIST_ID)

    print(len(tracks))
    for song in tracks:
        print(song.name)


if __name__ == '__main__':
    logging.basicConfig(filename='quiz.log', level=logging.DEBUG)
    main()
