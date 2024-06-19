import logging.config
import pathlib
from pprint import pprint

import yaml
from dotenv import load_dotenv

from src.controllers import Controller
from src.models import Model
from src.views import View

logger = logging.getLogger("my_app")


def setup_logging():
    config_file = pathlib.Path("logging_configs/config.yaml")
    with open(config_file) as f_in:
        config = yaml.safe_load(f_in)
    logging.config.dictConfig(config)


def main():
    setup_logging()
    load_dotenv()

    model = Model()
    view = View()

    controller = Controller(model, view)

    logger.info("starting my_app")
    controller.start()
    logger.info("closing my_app")

    tracks = model.parse_raw_playlist(list(model.user_playlists().values())[0])

    for song in tracks:
        pprint(song)


if __name__ == '__main__':
    main()
