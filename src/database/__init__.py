from random import randint
from typing import List
from typing import Optional

from sqlalchemy import or_
from sqlalchemy.sql import exists

from .connection import local_session
from .models import Game
from .models import User


class DBSession:
    """ connection to db """

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
        """ list of games by requested parameters """

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

        if not lang_ru:
            description = (
                session.query(Game.description_ru).filter(Game.name_ru == name).first()
            )
        description = (
            session.query(Game.description_en).filter(Game.name_en == name).first()
        )

        return description[0] if description else ""

    @local_session
    def get_random_game_description(self, session, lang_ru: int = 0) -> str:
        """returns random game description by lang"""
        if not lang_ru:
            query = session.query(Game.description_ru)
        else:
            query = session.query(Game.description_en)
        game = query.filter(Game.id == randint(1, session.query(Game).count())).first()
        return game[0]

    @local_session
    def authorize_user(self, session, chat_id: int) -> User:
        user = session.query(User).get(chat_id)
        if not user:
            user = User(
                chat_id=chat_id,
            )
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
            user = self.authorize_user(chat_id)
        user.language = lang
        session.commit()


db_interface = DBSession()
