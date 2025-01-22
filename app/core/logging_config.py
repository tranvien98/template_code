from logging.config import dictConfig
from config import settings

logging_config = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "default": {
            "format": "%(levelname)s: %(asctime)27s - %(message)s",
        },
        "detailed": {
            "format": "%(asctime)s - %(name)s - %(levelname)s - %(message)s [in %(pathname)s:%(lineno)d]",
        },
        "colored": {
            "format": "%(log_color)s%(levelname)s%(reset)s%(message_log_color)s: %(asctime)27s - %(message)s",
            "()": "colorlog.ColoredFormatter",
            "log_colors": {
                "DEBUG": "bold_blue",
                "INFO": "bold_green",
                "WARNING": "bold_yellow",
                "ERROR": "bold_red",
                "CRITICAL": "bold_purple",
            },
            "secondary_log_colors": {
                'message': {
                    'INFO': 'white'
                }
            },
        }
    },
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "formatter": "colored",
            "level": settings.LOG_LEVEL,
        },
        # "file": {
        #     "class": "logging.FileHandler",
        #     "formatter": "detailed",
        #     "filename": "app.log",
        #     "mode": "a",
        # },
    },
    "loggers": {
        "uvicorn": {
            "handlers": ["console"],
            "level": settings.LOG_LEVEL,
            "propagate": False,
        },
        "uvicorn.access": {
            "handlers": ["console"],
            "level": settings.LOG_LEVEL,
            "propagate": False,
        },
        "uvicorn.error": {
            "handlers": ["console"],
            "level": "WARNING",
            "propagate": False,
        }
    },
    "root": {
        "level": settings.LOG_LEVEL,
        "handlers": ["console"],
    },
}


def setup_logging():
    dictConfig(logging_config)
