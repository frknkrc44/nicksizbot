import logging

logging.basicConfig(
    # %(asctime)s
    # %(levelname)s
    # %(name)s
    format=" %(lineno)s - %(message)s",
    level=logging.DEBUG,
)
tgkatlogger = logging.getLogger(__name__)
