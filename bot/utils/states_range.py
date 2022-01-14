from enum import Enum


class State(Enum):
    """Dialog states"""

    CHOOSE_LANG = 0
    CHECK_PASSWORD = 1
    ADMIN = 2
    GAMES = 3

    GET_TYPE = 4
    GET_AGE = 5
    GET_AMOUNT = 6
    GET_LOCATION = 7
    GET_PROPS = 8

    ANSWER = 9
    BACK_ANSWER = 10
    ADMIN_PASSWORD = 11
