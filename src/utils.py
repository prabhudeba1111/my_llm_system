import logging
import sys
from logging.handlers import RotatingFileHandler
from pathlib import Path
from typing import Optional

from src.config import settings


def setup_logger(log_file_path: Optional[str] = None, max_bytes: int = 10_485_760, backup_count: int = 5) -> logging.Logger:

    log_level = getattr(logging, settings.log_level.upper())

    logger = logging.getLogger(settings.app_name)
    logger.setLevel(log_level)

    # Configure logger only once to avoid duplicate handlers
    if logger.handlers:
        return logger
    
    detailed_formatter = logging.Formatter(
        "[%(asctime)s] [%(levelname)-8s] [%(name)s:%(filename)s:%(lineno)d] - %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S"
    )
    
    simple_formatter = logging.Formatter(
        "[%(asctime)s] [%(levelname)-8s] %(name)s - %(message)s",
        datefmt="%H:%M:%S"
    )

    # Console Handler
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(log_level)
    console_handler.setFormatter(simple_formatter)

    logger.addHandler(console_handler)

    if log_file_path:
        log_file = Path(log_file_path)
        log_file.parent.mkdir(parents=True, exist_ok=True)

        file_handler = RotatingFileHandler(
            log_file,
            maxBytes=max_bytes,
            backupCount=backup_count
        )
        file_handler.setLevel(log_level)
        file_handler.setFormatter(detailed_formatter)

        logger.addHandler(file_handler)

    return logger
