from typing import Any

from sqlalchemy import BigInteger
from sqlalchemy import Boolean
from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import MetaData
from sqlalchemy import String
from sqlalchemy.ext.declarative import declarative_base

meta = MetaData(  # automatically name constraints to simplify migrations
    naming_convention={
        "ix": "ix_%(column_0_label)s",
        "uq": "uq_%(table_name)s_%(column_0_name)s",
        "ck": "ck_%(table_name)s_%(column_0_name)s",
        "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
        "pk": "pk_%(table_name)s",
    }
)
# Any saves from mypy checks of a dynamic class
Base: Any = declarative_base(metadata=meta)


class User(Base):
    """telegram user"""

    __tablename__ = "user"

    chat_id = Column(BigInteger, primary_key=True)
    username = Column(String(35))  # Telegram allows username no longer then 32
    is_registered = Column(Boolean)
    language = Column(Integer)  # 1 - en, 0 - ru

    def __repr__(self):
        # pylint: disable-next=consider-using-f-string
        return "<User(chat_id='{}', username='{}', is_registered='{}', language='{}')>".format(
            self.chat_id, self.username, self.is_registered, self.language
        )


class Game(Base):
    """game for children"""

    __tablename__ = "game"

    id = Column(Integer, primary_key=True)
    """name_ru = Column(String)
    name_en = Column(String)
    description_ru = Column(String)
    description_en = Column(String)"""
    name = Column(String)
    description = Column(String)
    game_type = Column(String)
    kids_age = Column(String)
    kids_amount = Column(String)
    location = Column(String)
    props = Column(String)

    def __repr__(self):
        # pylint: disable-next=consider-using-f-string
        return "<Game(id='{}', name_ru='{}')>".format(self.id, self.name_ru)
