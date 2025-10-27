import logging
import os
import time


def get_ls(string):
    try:
        """Обрабатываем запрос при вызывании ls"""
        logging.info("ls " + " ".join(string) if string else "ls")
        if len(string) == 0:
            """Если в консоль ввели
            просто ls"""
            items = sorted(os.listdir("."))
            """Выводим как консоль
            в алфавитном порядке"""
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
                """Обрабатываем случай, когда
                путь не существует"""
                print("ERROR: No such file or directory")
                logging.error("ERROR: No such file or directory")
                return
            if not os.path.isdir(path):
                """Проверяем, не является ли путь файлом"""
                print("ERROR: Not a directory")
                logging.error("ERROR: Not a directory")
                return
            else:
                """Срабатывает уже наша команда ls"""
                items = sorted(os.listdir(path))
                if "-l" not in string:
                    print(" ".join(items))
                else:
                    for item in items:
                        tek_path = os.path.join(path, item)
                        type_ch = "d" if os.path.isdir(tek_path) else "-"
                        try:
                            size = (
                                os.path.getsize(tek_path)
                                if os.path.isfile(tek_path)
                                else 0
                            )
                            mtime = os.path.getmtime(tek_path)
                            time_f = time.ctime(mtime)
                        except OSError:
                            size = 0
                            time_f = "????-??-?? ??:??:??"
                        print(f"{type_ch} {size} {time_f} {item}")
    except PermissionError:
        print("ERROR: Permission denied")
        logging.error("ERROR: Permission denied")
    except OSError as e:
        print(f"ERROR: {e}")
        logging.error(f"ERROR: Invalid path — {e}")


def get_cd(string):
    try:
        logging.info("cd" + " ".join(string) if string else "cd")
        if len(string) == 0:
            path = os.path.expanduser("~")
            os.chdir(path)
        else:
            if string[0] == "..":
                os.chdir("..")
            elif string[0] == "~":
                path = os.path.expanduser("~")
                os.chdir(path)
            else:
                cur_path = string[0]
                os.chdir(cur_path)
    except FileNotFoundError:
        logging.error("ERROR: No such file or directory")
        print("ERROR: No such file or directory")
    except NotADirectoryError:
        logging.error("ERROR: Not a directory")
        print("ERROR: Not a directory")
    except PermissionError:
        logging.error("ERROR: Permission denied")
        print("ERROR: Permission denied")
