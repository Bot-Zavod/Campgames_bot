from functools import wraps

from sqlalchemy import create_engine
from sqlalchemy.engine.url import URL
from sqlalchemy.orm import sessionmaker
from sqlalchemy.sql import text

from bot.config import settings
from bot.database.models import Base


sqlite_dir = settings.APP_DIR / "db" / "db.sqlite3"
sqlite_url = URL.create(drivername="sqlite", database=str(sqlite_dir))
print("sqlite_url: ", sqlite_url)
sqlite_engine = create_engine(sqlite_url)
Session = sessionmaker(bind=sqlite_engine)

Base.metadata.create_all(sqlite_engine)


def testdb():
    """run empty transaction"""
    try:
        Session().execute(text("SELECT 1 WHERE false;"))
        print("-------- DB conn test Successful --------")
    except Exception as error:
        print("!!!!!!!! DB conn test Failed !!!!!!!!")
        raise ValueError(error) from error  # notify developer


testdb()


def local_session(function):
    """build and close local session"""

    @wraps(function)
    def wrapped(self, *args, **kwargs):
        session = Session()
        try:
            try:
                result = function(self, session, *args, **kwargs)
            except ValueError:
                session.close()
                return None
        except Exception as error:
            # in case commit wan't be rolled back next trasaction failed
            session.rollback()
            raise ValueError(error) from error  # notify developer
        session.close()
        return result

    return wrapped
