from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from schemas.user import UserCreate, LoginCredentials, User
from services.user import create_user, authenticate_user, get_user_by_email
from core.database import get_db

router = APIRouter(
    prefix="/users",
    tags=["Users"],
)

@router.post("/signup", response_model=User)
def signup(user_data: UserCreate, db: Session = Depends(get_db)):
    """Endpoint for user signup."""
    existing_user = get_user_by_email(db, email=user_data.email)
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered.")
    new_user = create_user(db, user_data)
    if not new_user:
        raise HTTPException(status_code=500, detail="Error creating user.")
    return new_user

@router.post("/login")
def login(credentials: LoginCredentials, db: Session = Depends(get_db)):
    """Endpoint for user login."""
    token_response = authenticate_user(db, credentials)
    return token_response