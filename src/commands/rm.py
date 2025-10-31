import os
import shutil

from logger import log1, log2


def get_rm(string):
    if len(string) == 0:
        """Обрабатываем ввод пустого пути"""
        raise ValueError("missing file operand")

    path = [x for x in string if x != "-r"]
    # Находим путь без rm
    if len(path) == 0:
        """Если не был передан путь файла/директории"""
        raise ValueError("missing file operand")

    log1("rm", string)
    path1 = path[0]  # Определяем путь
    path2 = os.path.abspath(path1)

    if path2 == os.path.abspath("..") or path2 == "/":
        """Предотвращаем удаление корневого и родительского каталога"""
        raise PermissionError(f"cannot remove '{path1}': Operation not permitted")

    try:
        if not os.path.exists(path1):
            raise FileNotFoundError(
                f"cannot remove '{path1}': No such file or directory"
            )

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
                    log1("rm, " f"cancelled for '{path1}'")
            else:
                """Если нет -r"""
                raise IsADirectoryError(f"cannot remove '{path1}': Is a directory")
    except (FileNotFoundError, PermissionError, IsADirectoryError) as e:
        """Ловим ошибки и перевыбрасываем их"""
        log2("rm", str(e))
        raise
    except OSError as e:
        """Ошибка системы"""
        log2("rm", f"cannot remove '{path1}': {e}")
        raise OSError(f"cannot remove '{path1}': {e.strerror}")
