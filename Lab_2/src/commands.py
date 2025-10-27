import logging
import os
import time


def get_ls(string):
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
            path = "."
        path = os.path.abspath(path)
        if not os.path.exists(path):
            print("ERROR: No such file or directory")
            logging.error("No such file or directory")
            return
        if not os.path.isdir(path):
            print("ERROR: Not a directory")
            logging.error("Not a directory")
            return
        else:
            items = sorted(os.listdir(path))
            if "-l" not in string:
                print(" ".join(items))
            else:
                for item in items:
                    tek_path = os.path.join(path, item)
                    type_ch = "d" if os.path.isdir(tek_path) else "-"
                    size = os.path.getsize(tek_path) if os.path.isfile(tek_path) else 0
                    mtime = os.path.getmtime(tek_path)
                    time_f = time.ctime(mtime)
                    print(f"{type_ch} {size} {time_f} {item}")
