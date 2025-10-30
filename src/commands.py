import os
import shutil
import time
from pathlib import Path

from logger import log1, log2, logger


def get_ls(string):
    try:
        """Обрабатываем запрос при вызывании ls"""
        log1("ls", string)
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
                log2("ls", "No such file or directory")
                return
            if not os.path.isdir(path):
                """Проверяем, не является ли путь файлом"""
                print("ERROR: Not a directory")
                log2("ls", "Not a directory")
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
    except PermissionError:
        """Ловив ошибки оступа"""
        print("ERROR: Permission denied")
        log2("ls", "Permission denied")
    except OSError as e:
        """Ловим ошибку неправильного пути"""
        print(f"ERROR: {e}")
        log2("ls", f"Invalid path — {e}")


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
                """Обрабатываем обычный путб"""
                cur_path = string[0]
                os.chdir(cur_path)
    except FileNotFoundError:
        """Обрабатываем ошибку неверного имени файла"""
        log2("cd", "No such file or directory")
        print("ERROR: No such file or directory")
    except NotADirectoryError:
        """Не директория"""
        log2("cd", "Not a directory")
        print("ERROR: Not a directory")
    except PermissionError:
        """Нет доступа"""
        log2("cd", "Permission denied")
        print("ERROR: Permission denied")


def get_cat(string):
    """Обрабатываем запрос cat"""
    log1("cat", string)
    if len(string) == 0:
        """Если был подан пустой запрос"""
        log2("cat", "missing file operand")
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
            log2("cat", f"{file}: No such file or directory")
        except IsADirectoryError:
            """Ошибка директории(должен быть файл)"""
            print(f"cat: {file}: Is a directory")
            log2("cat", f"{file}: Is a directory")
        except PermissionError:
            """Отсутствие доступа"""
            print(f"cat: {file}: Permission denied")
            log2("cat", f"{file}: Permission denied")


def get_cp(string):
    if len(string) == 0:
        """Обрабатываем ввод пустого пути"""
        log2("cp", "missing file operand")
        print("cp: missing file operand")
        return

    tek_path = [x for x in string if x != "-r"]

    if len(tek_path) < 2:
        """Обрабатываем ввод меньше чем двух аргументов"""
        log2("cp", "missing destination file operand after source")
        print("cp: missing path2ination file operand after path1")
        return

    path1 = tek_path[0]
    path2 = tek_path[1]
    log1("cp", string)
    try:
        """Проверяем указатель -r"""
        if "-r" in string:
            shutil.copytree(path1, path2)
            return
        else:
            """Работаем с обычным копированием"""
            if os.path.isdir(path1):
                log2("cp", f"-r not specified, omitting directory '{path1}'")
                print(f"cp: -r not specified, omitting directory '{path1}'")
                return
            if os.path.isdir(path2):
                path2 = os.path.join(path2, os.path.basename(path1))
            shutil.copy2(path1, path2)
            return
    except FileNotFoundError:
        # Ошибка неправильного воода имени файла
        print(f"cp: cannot stat '{path1}': No such file or directory")
        log2("cp", f"cannot stat '{path1}': No such file or directory")
    except PermissionError:
        # Ошибка доступа
        print("cp: permission denied")
        log2("cp", "permission denied")
    except OSError as e:
        # Ловим ошибку неправильного пути
        print(f"cp: cannot copy '{path1}' to '{path2}': {e.strerror}")
        log2("cp", f"cannot copy '{path1}' to '{path2}': {e}")


def get_mv(string):
    """Обрабатываем ввод пустого пути"""
    if len(string) < 2:
        log2("mv", "missing file operand")
        print("mv: missing file operand")
        return

    if len(string) > 2:
        """Если введены 2 аргумента"""
        log2("mv", "extra operand after source and destination")
        print("mv: extra operand after source and destination")
        return
    path1 = string[0]
    path2 = string[1]
    log1("mv", string)
    try:
        """Перемещаем файл или каталог"""
        shutil.move(path1, path2)
    except FileNotFoundError:
        """Неверное имя файла/каталога"""
        print(f"mv: cannot stat '{path1}': No such file or directory")
        log2("mv", f"cannot stat '{path1}': No such file or directory")
    except PermissionError:
        """Отсутствие доступа"""
        print("mv: permission denied")
        log2("mv", "permission denied")
    except OSError as e:
        """Ловим ошибку неправильного пути или других системных ошибок"""
        print(f"mv: cannot move '{path1}' to '{path2}': {e.strerror}")
        log2("mv", f"cannot move '{path1}' to '{path2}': {e}")


def get_rm(string):
    if len(string) == 0:
        """Обрабатываем ввод пустого пути"""
        print("rm: missing file operand")
        log2("rm", "missing file operand")
        return

    path = [x for x in string if x != "-r"]
    # Находим путь без rm
    if len(path) == 0:
        """Если не был передан путь файла/директории"""
        print("rm: missing file operand")
        log2("rm", "missing file operand")
        return

    log1("rm", string)
    path1 = path[0]  # Определяем путь
    path2 = os.path.abspath(path1)
    if path2 == os.path.abspath("..") or path2 == "/":
        """Предотвращаем удаление корневого и родительского каталога"""
        print(f"rm: cannot remove '{path1}': Operation not permitted")
        log2("rm", f"cannot remove '{path1}': Operation not permitted")
        return
    else:
        """Рассматриваем ввод правильных путей"""
        try:
            if os.path.isfile(path1):
                """Удаляем файл"""
                os.remove(path1)
            elif os.path.isdir(path1):
                """Проверяем, является ли директорией"""
                if "-r" in string:
                    """Спрашиваем перед удалением"""
                    choice = input(f"rm: remove directory '{path1}'? (y/n) ").strip()
                    if choice == "y":
                        """Если принимается удаление,
                        то рекурсивно удаляем всё в директории"""
                        shutil.rmtree(path1)
                    else:
                        print("rm: cancelled")
                        logger.info(f"rm: cancelled for '{path1}'")
                else:
                    """Если нет -r"""
                    print(f"rm: cannot remove '{path1}': Is a directory")
                    log2("rm", f"cannot remove '{path1}': Is a directory")
            else:
                """Неизвестный файл"""
                print(f"rm: cannot remove '{path1}': No such file or directory")
                log2("rm", f"cannot remove '{path1}': No such file or directory")

        except PermissionError:
            """Ошибка доступа"""
            print(f"rm: cannot remove '{path1}': Permission denied")
            log2("rm", f"cannot remove '{path1}': Permission denied")
        except OSError as e:
            """Ошибка системы"""
            print(f"rm: cannot remove '{path1}': {e.strerror}")
            log2("rm", f"cannot remove '{path1}': {e}")
