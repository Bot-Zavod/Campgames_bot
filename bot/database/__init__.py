from random import randint
from typing import Optional

from sqlalchemy import or_
from sqlalchemy.sql import exists

from .connection import local_session
from .models import Game
from .models import User


class DBSession:
    """connection to db"""

    @local_session
    def get_game_names(
        self,
        session,
        game_type=None,
        kids_age=None,
        kids_amount=None,
        location=None,
        props=None,
    ) -> list:
        """list of games by requested parameters"""

        games = session.query(Game.id, Game.name_ru, Game.name_en)

        if game_type is not None:
            games = games.filter(
                or_(Game.game_type.contains(f"%{game_type}%"), Game.game_type.is_(None))
            )
        if kids_age is not None:
            games = games.filter(
                or_(Game.kids_age.contains(f"%{kids_age}%"), Game.kids_age.is_(None))
            )
        if kids_amount is not None:
            games = games.filter(
                or_(
                    Game.kids_amount.contains(f"%{kids_amount}%"),
                    Game.kids_amount.is_(None),
                )
            )
        if location is not None:
            games = games.filter(
                or_(Game.location.contains(f"%{location}%"), Game.location.is_(None))
            )
        if props is not None:
            games = games.filter(
                or_(Game.props.contains(f"%{props}%"), Game.props.is_(None))
            )

        return games.all()

    @local_session
    def get_game_description(self, session, name: str, lang_ru: int = 0) -> str:
        """returns game description by it's name and lang"""

        game_data = (
            [Game.description_ru, Game.name_ru],
            [Game.description_en, Game.name_en],
        )[lang_ru]
        description = session.query(game_data[0]).filter(game_data[1] == name).first()
        return description[0] if description else ""

    @local_session
    def get_random_game_description(self, session, lang_ru: int = 0) -> str:
        """returns random game description by lang"""
        # TODO: prevent error when db is empty
        if not lang_ru:
            query = session.query(Game.description_ru)
        else:
            query = session.query(Game.description_en)
        game = query.filter(Game.id == randint(1, session.query(Game).count())).first()
        return game[0]

    @local_session
    def get_all_games(self, session) -> list:
        games = session.query(
            Game.name_ru,
            Game.name_en,
            Game.description_ru,
            Game.description_en,
            Game.game_type,
            Game.kids_age,
            Game.kids_amount,
            Game.location,
            Game.props,
        ).all()
        return games

    @local_session
    def delete_games(self, session) -> int:
        games_count = session.query(Game).count()
        session.query(Game).delete()
        session.commit()
        return games_count

    @local_session
    def set_games(self, session, games: list):
        objects = [
            Game(
                name_ru=game[0],
                name_en=game[1],
                description_ru=game[2],
                description_en=game[3],
                game_type=game[4],
                kids_age=game[5],
                kids_amount=game[6],
                location=game[7],
                props=game[8],
            )
            for game in games
        ]
        session.bulk_save_objects(objects)
        session.commit()

    @local_session
    def authorize_user(self, session, chat_id: int) -> User:
        user = session.query(User).get(chat_id)
        if not user:
            user = self.create_user(chat_id)
        user.is_registered = True
        session.commit()
        return user

    @local_session
    def create_user(
        self, session, chat_id: int, language: Optional[int] = None
    ) -> User:
        user = session.query(User).get(chat_id)
        if not user:
            user = User(chat_id=chat_id, is_registered=False)
            if language in (0, 1):
                user.language = language
            session.add(user)
            session.commit()
        return user

    @local_session
    def check_user(self, session, chat_id: int) -> bool:
        user = session.query(User).get(chat_id)
        if user:
            return user.is_registered
        return False

    @local_session
    def get_language(self, session, chat_id: int) -> Optional[int]:
        user = session.query(User).get(chat_id)
        if user:
            return user.language
        return None

    @local_session
    def set_language(self, session, chat_id: int, lang: int):
        user = session.query(User).get(chat_id)
        if not user:
            user = self.create_user(chat_id, lang)
        else:
            user.language = lang
            session.commit()


db_interface = DBSession()
