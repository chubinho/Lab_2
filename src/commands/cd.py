import os

from logger import log1, log2


def get_cd(string):
    try:
        """Обрабатываем запрос cd"""
        log1("cd", string)
        if len(string) == 0:
            """Переходим в домашнюю директорию"""
            path = os.path.expanduser("~")
            os.chdir(path)
        else:
            """Переходим на уровень выше"""
            if string[0] == "..":
                os.chdir("..")
            elif string[0] == "~":
                """Переходим в домашнюю директорию"""
                path = os.path.expanduser("~")
                os.chdir(path)
            else:
                """Обрабатываем обычный путь"""
                cur_path = string[0]
                if not os.path.exists(cur_path):
                    raise FileNotFoundError(f"No such file or directory: {cur_path}")
                if not os.path.isdir(cur_path):
                    raise NotADirectoryError(f"Not a directory: {cur_path}")
                os.chdir(cur_path)
    except (FileNotFoundError, NotADirectoryError, PermissionError) as e:
        """Обрабатываем ошибки и перевыбрасываем их"""
        log2("cd", str(e))
        raise
