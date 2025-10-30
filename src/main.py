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
                vivod = current_dir
            else:
                home_dir = os.path.expanduser("~")
                if current_dir.startswith(home_dir):
                    vivod = current_dir.replace(
                        home_dir, "~", 1
                    )  # заменить только первое вхождение
                else:
                    vivod = current_dir
            user_input = input(f"{vivod} $ ")
            if user_input == "exit":
                break
            current_str = user_input.split()
            if not current_str:
                continue
            command = current_str[0]
            ost = current_str[1:]
            if command == "cd":
                get_cd(ost)
            elif command == "ls":
                get_ls(ost)
            elif command == "cat":
                get_cat(ost)
            elif command == "mv":
                get_mv(ost)
            elif command == "cp":
                get_cp(ost)
            elif command == "rm":
                get_rm(ost)
            elif command == "grep":
                archive.grep(ost)
            elif command == "zip":
                archive.zip(ost)
            elif command == "unzip":
                archive.unzip(ost)
            elif command == "tar":
                archive.tar(ost)
            elif command == "untar":
                archive.untar(ost)
            else:
                print(f"{command}: command not found")

    except KeyboardInterrupt:
        pass


if __name__ == "__main__":
    main()
