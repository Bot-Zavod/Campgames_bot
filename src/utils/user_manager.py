from typing import Dict

from ..database import db_interface


class User:
    """ Telegram user """

    def __init__(self, chat_id: int, username: str):
        self.chat_id: int = chat_id
        self.username: str = username
        self.lang: int = db_interface.get_language(self.chat_id)
        self.answers: list = [None, None, None, None, None]

    def __repr__(self):
        return f"User {self.username} with chat id: {self.chat_id}"

    def set_lang(self, lang: int):
        self.lang = lang

    def set_flag(self, flag: int):
        self.flag = flag

    def take_answer(self, question_num: int, answer: int):
        self.answers[question_num] = answer


class UserManager:
    """ manage iser during registration process """

    def __init__(self):
        self.current_users: Dict[int, User] = {}

    def create_user(self, user: User):
        if user.chat_id not in self.current_users:
            self.current_users[user.chat_id] = user
        else:
            print("ADDING EXISTING USER")

    def delete_user(self, chat_id: int):
        if chat_id in self.current_users:
            del self.current_users[chat_id]
        else:
            print(f"[WARNING]DELETING UNEXISTING USER {chat_id}")


user_manager = UserManager()
