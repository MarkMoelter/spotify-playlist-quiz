from pprint import pprint

from dotenv import load_dotenv

from src.controllers import Controller
from src.logger_setup import logger_setup
from src.models import Model
from src.views import View


def main():
    load_dotenv()

    model = Model()
    view = View()

    controller = Controller(model, view)
    controller.start()

    tracks = model.parse_raw_playlist(list(model.user_playlists().values())[0])

    for song in tracks:
        pprint(song)


if __name__ == '__main__':
    logger_setup("quiz")
    main()
