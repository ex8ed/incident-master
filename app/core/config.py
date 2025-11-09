# -*- coding: UTF-8 -*-
import logging
import os
import sys
from functools import lru_cache


DB_NAME = os.getenv("DB_NAME", "incidents")
DB_USER = os.getenv("DB_USER", "postgres") 
DB_PASSWORD = os.getenv("DB_PASSWORD", "password")
DB_HOST = os.getenv("DB_HOST", "postgres")

DB_URL = f"postgresql+asyncpg://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:5432/{DB_NAME}"
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")


@lru_cache(maxsize=1)
def setup_logs():
    _logger = logging.getLogger("incident_api")

    if _logger.handlers:
        return _logger
    
    _logger.setLevel(LOG_LEVEL)
    _logger.propagate = False

    formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S"
    )

    handler = logging.StreamHandler(sys.stdout)
    handler.setFormatter(formatter)
    _logger.addHandler(handler)

    logging.getLogger("uvicorn.access").disabled = True
    logging.getLogger("sqlalchemy.engine").setLevel(logging.WARNING)
    
    return _logger
