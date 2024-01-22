from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Boolean
from sqlalchemy.orm import relationship
from app.core.database import Base
import uuid

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)  # or UUID
    username = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    is_active = Column(Boolean, default=True)
    is_admin = Column(Boolean, default=False)
    # Add email, etc.

class OAuthClient(Base):
    __tablename__ = "oauth_clients"
    id = Column(Integer, primary_key=True, index=True, default=uuid.uuid4)
    client_id = Column(String, unique=True, index=True)
    client_secret = Column(String)
    redirect_uri = Column(String)

class OAuth2Token(Base):
    __tablename__ = "oauth2_tokens"
    id = Column(Integer, primary_key=True, index=True, default=uuid.uuid4)
    access_token = Column(String, index=True)
    token_type = Column(String)
    refresh_token = Column(String, index=True, nullable=True)
    expires_at = Column(DateTime)
    scopes = Column(String)
    user_id = Column(Integer, ForeignKey("users.id"))  # Match type with User id
    user = relationship("User")

class RefreshToken(Base):
    __tablename__ = "refresh_tokens"
    id = Column(Integer, primary_key=True, index=True, default=uuid.uuid4)
    token = Column(String, unique=True, index=True)
    user_id = Column(Integer, ForeignKey('users.id'))  # Match type with User id
    access_token_id = Column(Integer, ForeignKey("oauth2_tokens.id"))  # Match type with OAuth2Token id
