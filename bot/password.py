from bot.config import settings

PASSWORD_FILE = settings.APP_DIR / "data" / "password.txt"
DEFAULT_PASSWORD: str = "2222"


def get_password() -> str:
    if PASSWORD_FILE.exists():
        with PASSWORD_FILE.open() as file:
            password = file.readline().strip()
        return password
    return DEFAULT_PASSWORD


def validate_password(possible_password: str) -> bool:
    if PASSWORD_FILE.exists():
        with PASSWORD_FILE.open() as file:
            password = file.readline().strip()
    else:
        password = DEFAULT_PASSWORD
    return possible_password == password


def write_password(password: str) -> None:
    with PASSWORD_FILE.open("w") as file:
        file.write(password)
