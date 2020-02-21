from database import DbInterface
db = DbInterface(r"database.db")

class UserManager:

    def __init__(self):
        self.currentUsers = {}

    def create_user(self, user):
        if user.chat_id not in self.currentUsers:
            self.currentUsers[user.chat_id] = user
        else:
            print('ADDING EXISTING USER')

    def delete_user(self, chat_id):
        if chat_id in self.currentUsers:
            del self.currentUsers[chat_id]
        else:
            print(f'[WARNING]DELETING UNEXISTING USER {chat_id}')

    # Users stored in dictionary with keys as 
    # Structure {
    #   user_id: User-class object 
    # }
    # chat_id

class User:
    def __init__(self, chat_id, username):
        self.chat_id = chat_id
        self.username = username
        self.lang = db.getLang(self.chat_id)
        self.answers = [None,None,None,None,None]

    def __repr__(self):
        return f'User {self.username} with chat id: {self.chat_id}'

    def set_lang(self, lang):
        self.lang = lang

    def set_flag(self, flag):
        self.flag = flag

    def take_answer(self, n, answer):
        self.answers[n] = answer

# if __name__ == "__main__":
#     user = User(100500)
#     user.addQuestions([1,2,3,4,5])
#     user.addAnswer(1, 0)
#     print(user.answers)