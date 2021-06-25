from collections import defaultdict
from .connection import local_session
import sqlite3
from .models import User
from .models import Game
from typing import List

path_to_db = "/Users/vlad-vargan/Documents/prog/Campgames_bot/rename.sqlite"


class DBSession:
    """ connection to db """

    def __init__(self):
        self.conn = sqlite3.connect(path_to_db, check_same_thread=False)
        self.cursor = self.conn.cursor()

    @local_session
    def get_games(
        self, session, game_type=None, kids_age=None, kids_amount=None, location=None, props=None
    ) -> list:
        """ list of games by requested parameters """

        games = session.query(Game.id, Game.name_ru, Game.name_en)

        if game_type is not None:
            games = games.filter(Game.game_type.contains(f"%{game_type}%"))
        if kids_age is not None:
            games = games.filter(Game.kids_age.like(f"%{kids_age}%"))
        if kids_amount is not None:
            games = games.filter(Game.kids_amount.like(f"%{kids_amount}%"))
        if location is not None:
            games = games.filter(Game.location.like(f"%{location}%"))
        if props is not None:
            games = games.filter(Game.props.like(f"%{props}%"))

        return games.all()

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


db_interface = DBSession()

path_to_db = "/Users/vlad-vargan/Documents/prog/Campgames_bot/rename.sqlite"
conn = sqlite3.connect(path_to_db)
cursor = conn.cursor()

cursor.execute("SELECT * FROM Games")


games = defaultdict(list)
for row in cursor.fetchall():
    games[row[0]].append(row[1:])


def merge_g(g1, g2):
    new_g = []
    for i in range(len(g1)):
        if g1[i] != g2[i]:
            new_g.append(str(g1[i]) + str(g2[i]))
        else:
            if g1[i] != None:
                new_g.append(str(g1[i]))
            else:
                new_g.append(g1[i])

    return tuple(new_g)


def to_str(g):
    g = list(g)

    for i in range(len(g)):
        if g[i] != None:
            g[i] = str(g[i])
    return tuple(g)


@ local_session
def migrate(self, session):
    for i, game in games.items():
        if len(game) > 1:
            games[i] = merge_g(*game)
        else:
            games[i] = to_str(game[0])

        print(i, games[i])

        # print(names[i]["ru"])
        # print(games_desc[i])

        new_game = Game(
            id=i,

            name_ru=names[i]["ru"],
            name_en=names[i]["en"],

            description_ru=games_desc[i]["ru"],
            description_en=games_desc[i]["en"],

            game_type=games[i][0],
            kids_age=games[i][1],
            kids_amount=games[i][2],
            location=games[i][3],
            props=games[i][4],
        )
        session.add(new_game)
    session.commit()


# migrate(1)
get_games = db_interface.get_games(1, 1, 2, 1, 1)
print(len(get_games))
for name, game in get_games:
    print(name)
    print(game)
    print()

# DBSession('database.db').set_language_database(10,2)
# print(DBSession('database.db').get_language(10))
# authorize_user()
# print(check_user(100))
# clear_users()
