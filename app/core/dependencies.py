# dependencies
from fastapi.security import OAuth2PasswordBearer
from slowapi import Limiter
from slowapi.util import get_remote_address
from .database import session_local

# dependency for the rate limiter
limiter = Limiter(key_func=get_remote_address)

# dependency for authentication
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/token")

# dependency to get the database session
def get_db(): 
    database = session_local()
    try: 
        yield database
    finally: 
        database.close()
