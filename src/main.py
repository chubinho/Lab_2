import logging

from commands import get_cat, get_cd, get_cp, get_ls, get_mv, get_rm

logging.basicConfig(
    level=logging.INFO,
    filename="shell.log",
    format="[%(asctime)s] %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)


def main():
    try:
        while True:
            user_input = input("$ ")
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

            else:
                print(f"{command}: command not found")

    except KeyboardInterrupt:
        pass


if __name__ == "__main__":
    main()
