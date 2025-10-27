import logging

from commands import get_ls

logging.basicConfig(
    level=logging.INFO,
    filename="shell.log",
    format="[%(asctime)s] %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)

try:
    while True:
        user_input = input("$ ")
        current_str = user_input.split()
        if not current_str:
            continue
        command = current_str[0]
        ost = current_str[1:]
        if command == "ls":
            get_ls(ost)

        elif user_input == "exit":
            break

except KeyboardInterrupt:
    pass
