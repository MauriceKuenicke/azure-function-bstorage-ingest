import logging
import os

LOG_FILE_PATH = os.path.join(os.getcwd(), "execution_log.log")


def create_file_handler() -> logging.FileHandler:
    f_handler = logging.FileHandler(LOG_FILE_PATH, mode="w")
    f_format = logging.Formatter('%(asctime)s [%(levelname)s] - %(name)s - %(message)s')
    f_handler.setLevel(logging.DEBUG)
    f_handler.setFormatter(f_format)

    return f_handler
