import os

from archive import ArchiveCommands
from commands import get_cat, get_cd, get_cp, get_ls, get_mv, get_rm


def main():
    # создаём объект архивных команд
    archive = ArchiveCommands()

    try:
        while True:
            current_dir = os.getcwd()
            if not current_dir.startswith(os.path.expanduser("~")):
                """Если текущая дериктория не совпадает с домашней"""
                vivod = current_dir
            else:
                """Получаем домашнюю директорию и проверяем
                не совпадает ли с домашней директорией
                наш путь"""
                home_dir = os.path.expanduser("~")
                if current_dir.startswith(home_dir):
                    vivod = current_dir.replace(home_dir, "~", 1)
                else:
                    vivod = current_dir
            user_input = input(f"{vivod} $ ")
            if user_input == "exit":
                """Ввод exit для выхода"""
                break
            current_str = user_input.split()
            if not current_str:
                """Обрабатываем пустой ввод"""
                continue
            command = current_str[0]
            ost = current_str[1:]
            if command == "cd":
                """Ввод cd"""
                get_cd(ost)
            elif command == "ls":
                """Ввод ls"""
                get_ls(ost)
            elif command == "cat":
                """Ввод cat"""
                get_cat(ost)
            elif command == "mv":
                """Ввод mv"""
                get_mv(ost)
            elif command == "cp":
                """Ввод cp"""
                get_cp(ost)
            elif command == "rm":
                """Ввод rm"""
                get_rm(ost)
            elif command == "grep":
                """Ввод grep"""
                archive.grep(ost)
            elif command == "zip":
                """Ввод zip"""
                archive.zip(ost)
            elif command == "unzip":
                """Ввод unzip"""
                archive.unzip(ost)
            elif command == "tar":
                """Ввод tar"""
                archive.tar(ost)
            elif command == "untar":
                """Ввод untar"""
                archive.untar(ost)
            else:
                print(f"{command}: command not found")

    except KeyboardInterrupt:
        pass


if __name__ == "__main__":
    main()
