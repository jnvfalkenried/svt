from loguru import logger


def setup_logger(log_name, level="INFO"):
    """
    Configure and set up a specialized logger for logging application events.

    Creates a log file with advanced configuration using Loguru, including
    automatic rotation, compression, and detailed formatting.

    Args:
        log_name (str): Base name for the log file. The log will be created 
                        in the 'logs/' directory with this name and a '.log' extension.
        level (str, optional): Logging level. Defaults to "INFO". 
                               Accepted values include "DEBUG", "INFO", 
                               "WARNING", "ERROR", "CRITICAL".

    Returns:
        logger: Configured Loguru logger instance with specified settings.
    """
    logger.add(
        f"logs/{log_name}.log",
        level=level,
        format="{time} | {level} | {module}:{function}:{line} | {message}",
        rotation="5 MB",
        compression="zip",
        enqueue=True,
    )
    return logger
