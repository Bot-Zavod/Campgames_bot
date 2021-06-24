from .database import DbInterface

db_interface = DbInterface(r"database.db")


class User:
    """ Telegram user """

    def __init__(self, chat_id, username):
        self.chat_id = chat_id
        self.username = username
        self.lang = db_interface.get_language(self.chat_id)
        self.answers = [None, None, None, None, None]

    def __repr__(self):
        return f"User {self.username} with chat id: {self.chat_id}"

    def set_lang(self, lang):
        self.lang = lang

    def set_flag(self, flag):
        self.flag = flag

    def take_answer(self, question_num, answer):
        self.answers[question_num] = answer


# if __name__ == "__main__":
#     user = User(100500)
#     user.addQuestions([1,2,3,4,5])
#     user.addAnswer(1, 0)
#     print(user.answers)
