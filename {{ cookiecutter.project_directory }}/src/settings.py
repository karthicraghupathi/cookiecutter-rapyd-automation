import logging
import socket
import sys
from functools import partial, partialmethod
from logging.config import dictConfig

# setup some default variables
PROJECT_NAME = "{{ cookiecutter.project_name }}"
HOSTNAME = socket.gethostname().replace("-", "_").lower().split(".")[0]

# setup logging
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
                "level": "INFO",
                "class": "logging.StreamHandler",
            }
        },
        "loggers": {"": {"handlers": ["console"], "level": "DEBUG"}},
    }
)
logging.TRACE = 5
logging.addLevelName(logging.TRACE, "TRACE")
logging.Logger.trace = partialmethod(logging.Logger.log, logging.TRACE)
logging.trace = partial(logging.log, logging.TRACE)
logger = logging.getLogger("{{ cookiecutter.project_slug }}")


def handle_exception(exctype, value, traceback):
    """Sends unhandled exceptions to logging mechanism."""
    # ignore KeyboardInterrupt so a console python program can exit with ctrl + c
    if issubclass(exctype, KeyboardInterrupt):
        sys.__excepthook__(exctype, value, traceback)
        return
    # rely entirely on python's logging module for formatting the exception
    logger.critical("Uncaught exception", exc_info=(exctype, value, traceback))


# hook up the exception handler
sys.excepthook = handle_exception
