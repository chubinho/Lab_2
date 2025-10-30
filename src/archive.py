import os
import re
import tarfile
import zipfile

from logger import log1, log2


class ArchiveCommands:
    """Класс для работы с архивами и поиском файлов"""

    def grep(self, string):
        """Обрабатываем запрос grep"""
        if len(string) < 2:
            """Если неправильный ввод аргументов"""
            print("grep: usage: grep <pattern> <path>")
            return
        pattern = string[0]
        path = string[1]
        log1("grep", string)

        if "-i" in string:
            flags = re.I
        else:
            flags = 0
        try:
            """Пытаемся получить регулярное выражение"""
            reg = re.compile(pattern, flags)
        except re.error as e:
            """Если неправильно"""
            print(f"grep: invalid pattern: {e}")
            log2("grep", f"invalid pattern: {e}")
            return

        # Проверяем, что путь существует
        if os.path.isfile(path):
            """Если это файл - обрабатываем его"""
            self._grep_file(path, reg)
        # Или директорияы
        elif os.path.isdir(path):
            """Если это директория"""
            if "-r" in string:
                """Если нужно искать рекурсивно"""
                # Проходим по всем поддиректориям и файлам в них
                for tek_dir, pod_dir, files in os.walk(path):
                    for file in files:
                        """Получаем полный путь к файлу"""
                        full_path = os.path.join(tek_dir, file)
                        """Обрабатываем файл"""
                        self._grep_file(full_path, reg)
            else:
                """Если не рекурсивно - только файлы в папке"""
                # Получаем файлы в директории
                for file in os.listdir(path):
                    """Получаем полный путь"""
                    full_path = os.path.join(path, file)
                    """Проверяем, что это файл"""
                    if os.path.isfile(full_path):
                        """Обрабатываем файл"""
                        self._grep_file(full_path, reg)
        else:
            """Если путь не существует"""
            print(f"grep: {path}: No such file or directory")
            log2("grep", f"{path}: No such file or directory")

    def _check_line_for_match(self, line, reg):
        """Проверяем строку на совпадение с регуляркой"""
        match = reg.search(line)
        if match:
            return match.group(0)
        return None

    def _grep_file(self, file_path, reg):
        """Обрабатываем один файл для grep"""
        try:
            """Открываем файл для чтения"""
            with open(file_path, "r", encoding="utf-8") as f:
                """Проходим по строкам файла"""
                for line_num, line in enumerate(f, 1):
                    """Проверяем, подходит ли строка под шаблон"""
                    found_text = self._check_line_for_match(line, reg)
                    if found_text:
                        """Если строка подходит"""
                        """Выводим результат"""
                        print(f"{file_path}: {line_num}: {found_text}")
        except PermissionError:
            """Если нет прав для открытия файла"""
            print(f"grep: {file_path}: Permission denied")
            log2("grep", f"{file_path}: Permission denied")
        except UnicodeDecodeError:
            """Если файл не текстовый"""
            pass
        except Exception as e:
            """Другие ошибки"""
            print(f"grep: {file_path}: {e}")
            log2("grep", f"{file_path}: {e}")

    def zip(self, string):
        """Обрабатываем запрос zip"""
        if len(string) != 2:
            """Если аргументов не 2"""
            print("zip: usage: zip <folder> <archive.zip>")
            return
        folder = string[0]
        archive = string[1]
        log1("zip", string)

        if not os.path.isdir(folder):
            """Если переданный параметр не директория"""
            print(f"zip: {folder}: Not a directory")
            log2("zip", f"{folder}: Not a directory")
            return

        if not os.path.exists(folder):
            """Если папка не существует"""
            print(f"zip: {folder}: No such file or directory")
            log2("zip", f"{folder}: No such file or directory")
            return

        # Проверяем, что архив можно создать
        try:
            """Создаём ZIP-архив"""
            with zipfile.ZipFile(archive, "w", zipfile.ZIP_DEFLATED) as zf:
                """Проходим по всем файлам в папке"""
                for tek_dir, dirs, files in os.walk(folder):
                    """Проходим по файлам"""
                    for file in files:
                        # Получаем путь к файлу и добавляем его в архив
                        full_path = os.path.join(tek_dir, file)
                        arc_name = os.path.relpath(full_path, folder)
                        zf.write(full_path, arc_name)
            print(f"Archive '{archive}' created successfully.")
        except PermissionError:
            """Если нет прав на запись"""
            print(f"zip: {archive}: Permission denied")
            log2("zip", f"{archive}: Permission denied")
        except Exception as e:
            """Другие ошибки"""
            print(f"zip: {archive}: {e}")
            log2("zip", f"{archive}: {e}")

    def unzip(self, string):
        """Обрабатываем запрос unzip"""
        if len(string) != 1:
            """Если аргументов не 1"""
            print("unzip: usage: unzip <archive.zip>")
            return
        archive = string[0]
        log1("unzip", string)

        # Проверяем, что архив существует
        if not os.path.exists(archive):
            """Если архив не существует"""
            print(f"unzip: {archive}: No such file or directory")
            log2("unzip", f"{archive}: No such file or directory")
            return

        # Проверяем, что можно распаковать
        try:
            """Открываем ZIP-архив"""
            with zipfile.ZipFile(archive, "r") as zf:
                """Распаковываем всё"""
                zf.extractall()
            """Выводим сообщение об успехе"""
            print(f"Archive '{archive}' extracted successfully.")
        except PermissionError:
            """Если нет прав на запись"""
            print(f"unzip: {archive}: Permission denied")
            log2("unzip", f"{archive}: Permission denied")
        except zipfile.BadZipFile:
            """Если файл не ZIP-архив"""
            print(f"unzip: {archive}: Not a valid ZIP file")
            log2("unzip", f"{archive}: Not a valid ZIP file")
        except Exception as e:
            """Другие ошибки"""
            print(f"unzip: {archive}: {e}")
            log2("unzip", f"{archive}: {e}")

    def tar(self, string):
        """Обрабатываем запрос tar"""
        if len(string) != 2:
            """Если аргументов не 2"""
            print("tar: usage: tar <folder> <archive.tar.gz>")
            return
        folder = string[0]
        archive = string[1]
        log1("tar", string)

        if not os.path.exists(folder):
            """Если папка не существует"""
            print(f"tar: {folder}: No such file or directory")
            log2("tar", f"{folder}: No such file or directory")
            return

        if not os.path.isdir(folder):
            """Если это не директория"""
            print(f"tar: {folder}: Not a directory")
            log2("tar", f"{folder}: Not a directory")
            return

        try:
            """Создаём TAR.GZ-архив"""
            with tarfile.open(archive, "w:gz") as tf:
                """Добавляем папку в архив"""
                tf.add(folder, arcname=os.path.basename(folder))
            print(f"Archive '{archive}' created successfully.")
        except PermissionError:
            """Если нет прав на запись"""
            print(f"tar: {archive}: Permission denied")
            log2("tar", f"{archive}: Permission denied")
        except Exception as e:
            """Другие ошибки"""
            print(f"tar: {archive}: {e}")
            log2("tar", f"{archive}: {e}")

    def untar(self, string):
        """Обрабатываем запрос untar"""
        if len(string) != 1:
            """Если аргументов не 1"""
            print("untar: usage: untar <archive.tar.gz>")
            return
        archive = string[0]
        log1("untar", string)

        if not os.path.exists(archive):
            """Если архив не существует"""
            print(f"untar: {archive}: No such file or directory")
            log2("untar", f"{archive}: No such file or directory")
            return

        try:
            """Открываем TAR.GZ-архив"""
            with tarfile.open(archive, "r:gz") as tf:
                """Пробуем распокавать всё"""
                tf.extractall()
            print(f"Archive '{archive}' extracted successfully.")
        except tarfile.ReadError:
            """Если файл не TAR.GZ-архив"""
            print(f"untar: {archive}: Not a valid TAR.GZ file")
            log2("untar", f"{archive}: Not a valid TAR.GZ file")
        except PermissionError:
            """Если нет прав на запись"""
            print(f"untar: {archive}: Permission denied")
            log2("untar", f"{archive}: Permission denied")
        except Exception as e:
            """Другие ошибки"""
            print(f"untar: {archive}: {e}")
            log2("untar", f"{archive}: {e}")
