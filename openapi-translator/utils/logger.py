import os
import sys
from datetime import timedelta
from loguru import logger

class Logger:
    def __init__(self, name="translator", log_dir="logs", debug=False):
        if not os.path.exists(log_dir):
            os.makedirs(log_dir)
        log_file_path = os.path.join(log_dir, f"{name}.log")
        logger.remove()

        level = "DEBUG" if debug else "INFO"
        logger.add(sys.stdout, level=level)
        logger.add(log_file_path, rotation=timedelta(days=1), level=level)
        self.logger = logger


LOG = Logger(debug=True).logger

if __name__ == '__main__':
    LOG.debug("This is a debug message.")
    LOG.info("This is an info message.")
    LOG.warning("This is a warning message.")
    LOG.error("This is an error message.")

