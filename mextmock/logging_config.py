import logging.config


def get_logging_config() -> dict:

    logging_config = {
        "version": 1,
        "disable_existing_loggers": False,
        "formatters": {
            "verbose": {
                "format": "{asctime} {name} {levelname} (pid: {process}) {message}",
                "style": "{",
            },
        },
        "handlers": {
            "console": {
                "class": "logging.StreamHandler",
                "formatter": "verbose",
                "stream": "ext://sys.stderr",
            },
        },
        "root": {
            "handlers": ["console"],
            "level": "INFO",
        },
        "loggers": {
            "mextmock": {
                "handlers": ["console"],
                "level": "INFO",
                "propagate": False,
            },
            "mrok": {
                "handlers": ["console"],
                "level": "INFO",
                "propagate": False,
            },
        },
    }

    return logging_config


def setup_logging() -> None:
    logging_config = get_logging_config()
    logging.config.dictConfig(logging_config)
