import logging
import os
import sys
from logging.config import dictConfig

from dotenv import load_dotenv, find_dotenv


# Load environment variables from the .env file
try:
    load_dotenv(find_dotenv(raise_error_if_not_found=True))
except OSError:
    raise FileNotFoundError(
        "Could not find an .env file. Did you create one?"
    ) from None


# Setup default variables
PROJECT_NAME = "{{ cookiecutter.project_name }}"
PROJECT_SLUG = "{{ cookiecutter.project_slug }}"


# Logging setup

# Configure logging
dictConfig(
    {
        "version": 1,
        "disable_existing_loggers": False,
        "formatters": {
            "simple": {"format": "%(asctime)s %(levelname)-8s %(name)s %(message)s"}
        },
        "handlers": {
            "console": {
                "formatter": "simple",
                "level": os.environ.get("LOG_LEVEL", "INFO"),
                "class": "logging.StreamHandler",
            }
        },
        "loggers": {"": {"handlers": ["console"], "level": "INFO"}},
    }
)
logger = logging.getLogger("{}.{}".format(PROJECT_SLUG, __name__))


# Define the exception handler for unhandled exceptions
def handle_exception(exctype, value, traceback):
    """Sends unhandled exceptions to logging mechanism."""
    # ignore KeyboardInterrupt so a console python program can exit with ctrl + c
    if issubclass(exctype, KeyboardInterrupt):
        sys.__excepthook__(exctype, value, traceback)
        return
    # rely entirely on python's logging module for formatting the exception
    logger.critical("Uncaught exception", exc_info=(exctype, value, traceback))


# Hook up the exception handler
sys.excepthook = handle_exception
