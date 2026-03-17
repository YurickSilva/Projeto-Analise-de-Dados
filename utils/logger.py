import logging
import os
from datetime import datetime
from pathlib import Path

LOG_DIR = Path(__file__).resolve().parents[1] / "logs"
LOG_DIR.mkdir(exist_ok=True)

def setup_logger(nome: str) -> logging.Logger:
    logger = logging.getLogger(nome)
    logger.setLevel(logging.INFO)

    if logger.handlers:
        return logger  # evita duplicação

    data = datetime.now().strftime("%Y-%m-%d")
    log_file = LOG_DIR / f"{data}_{nome}.log"

    formatter = logging.Formatter(
        "%(asctime)s | %(levelname)s | %(name)s | %(message)s"
    )

    file_handler = logging.FileHandler(log_file, encoding="utf-8")
    file_handler.setFormatter(formatter)

    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(formatter)

    logger.addHandler(file_handler)
    logger.addHandler(stream_handler)

    return logger