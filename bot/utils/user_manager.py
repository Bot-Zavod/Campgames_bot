from enum import Enum
from typing import Dict
from typing import Optional

from loguru import logger

from bot.database import db_interface


class QuestionType(str, Enum):
    TYPE = "type"
    AGE = "age"
    AMOUNT = "amount"
    LOCATION = "location"
    PROPS = "props"


class User:
    """Telegram user"""

    def __init__(self, chat_id: int, username: str):
        self.chat_id: int = chat_id
        self.username: str = username
        self.lang: int = db_interface.get_language(self.chat_id)
        self.answers: Dict[QuestionType, Optional[int]] = {
            QuestionType.TYPE: None,
            QuestionType.AGE: None,
            QuestionType.AMOUNT: None,
            QuestionType.LOCATION: None,
            QuestionType.PROPS: None,
        }

    def __repr__(self):
        return f"User {self.username} with chat id: {self.chat_id}"

    def set_lang(self, lang: int):
        self.lang = lang

    def set_flag(self, flag: int):
        self.flag = flag


class UserManager:
    """manage iser during registration process"""

    def __init__(self):
        self.current_users: Dict[int, User] = {}

    def create_user(self, user: User):
        if user.chat_id not in self.current_users:
            self.current_users[user.chat_id] = user
        else:
            logger.warning("ADDING EXISTING USER")

    def delete_user(self, chat_id: int):
        if chat_id in self.current_users:
            del self.current_users[chat_id]
        else:
            logger.warning(f"[WARNING]DELETING UNEXISTING USER {chat_id}")

    def take_answer(
        self, chat_id: int, question_type: QuestionType, answer: Optional[int]
    ):
        user = self.current_users[chat_id]
        user.answers[question_type] = answer


user_manager = UserManager()
