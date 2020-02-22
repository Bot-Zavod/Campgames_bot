import sqlite3

class DbInterface:
    def __init__(self, path):
        self.conn = sqlite3.connect(path, check_same_thread=False)
        self.cursor = self.conn.cursor()

    def getGames(self, type=None, age=None, amount=None, location=None, props=None):
        sql = "SELECT DISTINCT Id FROM Games WHERE "
        args = [type]
        sql += 'Type=?'
        if age is not None:
            sql += 'AND (Age=? OR Age is NULL)'
            args.append(age)
        if amount is not None:
            sql += 'AND (Amount=? OR Amount is NULL)'
            args.append(amount)
        if location is not None:
            sql += 'AND (Location=? OR Location is NULL)'
            args.append(location)
        if props is not None:
            sql += 'AND (Props=? OR Props is NULL)'
            args.append(props)
        self.cursor.execute(sql, args)
        data = self.cursor.fetchall()
        return data if len(data) == 0 else tuple(d[0] for d in data)

    def authorizeUser(self, chat_id):
        sql = 'INSERT INTO Users (Chat_id) VALUES (?)'
        args = [chat_id]
        try:
            self.cursor.execute(sql, args)
            self.conn.commit()
        except sqlite3.IntegrityError:
            print("User exists")

    def clearUsers(self):
        sql = 'DELETE FROM USERS'
        try:
            self.cursor.execute(sql)
            self.conn.commit()
        except sqlite3.IntegrityError:
            print("ERROR")

    def checkUser(self, chat_id):
        sql = 'SELECT EXISTS(SELECT * from Users Where Chat_id = ?)'
        args = [chat_id]
        self.cursor.execute(sql, args)
        return True if self.cursor.fetchall()[0][0] == 1 else False

    def setLang(self, chat_id, lang):
        sql = 'INSERT OR REPLACE INTO Lang (Chat_id, lang) VALUES (?, ?)'
        args = [chat_id, lang]
        try:
            self.cursor.execute(sql, args)
            self.conn.commit()
        except sqlite3.IntegrityError:
            print("error")

    def getLang(self, chat_id):
        sql = 'SELECT EXISTS(SELECT * from Lang Where Chat_id = ?)'
        args = [chat_id]
        # print(chat_id)
        try:
            self.cursor.execute(sql, args)
            self.conn.commit()
        except sqlite3.IntegrityError:
            print("error")
        if self.cursor.fetchall()[0][0] == 0:
            return None
        sql = 'SELECT Lang from Lang Where Chat_id = ?'
        args = [chat_id]
        try:
            self.cursor.execute(sql, args)
            self.conn.commit()
        except sqlite3.IntegrityError:
            print("error")
        return self.cursor.fetchall()[0][0]

    
# print(getGames(0,0,0,0,0))
# DbInterface('database.db').setLang(10,2)
# print(DbInterface('database.db').getLang(10))
# authorizeUser()
# print(checkUser(100))
# clearUsers()