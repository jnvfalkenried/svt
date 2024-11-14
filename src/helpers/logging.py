from loguru import logger


def setup_logger(log_name, level="INFO"):
    logger.add(
        f"logs/{log_name}.log",
        level=level,
        format="{time} | {level} | {module}:{function}:{line} | {message}",
        rotation="5 MB",
        compression="zip",
        enqueue=True,
    )
    return logger
