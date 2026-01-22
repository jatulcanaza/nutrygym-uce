import logging
from app.core.config import LOG_LEVEL, SERVICE_NAME

def get_logger(name: str = SERVICE_NAME) -> logging.Logger:
    logger = logging.getLogger(name)
    if logger.handlers:
        return logger

    logger.setLevel(LOG_LEVEL)
    handler = logging.StreamHandler()
    fmt = logging.Formatter(
        fmt="%(asctime)s %(levelname)s %(name)s - %(message)s"
    )
    handler.setFormatter(fmt)
    logger.addHandler(handler)
    logger.propagate = False
    return logger
