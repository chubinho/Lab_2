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
            raise ValueError("usage: grep <pattern> <path>")
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
            log2("grep", f"invalid pattern: {e}")
            raise

        # Проверяем, что путь существует
        if not os.path.exists(path):
            raise FileNotFoundError(f"{path}: No such file or directory")

        if os.path.isfile(path):
            """Обрабатываем если файл"""
            self._grep_file(path, reg)
        elif os.path.isdir(path):
            """Если это директория"""
            if "-r" in string:
                # Проходим по всем поддиректориям и файлам в них
                for tek_dir, pod_dir, files in os.walk(path):
                    for file in files:
                        """Получаем полный путь к файлу"""
                        full_path = os.path.join(tek_dir, file)
                        """Обрабатываем файл"""
                        self._grep_file(full_path, reg)
            else:
                # Получаем файлы в директории
                for file in os.listdir(path):
                    """Получаем полный путь"""
                    full_path = os.path.join(path, file)
                    """Проверяем, что это файл"""
                    if os.path.isfile(full_path):
                        """Обрабатываем файл"""
                        self._grep_file(full_path, reg)
        else:
            """Если путь не файл и не директория"""
            raise ValueError(f"{path}: No such file or directory")

    def _check_line_for_match(self, line, reg):
        """Возвращает совпадение или None"""
        return reg.search(line).group(0) if reg.search(line) else None

    def _grep_file(self, file_path, reg):
        """Обрабатываем один файл для grep"""
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                """Проходим по строкам файла"""
                for line_num, line in enumerate(f, 1):
                    """Проверяем, подходит ли строка под шаблон"""
                    found_text = self._check_line_for_match(line, reg)
                    if found_text:
                        """Если строка подходит
                        Выводим результат"""
                        print(f"{file_path}: {line_num}: {found_text}")
        except PermissionError:
            """Если нет прав для открытия файла"""
            raise PermissionError(f"{file_path}: Permission denied")
        except UnicodeDecodeError:
            """Если файл не текстовый"""
            pass
        except Exception as e:
            """Другие ошибки"""
            raise RuntimeError(f"{file_path}: {e}")

    def zip(self, string):
        """Обрабатываем запрос zip"""
        if len(string) != 2:
            """Если аргументов не 2"""
            raise ValueError("usage: zip <folder> <archive.zip>")
        folder = string[0]
        archive = string[1]
        log1("zip", string)

        if not os.path.exists(folder):
            raise FileNotFoundError(f"{folder}: No such file or directory")

        if not os.path.isdir(folder):
            raise NotADirectoryError(f"{folder}: Not a directory")

        try:
            """Создаём ZIP-архив"""
            with zipfile.ZipFile(archive, "w", zipfile.ZIP_DEFLATED) as zf:
                """Проходим по файлам в указанной папке"""
                for tek_dir, dirs, files in os.walk(folder):
                    for file in files:
                        # Получаем путь к файлу и добавляем его в архив
                        full_path = os.path.join(tek_dir, file)
                        arc_name = os.path.relpath(full_path, folder)
                        zf.write(full_path, arc_name)
            print(f"Archive '{archive}' created successfully.")
        except PermissionError:
            """Нет доступа"""
            raise PermissionError(f"{archive}: Permission denied")
        except Exception as e:
            """Другие ошибки"""
            raise RuntimeError(f"{archive}: {e}")

    def unzip(self, string):
        """Обрабатываем запрос unzip"""
        if len(string) != 1:
            raise ValueError("usage: unzip <archive.zip>")
        archive = string[0]
        log1("unzip", string)

        if not os.path.exists(archive):
            """Если архив не существует"""
            raise FileNotFoundError(f"{archive}: No such file or directory")

        try:
            """Открываем ZIP-архив"""
            with zipfile.ZipFile(archive, "r") as zf:
                """Распаковываем всё"""
                zf.extractall()
            print(f"Archive '{archive}' extracted successfully.")
        except PermissionError:
            """Нет доступа"""
            raise PermissionError(f"{archive}: Permission denied")
        except zipfile.BadZipFile:
            """Если файл не ZIP-архив"""
            log2("unzip", f"{archive}: Not a valid ZIP file")
            raise
        except Exception as e:
            """Другие ошибки"""
            raise RuntimeError(f"{archive}: {e}")

    def tar(self, string):
        """Обрабатываем запрос tar"""
        if len(string) != 2:
            raise ValueError("usage: tar <folder> <archive.tar.gz>")
        folder = string[0]
        archive = string[1]
        log1("tar", string)

        if not os.path.exists(folder):
            raise FileNotFoundError(f"{folder}: No such file or directory")

        if not os.path.isdir(folder):
            raise NotADirectoryError(f"{folder}: Not a directory")

        try:
            """Создаём TAR.GZ-архив"""
            with tarfile.open(archive, "w:gz") as tf:
                """Добавляем папку в архив"""
                tf.add(folder, arcname=os.path.basename(folder))
            print(f"Archive '{archive}' created successfully.")
        except PermissionError:
            """Нет доступа"""
            raise PermissionError(f"{archive}: Permission denied")
        except Exception as e:
            """Другие ошибки"""
            raise RuntimeError(f"{archive}: {e}")

    def untar(self, string):
        """Обрабатываем запрос untar"""
        if len(string) != 1:
            raise ValueError("usage: untar <archive.tar.gz>")
        archive = string[0]
        log1("untar", string)

        if not os.path.exists(archive):
            raise FileNotFoundError(f"{archive}: No such file or directory")

        try:
            """Открываем TAR.GZ-архив"""
            with tarfile.open(archive, "r:gz") as tf:
                """Пробуем распокавать всё"""
                tf.extractall()
            print(f"Archive '{archive}' extracted successfully.")
        except tarfile.ReadError:
            """Если файл не TAR.GZ-архив"""
            log2("untar", f"{archive}: Not a valid TAR.GZ file")
            raise
        except PermissionError:
            """Нет доступа"""
            raise PermissionError(f"{archive}: Permission denied")
        except Exception as e:
            """Другие ошибки"""
            raise RuntimeError(f"{archive}: {e}")
