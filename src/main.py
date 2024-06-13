import logging

from dotenv import load_dotenv

from controllers import Controller
from models import Model
from views import View


def main():
    load_dotenv()

    model = Model()
    view = View()

    controller = Controller(model, view)
    controller.start()

    tracks = model.parse_raw_playlist(list(model.user_playlists().values())[0])

    print(len(tracks))
    for song in tracks[:5]:
        print(song)


if __name__ == '__main__':
    logging.basicConfig(filename='quiz.log', level=logging.DEBUG)
    main()
