import logging


def create_file_handler(file_path: str) -> logging.FileHandler:
    f_handler = logging.FileHandler(file_path, mode="w")
    f_format = logging.Formatter('%(asctime)s [%(levelname)s] - %(name)s - %(message)s')
    f_handler.setLevel(logging.DEBUG)
    f_handler.setFormatter(f_format)

    return f_handler
