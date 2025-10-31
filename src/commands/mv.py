import os
import shutil

from logger import log1, log2


def get_mv(string):
    """Обрабатываем ввод пустого пути"""
    if len(string) < 2:
        raise ValueError("missing file operand")

    if len(string) > 2:
        """Если введены больше 2 аргументов"""
        raise ValueError("extra operand after source and destination")

    path1 = string[0]
    path2 = string[1]
    log1("mv", string)

    try:
        """Проверяем существование исходного файла"""
        if not os.path.exists(path1):
            raise FileNotFoundError(f"cannot stat '{path1}': No such file or directory")

        """Перемещаем файл или каталог"""
        shutil.move(path1, path2)
    except (FileNotFoundError, PermissionError, ValueError) as e:
        """Ловим ошибки и перевыбрасываем их"""
        log2("mv", str(e))
        raise
    except OSError as e:
        """Ловим ошибку неправильного пути или других системных ошибок"""
        log2("mv", f"cannot move '{path1}' to '{path2}': {e}")
        raise OSError(f"cannot move '{path1}' to '{path2}': {e.strerror}")
