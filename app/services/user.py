from sqlalchemy.orm import Session
from model.user import User
from schemas.user import UserCreate, LoginCredentials, TokenResponse
from core.config import settings
from jose import jwt, JWTError
from passlib.context import CryptContext
from datetime import datetime, timedelta
from fastapi import HTTPException
from sqlalchemy.exc import SQLAlchemyError
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
def hash_password(password: str) -> str:
    return pwd_context.hash(password)

def create_user(db: Session, user_data: UserCreate) -> User | None:
    try:
        """Creates a new user in the database."""
        hashed_password = hash_password(user_data.password)
        new_user = User(email=user_data.email, password=hashed_password)
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
        return new_user
    except SQLAlchemyError as e:
        db.rollback()  # Rollback transaction in case of error
        logger.error(f"Error creating user: {e}")
        return None
    
def get_user_by_email(db: Session, email: str) -> User | None:
    """Retrieve a user by their email."""
    try:
        user = db.query(User).filter(User.email == email).first()
        if user:
            logger.info(f"User retrieved successfully: {email}")
        else:
            logger.warning(f"No user found with email: {email}")
        return user
    except SQLAlchemyError as e:
        logger.error(f"Error retrieving user by email: {e}")
        return None
    
def get_all_users(db: Session, skip: int = 0, limit: int = 10) -> list[User]:
    """Retrieve a list of all users with optional pagination."""
    try:
        users = db.query(User).offset(skip).limit(limit).all()
        logger.info(f"Retrieved {len(users)} users (skip={skip}, limit={limit}).")
        return users
    except SQLAlchemyError as e:
        logger.error(f"Error retrieving all users: {e}")
        return []
    
def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

def create_token(data:dict, expires_delta: timedelta | None)-> str:
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=settings.access_token_expire_minutes))
    to_encode.update({'exp':expire})

    encoded_jwt = jwt.encode(to_encode, settings.secret_key, algorithm=settings.algorithm)
    return encoded_jwt

def authenticate_user(db:Session, credentials: LoginCredentials) -> TokenResponse | None:
    user = db.query(User).filter(User.email == credentials.email).first()
    if not user or not verify_password(credentials.password, user.password):
        raise HTTPException(status_code=401, detail="Invalid email or password")
    access_token = create_token(data={'sub':user.email}, expires_delta=timedelta(minutes=10))
    return {"access_token": access_token, "token_type":"bearer", "email":user.email}
