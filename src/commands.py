import logging
import os
import shutil
import time
from pathlib import Path


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
                        """Создаем подробный вывод файла"""
                        tek_path = os.path.join(path, item)
                        """ Проверяем, является ли путь директорией"""
                        type_ch = "d" if os.path.isdir(tek_path) else "-"
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
    except PermissionError:
        """Ловив ошибки оступа"""
        print("ERROR: Permission denied")
        logging.error("ERROR: Permission denied")
    except OSError as e:
        """Ловим ошибку неправильного пути"""
        print(f"ERROR: {e}")
        logging.error(f"ERROR: Invalid path — {e}")


def get_cd(string):
    try:
        """Обрабатываем запрос cd"""
        logging.info("cd" + " ".join(string) if string else "cd")
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
                """Обрабатываем обычный путб"""
                cur_path = string[0]
                os.chdir(cur_path)
    except FileNotFoundError:
        """Обрабатываем ошибку неверного имени файла"""
        logging.error("ERROR: No such file or directory")
        print("ERROR: No such file or directory")
    except NotADirectoryError:
        """Не директория"""
        logging.error("ERROR: Not a directory")
        print("ERROR: Not a directory")
    except PermissionError:
        """Нет доступа"""
        logging.error("ERROR: Permission denied")
        print("ERROR: Permission denied")


def get_cat(string):
    """Обрабатываем запрос cat"""
    logging.info("cat" + " ".join(string))
    if len(string) == 0:
        """Если был подан пустой запрос"""
        logging.error("cat: missing file operand")
        print("cat: missing file operand")
        return
    for file in string:
        try:
            """Проходимся по файлам и пытаемся
            вывести содержание каждого"""
            text = Path(file).read_text()
            print(text, end="")
        except FileNotFoundError:
            """Неверное имя файла"""
            print(f"cat: {file}: No such file or directory")
            logging.error(f"cat: {file}: No such file or directory")
        except IsADirectoryError:
            """Ошибка директории(должен быть файл)"""
            print(f"cat: {file}: Is a directory")
            logging.error(f"cat: {file}: Is a directory")
        except PermissionError:
            """Отсутствие доступа"""
            print(f"cat: {file}: Permission denied")
            logging.error(f"cat: {file}: Permission denied")


def get_cp(string):
    if len(string) == 0:
        """Обрабатываем ввод пустого пути"""
        logging.error("cp: missing file operand")
        print("cp: missing file operand")
        return

    tek_path = [x for x in string if x != "-r"]
    """Получаем путь"""

    if len(tek_path) < 2:
        """Обрабатываем ввод меньше чем двух аргументов"""
        logging.error("cp: missing destination file operand after source")
        print("cp: missing destination file operand after source")
        return

    path1 = tek_path[0]
    path2 = tek_path[1]
    logging.info("cp " + " ".join(string))
    try:
        """Проверяем указатель -r"""
        if "-r" in string:
            shutil.copytree(path1, path2)
            return
        else:
            """Работаем с обычным копированием"""
            if os.path.isdir(path1):
                logging.error(f"cp: -r not specified, omitting directory '{path1}'")
                print(f"cp: -r not specified, omitting directory '{path1}'")
                return
            if os.path.isdir(path2):
                path2 = os.path.join(path2, os.path.basename(path1))
            shutil.copy2(path1, path2)
            return
    except FileNotFoundError:
        # Ошибка неправильного воода имени файла
        print(f"cp: cannot stat '{path1}': No such file or directory")
        logging.error(f"cp: cannot stat '{path1}': No such file or directory")
    except PermissionError:
        # Ошибка доступа
        print("cp: permission denied")
        logging.error("cp: permission denied")
    except OSError as e:
        # Ловим ошибку неправильного пути
        print(f"cp: cannot copy '{path1}' to '{path2}': {e.strerror}")
        logging.error(f"cp: cannot copy '{path1}' to '{path2}': {e}")
