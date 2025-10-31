import os
import time

from logger import log1, log2


def get_ls(string):
    try:
        """Обрабатываем запрос при вызывании ls"""
        log1("ls", string)
        if len(string) == 0:
            """Если в консоль ввели просто ls"""
            items = sorted(os.listdir("."))
            """Выводим как консоль в алфавитном порядке"""
            print(" ".join(items))
            return
        else:
            """Определяем путь без указателя -l"""
            current_path = [x for x in string if x != "-l"]
            if len(current_path) > 0:
                """Обрабатываем путь"""
                path = current_path[0]
            else:
                """Выводим путь"""
                path = "."
            """Получаем абсолютный путь"""
            path = os.path.abspath(path)
            if not os.path.exists(path):
                """Обрабатываем случай, когда путь не существует"""
                raise FileNotFoundError(f"No such file or directory: {path}")
            if not os.path.isdir(path):
                """Проверяем, не является ли путь файлом"""
                raise NotADirectoryError(f"Not a directory: {path}")
            else:
                """Срабатывает уже наша команда ls"""
                items = sorted(os.listdir(path))
                if "-l" not in string:
                    print(" ".join(items))
                else:
                    for item in items:
                        """Создаем подробный вывод файла"""
                        tek_path = os.path.join(path, item)
                        """ Проверяем, является ли путь директорией"""
                        if os.path.isdir(tek_path):
                            type_ch = "D"
                        else:
                            type_ch = "F"
                        try:
                            size = (
                                os.path.getsize(tek_path)
                                if os.path.isfile(tek_path)
                                else 0
                            )
                            """Получаем время в таком формате, как нас просят"""
                            mtime = os.path.getmtime(tek_path)
                            time_f = time.ctime(mtime)

                        except OSError:
                            size = 0
                            time_f = "????-??-?? ??:??:??"
                        print(f"{type_ch} {size} {time_f} {item}")
    except (PermissionError, NotADirectoryError, FileNotFoundError) as e:
        """Ловим ошибки и перевыбрасываем их"""
        log2("ls", str(e))
        raise
    except OSError as e:
        """Ловим ошибку неправильного пути"""
        log2("ls", f"Invalid path — {e}")
        raise OSError(f"Invalid path: {e}")
