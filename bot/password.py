import os


PASSWORD_FILE = os.path.join("data", "password.txt")
DEFAULT_PASSWORD = "2222"


def get_password() -> str:
    if os.path.exists(PASSWORD_FILE):
        with open(PASSWORD_FILE, "r") as file:
            password = file.readline().strip()
        return password
    return DEFAULT_PASSWORD


def validate_password(possible_password: str) -> bool:
    if os.path.exists(PASSWORD_FILE):
        with open(PASSWORD_FILE, "r") as file:
            password = file.readline().strip()
    else:
        password = DEFAULT_PASSWORD
    return possible_password == password


def write_password(password: str) -> None:
    with open(PASSWORD_FILE, "w") as file:
        file.write(password)
