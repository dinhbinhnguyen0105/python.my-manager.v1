import logging
import sys

logger = logging.getLogger(__name__)
logger.setLevel(logging.ERROR)
formatter = logging.Formatter(
    '%(asctime)s - %(name)s - %(levelname)s - %(filename)s:%(lineno)d - %(message)s')
handler = logging.StreamHandler(sys.stderr)
handler.setFormatter(formatter)
if not logger.hasHandlers():
    logger.addHandler(handler)


def error(msg):
    logger.error(msg)


def warning(msg):
    logger.warning(msg)


def info(msg):
    logger.info(msg)
