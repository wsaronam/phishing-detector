from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base




DATABASE_URL = "sqlite:///./scans.db"

engine = create_engine(
    DATABASE_URL,
    connect_args={'check_same_thread': False}
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


def get_db():
    '''
    provides DB on request and closes even if something happens
    '''
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()



def init_db():
    '''
    Creates tables if they don' texist
    '''
    from app.models import db_models
    Base.metadata.create_all(bind=engine)