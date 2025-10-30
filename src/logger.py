import logging


def logger_set():
    logging.basicConfig(
        level=logging.INFO,
        filename="shell.log",
        format="[%(asctime)s] %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )
    return logging.getLogger("shell")


logger = logger_set()


# Добавляем в shell.log команду
def log1(command, string):
    logger.info(f"{command} {' '.join(string)}")


# Добавляем в shell.log ошибку
def log2(command, message):
    logger.error(f"{command}: {message}")
