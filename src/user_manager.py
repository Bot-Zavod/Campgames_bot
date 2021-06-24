class UserManager:
    """ manage iser during registration process """

    def __init__(self):
        self.current_users = {}

    def create_user(self, user):
        if user.chat_id not in self.current_users:
            self.current_users[user.chat_id] = user
        else:
            print("ADDING EXISTING USER")

    def delete_user(self, chat_id):
        if chat_id in self.current_users:
            del self.current_users[chat_id]
        else:
            print(f"[WARNING]DELETING UNEXISTING USER {chat_id}")

    # Users stored in dictionary with keys as
    # Structure {
    #   user_id: User-class object
    # }
    # chat_id


user_manager = UserManager()
