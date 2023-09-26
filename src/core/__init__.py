import logging
import os
from .LoggingFileHandler import create_file_handler

LOG_FILE_PATH = os.path.join(os.getcwd(), "execution_log.log")
LOG_FILE_HANDLER = create_file_handler(LOG_FILE_PATH)

