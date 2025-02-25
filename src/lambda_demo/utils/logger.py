import json
import logging
import os


def setup_json_logger(name=None):
    logger = logging.getLogger(name)  # Get logger with name or root logger

    log_level = os.environ.get(f"LOG_LEVEL_{name}", os.environ.get("LOG_LEVEL", "INFO")).upper()
    logger.setLevel(log_level)

    for hdlr in logger.handlers[:]:
        print("setup_json_logger removing a handler")
        logger.removeHandler(hdlr)

    json_handler = logging.StreamHandler()
    json_formatter = logging.Formatter(
        json.dumps(
            {
                "asctime": "%(asctime)s",
                "levelname": "%(levelname)s",
                "filename": "%(filename)s",
                "lineno": "%(lineno)d",
                "message": "%(message)s",
            }
        ),
        datefmt="%Y-%m-%d %H:%M:%S",
    )
    json_handler.setFormatter(json_formatter)
    logger.addHandler(json_handler)

    return logger
