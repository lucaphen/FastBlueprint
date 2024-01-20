"""
    File: authentication.py
    Type: route
    Explanation: This route facilitates CRUD operations for the Authentication Service.
    Author: @lucaphen Github
"""
# dependencies
from fastapi import APIRouter, Request, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from app.api.schema.response import ResponseModel, ErrorResponseModel
from app.api.schema.contracts import Contract
from app.core.dependencies import limiter, get_db
from app.core.config import (
    RATE_LIMIT, # 10/minute
    ACCESS_TOKEN_EXPIRE_MINUTES # 30 seconds
)
from app.services.hashing import Hash
from app.services.oauth2 import (
    create_access_token,
    get_current_user,
    verify_token
)
from typing import List
from app.models.authentication import User, OAuth2Token, OAuthClient, RefreshToken
from app.api.schema import UserBase, UserCreate, UserResponse

# development dependencies
from datetime import date, timedelta

# Router initialization
router = APIRouter()

@router.post("/register", response_model=UserResponse)
@limiter.limit(RATE_LIMIT)
def register_user(
    request: Request,
    user: UserCreate, 
    db: Session = Depends(get_db)
):
    # Check if user already exists
    db_user = db.query(User).filter(User.username == user.username).first()
    if db_user:
        raise HTTPException(status_code=400, detail="Username already registered")
    
    # create user
    hashed_password = Hash.bcrypt(user.password)
    new_user = User(username=user.username, hashed_password=hashed_password)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user



@router.post("/token")
@limiter.limit(RATE_LIMIT)
async def generate_token(
    request: Request,
    form_data: OAuth2PasswordRequestForm = Depends(), 
    db: Session = Depends(get_db)
):
    # fetch user
    user = db.query(User).filter(User.username == form_data.username).first()
    if not user or not Hash.verify(user.hashed_password, form_data.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # generate access token
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}



@router.get("/users", response_model=List[UserResponse])
@limiter.limit(RATE_LIMIT)
def get_users(
    request: Request,
    db: Session = Depends(get_db), 
    current_user: User = Depends(get_current_user)
):  
    # check admin access
    if not current_user.is_admin:
        raise HTTPException(status_code=403, detail="Not enough permissions")
    
    # fetch all users
    users = db.query(User).all()
    return users

@router.get("/users/{user_id}", response_model=UserResponse)
@limiter.limit(RATE_LIMIT)
def get_user(
    request: Request,
    user_id: int, 
    db: Session = Depends(get_db), 
    current_user: User = Depends(get_current_user)
):
    # check if admin user
    if not current_user.is_admin:
        raise HTTPException(status_code=403, detail="Not enough permissions")
    
    # fetch user
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@router.delete("/users/{user_id}", response_model=UserResponse)
@limiter.limit(RATE_LIMIT)
def delete_user(
    request: Request,
    user_id: int, 
    db: Session = Depends(get_db), 
    current_user: User = Depends(get_current_user)
):
    # check if user is admin
    if not current_user.is_admin:
        raise HTTPException(status_code=403, detail="Not enough permissions")
    
    # fetch user
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    # delete user
    db.delete(user)
    db.commit()
    return user