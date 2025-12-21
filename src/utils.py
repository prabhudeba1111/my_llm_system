import logging

from src.config import settings


def setup_logger() -> logging.Logger:
    logging.basicConfig(
        level=getattr(logging, settings.log_level.upper(), logging.INFO),
        format="[%(asctime)s] [%(levelname)s] %(name)s - %(message)s",
    )

    logger = logging.getLogger(settings.app_name)
    return logger
