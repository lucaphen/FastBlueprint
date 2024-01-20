from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase

# database connection
SQLALCHEMY_DATABASE_URL = "sqlite:///./fast_blueprint.db"

class Base(DeclarativeBase): 
    pass

# intialize engine
engine = create_engine(SQLALCHEMY_DATABASE_URL)
session_local = sessionmaker(autocommit=False, autoflush=False, bind=engine)
