from models import *
from sqlalchemy_utils import database_exists, create_database, drop_database
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from log_writer import setup_logger
import inspect
import psycopg2
from config_reader import read_config



engine = None
logger = None
if not logger:
    logger = setup_logger(__name__)


def db_error_handler(func):
    MAX_RECONNECT_ATTEMPTS = 3

    def wrapper(*args, **kwargs):
        reconnect_attempts = 0
        try:
            # assert isinstance(args[0], Session)
            return func(*args, **kwargs)
        # except AssertionError as e:
        #     logger.error(f"Function {inspect.currentframe().f_back.f_code.co_name} dont have session argument "
        #                  f"that is demanded by error decorator", exc_info=True)
        # except OperationalError as e:
        #     logger.error(f"OperationalError in function '{inspect.currentframe().f_back.f_code.co_name}: "
        #                  f"{e}. Attempting to reconnect...")
        #     session, engine = database_init()
        #     return func(session, *args, **kwargs)
        except Exception as e:
            error_type = type(e).__name__
            logger.error(f"Database error of type {error_type} in function "
                         f"'{inspect.currentframe().f_back.f_code.co_name}': {str(e)}", exc_info=True)

    return wrapper


### системные функции
def database_init():
    sqlalchemy_config = read_config('postgresql')
    db_url = f"postgresql://{sqlalchemy_config['user']}:" \
             f"{sqlalchemy_config['password']}@{sqlalchemy_config['host']}:" \
             f"{sqlalchemy_config['port']}/{sqlalchemy_config['database']}"
    global engine

    if engine is None:
        engine = create_engine(db_url, pool_size=10, max_overflow=5)
        if not database_exists(engine.url):
            create_database(engine.url)
        Base.metadata.create_all(bind=engine)
    session = sessionmaker(bind=engine)()
    return session, engine


def database_session(func):
    def wrapper(*args, **kwargs):
        session, _ = database_init()
        return func(session, *args, **kwargs)

    return wrapper


def recreate_db():
    global engine
    session, engine = database_init()
    drop_database(engine.url)
    engine = None
    session, engine = database_init()


if __name__ == '__main__':
    database_init()
    # print(*get_all_excursions(), sep='\n')