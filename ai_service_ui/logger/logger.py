import logging
import logging.config

from . import CONFIG_LOG


class Logger(logging.getLoggerClass()):
    """This is a customized Logger initialized with a default Logger provided by logging library."""

    def __init__(self, name, level=logging.NOTSET):
        """Create custom logger calling to super class.

        Args:
            name (str): Name of the logger.
            level (str or int): Set the logging level of this logger.
        """
        super(logging.getLoggerClass(), self).__init__(name, level)


def get_logger(name=None):
    """Build a logger with the given name and returns the logger.

    Args:
        name: The name for the logger. This is usually the module name, ``__name__``.

    Returns:
        Logger object
    """
    logging.setLoggerClass(Logger)
    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)
    try:
        logging.config.fileConfig(
            fname=CONFIG_LOG, disable_existing_loggers=False
        )
    except FileNotFoundError as e:
        logging.error(e)

    return logger
