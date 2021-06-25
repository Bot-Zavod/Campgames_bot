from functools import wraps
from os import path
from .models import Base

from sqlalchemy import create_engine
from sqlalchemy.engine.url import URL
from sqlalchemy.orm import sessionmaker


base_dir = path.dirname(path.dirname(path.dirname(path.abspath(__file__))))
sqlite_dir = path.join(base_dir, "database.sqlite")
sqlite_db = {"drivername": "sqlite", "database": sqlite_dir}
sqlite_uri = URL(**sqlite_db)
print("sqlite_uri: ", sqlite_uri)
sqlite_engine = create_engine(sqlite_uri)
Session = sessionmaker(bind=sqlite_engine)

Base.metadata.create_all(sqlite_engine)


def testdb():
    """ run empty transaction """
    try:
        Session().execute("SELECT 1 WHERE false;")
        print("-------- DB conn test Successful --------")
    except Exception as error:
        print("!!!!!!!! DB conn test Failed !!!!!!!!")
        raise ValueError(error) from error  # notify developer


testdb()


def local_session(function):
    """ build and close local session """

    @wraps(function)
    def wrapped(self, *args, **kwargs):
        session = Session()
        try:
            result = function(self, session, *args, **kwargs)
        except Exception as error:
            # in case commit wan't be rolled back next trasaction failed
            session.rollback()
            raise ValueError(error) from error  # notify developer
        session.close()
        return result
    return wrapped
