import logging
from pathlib import Path

from datetime import datetime


def logger_setup(log_file_name: str = "App", log_folder_name: Path | str = "logs") -> None:
    """Create a root logger with a Stream and File Handler."""
    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)

    formatted_date = datetime.strftime(datetime.today(), "%Y_%m_%d")

    file_handler = logging.FileHandler(f"{log_folder_name}\\{log_file_name}_{formatted_date}.log")
    file_handler.setLevel(logging.INFO)

    debug_file_handler = logging.FileHandler(f"{log_folder_name}\\{log_file_name}_{formatted_date}_debug.log")
    debug_file_handler.setLevel(logging.DEBUG)

    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.ERROR)

    FORMAT = "%(levelname)s - %(asctime)s - %(name)s - %(message)s"
    formatter = logging.Formatter(FORMAT)
    file_handler.setFormatter(formatter)
    console_handler.setFormatter(formatter)

    logger.addHandler(file_handler)
    logger.addHandler(debug_file_handler)
    logger.addHandler(console_handler)
