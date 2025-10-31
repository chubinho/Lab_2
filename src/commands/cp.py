import os
import shutil

from logger import log1, log2


def get_cp(string):
    if len(string) == 0:
        """Обрабатываем ввод пустого пути"""
        raise ValueError("missing file operand")

    tek_path = [x for x in string if x != "-r"]

    if len(tek_path) < 2:
        """Обрабатываем ввод меньше чем двух аргументов"""
        raise ValueError("missing destination file operand after source")

    path1 = tek_path[0]
    path2 = tek_path[1]
    log1("cp", string)

    try:
        """Проверяем существование исходного файла"""
        if not os.path.exists(path1):
            raise FileNotFoundError(f"cannot stat '{path1}': No such file or directory")

        """Проверяем указатель -r"""
        if "-r" in string:
            shutil.copytree(path1, path2)
            return
        else:
            """Работаем с обычным копированием"""
            if os.path.isdir(path1):
                raise ValueError(f"-r not specified, omitting directory '{path1}'")
            if os.path.isdir(path2):
                path2 = os.path.join(path2, os.path.basename(path1))
            shutil.copy2(path1, path2)
            return
    except (FileNotFoundError, PermissionError, ValueError) as e:
        """Ловим ошибки и перевыбрасываем их"""
        log2("cp", str(e))
        raise
    except OSError as e:
        """Ловим ошибку неправильного пути"""
        log2("cp", f"cannot copy '{path1}' to '{path2}': {e}")
        raise OSError(f"cannot copy '{path1}' to '{path2}': {e.strerror}")
