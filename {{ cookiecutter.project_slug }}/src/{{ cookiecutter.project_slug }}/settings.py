import logging
import sys
from logging.config import dictConfig
from pathlib import Path

from environs import env

env.read_env()

PROJECT_NAME = {{ cookiecutter.project_name | tojson }}
PROJECT_SLUG = {{ cookiecutter.project_slug | tojson }}
PROJECT_DIR = Path(__file__).resolve().parents[2]

VALID_LOG_LEVELS = {"DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"}
_RAW_LOG_LEVEL = env.str("LOG_LEVEL", "INFO").upper()
if _RAW_LOG_LEVEL not in VALID_LOG_LEVELS:
    print(
        f"[settings] LOG_LEVEL={_RAW_LOG_LEVEL!r} is not one of {sorted(VALID_LOG_LEVELS)}; "
        "falling back to INFO.",
        file=sys.stderr,
    )
    _RAW_LOG_LEVEL = "INFO"
LOG_LEVEL = _RAW_LOG_LEVEL


class ExcludeErrorFilter(logging.Filter):
    """Filter that drops records at ERROR level or above."""

    def filter(self, record: logging.LogRecord) -> bool:
        return record.levelno < logging.ERROR


dictConfig(
    {
        "version": 1,
        "disable_existing_loggers": False,
        "filters": {"exclude_error": {"()": ExcludeErrorFilter}},
        "formatters": {
            "simple": {"format": "%(asctime)s %(levelname)-8s %(name)s %(message)s"}
        },
        "handlers": {
            "console_stdout": {
                "formatter": "simple",
                "level": LOG_LEVEL,
                "class": "logging.StreamHandler",
                "stream": sys.stdout,
                "filters": ["exclude_error"],
            },
            "console_stderr": {
                "formatter": "simple",
                "level": "ERROR",
                "class": "logging.StreamHandler",
                "stream": sys.stderr,
            },
        },
        "loggers": {
            "": {
                "handlers": ["console_stdout", "console_stderr"],
                "level": "DEBUG",
            }
        },
    }
)
logger = logging.getLogger(__name__)


def handle_exception(exctype, value, traceback):
    """Route uncaught exceptions through logging.

    KeyboardInterrupt is preserved so console programs exit cleanly on Ctrl+C.
    """
    if issubclass(exctype, KeyboardInterrupt):
        sys.__excepthook__(exctype, value, traceback)
        return
    logger.critical("Uncaught exception", exc_info=(exctype, value, traceback))


sys.excepthook = handle_exception
