import logging
import sys

def get_logger(name: str = "reco_api", level: str = "INFO") -> logging.Logger:
    logger = logging.getLogger(name)
    logger.setLevel(level)
    
    if not logger.handlers:
        formatter = logging.Formatter(
            "[%(asctime)s] [%(levelname)s] [%(name)s] %(message)s"
        )
        ch = logging.StreamHandler(sys.stdout)
        ch.setFormatter(formatter)
        logger.addHandler(ch)
    return logger

# Usage example:
# logger = get_logger()
# logger.info("API Started")
