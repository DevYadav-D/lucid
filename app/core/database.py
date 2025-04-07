from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base, Session
from core.config import settings

user_db_base_orm = declarative_base()
user_db_engine = create_engine(settings.database_url)
user_db_session_local = sessionmaker(bind= user_db_engine, autocommit= False, autoflush= False)

def init_db():
    try:
        user_db_base_orm.metadata.create_all(bind=user_db_engine)
        print("User&post  db initialized successfully")
    except Exception as e:
        print(f'Error in initializing the user db: {e}')

def get_db() -> Session:
    db = user_db_session_local()
    try:
        yield db
    finally:
        db.close()

