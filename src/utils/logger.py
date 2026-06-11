import logging
import json
from datetime import datetime
from pathlib import Path

def setup_logger(log_dir: Path, name: str = "seip_etl") -> logging.Logger:
    log_dir.mkdir(parents=True, exist_ok=True)
    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)

    if logger.handlers:
        return logger

    log_file = log_dir / f"{name}_{datetime.now().strftime('%Y%m%d')}.log"
    file_handler = logging.FileHandler(log_file)
    console_handler = logging.StreamHandler()
    formatter = logging.Formatter("%(message)s")

    file_handler.setFormatter(formatter)
    console_handler.setFormatter(formatter)

    logger.addHandler(file_handler)
    logger.addHandler(console_handler)

    return logger

def log_event(logger: logging.Logger, event_type: str, **kwargs):
    payload = {"timestamp": datetime.now().isoformat(), "event_type": event_type, **kwargs}
    logger.info(json.dumps(payload, default=str))
