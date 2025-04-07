from fastapi import Depends, HTTPException
from jose import JWTError, jwt
from core.database import get_db
from services.user import get_user_by_email
from core.config import settings
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/users/login")


def get_current_user(db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)):
    """Validates the JWT token and retrieves the current user."""
    try:
        payload = jwt.decode(token, settings.secret_key, algorithms=[settings.algorithm])
        email = payload.get("sub")
        if not email:
            raise HTTPException(status_code=401, detail="Invalid token.")
        user = get_user_by_email(db, email=email)
        if not user:
            raise HTTPException(status_code=404, detail="User not found.")
        return user
    except JWTError:
        raise HTTPException(status_code=401, detail="Could not validate token: {str(e)}")