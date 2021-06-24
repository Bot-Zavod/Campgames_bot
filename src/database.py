import sqlite3
import sys
from os import path

from sqlalchemy import create_engine
from sqlalchemy.engine.url import URL
from sqlalchemy.orm import sessionmaker


base_dir = path.dirname(path.dirname(path.abspath(__file__)))
sqlite_dir = path.join(base_dir, "database.sqlite")
sqlite_db = {"drivername": "sqlite", "database": sqlite_dir}
sqlite_uri = URL(**sqlite_db)
print(sqlite_uri)
sqlite_engine = create_engine(sqlite_uri)
Session = sessionmaker(bind=sqlite_engine)


def testdb():
    """ run empty transaction """

    try:
        Session().execute("SELECT 1 WHERE false;")
        print("-------- DB conn test Successful --------")
    except Exception as error:
        print("!!!!!!!! DB conn test Failed !!!!!!!!")
        print(error)


testdb()

sys.exit()

# print("\nDB_URI: ", db_uri, "\n")

# echo_value = "-db" in sys.argv
# print("-" * 6, "SQLalchemy logging is " + str(echo_value), "-" * 6, "\n")

# m.Base.metadata.create_all(postgres_engine)


class DbInterface:
    """ connection to db """

    def __init__(self, path_to_db):
        self.conn = sqlite3.connect(path_to_db, check_same_thread=False)
        self.cursor = self.conn.cursor()

    def get_games(
        self, game_type=None, age=None, amount=None, location=None, props=None
    ):
        sql = "SELECT DISTINCT Id FROM Games WHERE "
        args = [game_type]
        sql += "Type=?"
        if age is not None:
            sql += "AND (Age=? OR Age is NULL)"
            args.append(age)
        if amount is not None:
            sql += "AND (Amount=? OR Amount is NULL)"
            args.append(amount)
        if location is not None:
            sql += "AND (Location=? OR Location is NULL)"
            args.append(location)
        if props is not None:
            sql += "AND (Props=? OR Props is NULL)"
            args.append(props)
        self.cursor.execute(sql, args)
        data = self.cursor.fetchall()
        return data if len(data) == 0 else tuple(d[0] for d in data)

    def authorize_user(self, chat_id):
        sql = "INSERT INTO Users (Chat_id) VALUES (?)"
        args = [chat_id]
        try:
            self.cursor.execute(sql, args)
            self.conn.commit()
        except sqlite3.IntegrityError:
            print("User exists")

    def clear_users(self):
        sql = "DELETE FROM USERS"
        try:
            self.cursor.execute(sql)
            self.conn.commit()
        except sqlite3.IntegrityError:
            print("ERROR")

    def check_user(self, chat_id):
        sql = "SELECT EXISTS(SELECT * from Users Where Chat_id = ?)"
        args = [chat_id]
        self.cursor.execute(sql, args)
        return self.cursor.fetchall()[0][0] == 1

    def set_language_database(self, chat_id, lang):
        sql = "INSERT OR REPLACE INTO Lang (Chat_id, lang) VALUES (?, ?)"
        args = [chat_id, lang]
        try:
            self.cursor.execute(sql, args)
            self.conn.commit()
        except sqlite3.IntegrityError:
            print("error")

    def get_language(self, chat_id):
        sql = "SELECT EXISTS(SELECT * from Lang Where Chat_id = ?)"
        args = [chat_id]
        # print(chat_id)
        try:
            self.cursor.execute(sql, args)
            self.conn.commit()
        except sqlite3.IntegrityError:
            print("error")
        if self.cursor.fetchall()[0][0] == 0:
            return None
        sql = "SELECT Lang from Lang Where Chat_id = ?"
        args = [chat_id]
        try:
            self.cursor.execute(sql, args)
            self.conn.commit()
        except sqlite3.IntegrityError:
            print("error")
        return self.cursor.fetchall()[0][0]


db_interface = DbInterface(r"database.db")

# print(get_games(0,0,0,0,0))
# DbInterface('database.db').set_language_database(10,2)
# print(DbInterface('database.db').get_language(10))
# authorize_user()
# print(check_user(100))
# clear_users()
