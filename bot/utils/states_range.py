from enum import Enum


class State(Enum):
    """Dialog states"""

    CHOOSE_LANG = 0
    CHECK_PASSWORD = 1
    ADMIN = 2
    GAMES = 3

    READ_TYPE = 4
    READ_AGE = 5
    READ_AMOUNT = 6
    READ_LOCATION = 7
    READ_PROPS = 8

    ANSWER = 9
    BACK_ANSWER = 10
    ADMIN_PASSWORD = 11
