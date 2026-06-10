import logging.config
import pathlib

import yaml
from dotenv import load_dotenv

from src.controllers import Controller
from src.models import Model
from src.views import View

# Anchor all relative paths to the repo root, not the working directory.
# This makes the app runnable from the IDE (cwd = src/) or the terminal
# (cwd = repo root) without breaking file lookups.
ROOT = pathlib.Path(__file__).parent.parent

logger = logging.getLogger("my_app")


def setup_logging():
    config_file = ROOT / "logging_configs" / "config.yaml"
    with open(config_file) as f_in:
        config = yaml.safe_load(f_in)
    # Make the log file path absolute so it works regardless of cwd
    config["handlers"]["file"]["filename"] = str(ROOT / "logs" / "app.log")
    logging.config.dictConfig(config)


def main():
    setup_logging()
    load_dotenv(ROOT / ".env")

    model = Model()
    view = View()
    controller = Controller(model, view)

    logger.info("starting my_app")
    controller.start()
    logger.info("closing my_app")


if __name__ == "__main__":
    main()
