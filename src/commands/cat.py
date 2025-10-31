import os
from pathlib import Path

from logger import log1, log2


def get_cat(string):
    """Обрабатываем запрос cat"""
    log1("cat", string)
    if len(string) == 0:
        """Если был подан пустой запрос"""
        raise ValueError("missing file operand")

    for file in string:
        try:
            """Проходимся по файлам и пытаемся вывести содержание каждого"""
            if not os.path.exists(file):
                raise FileNotFoundError(f"{file}: No such file or directory")
            if os.path.isdir(file):
                raise IsADirectoryError(f"{file}: Is a directory")

            text = Path(file).read_text()
            print(text, end="")
        except (FileNotFoundError, IsADirectoryError, PermissionError) as e:
            """Ловим ошибки и перевыбрасываем их"""
            log2("cat", str(e))
            raise
