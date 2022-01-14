import os


PASSWORD_FILE = os.path.join("data", "password.txt")


def get_password() -> str:
    with open(PASSWORD_FILE, "r") as file:
        password = file.readline().strip()
    return password


def validate_password(possible_password: str) -> bool:
    with open(PASSWORD_FILE, "r") as file:
        password = file.readline().strip()
    return possible_password == password


def write_password(password: str) -> None:
    with open(PASSWORD_FILE, "w") as file:
        file.write(password)
