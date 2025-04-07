from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from schemas.post import PostCreate, Post as PostSchema
from services.post import create_post, get_user_posts, delete_post
from core.database import get_db
from routers.dependencies import get_current_user  # Authentication dependency

router = APIRouter(
    prefix="/posts",
    tags=["Posts"],
)

@router.post("/", response_model=PostSchema)
def create_new_post(post_data: PostCreate, db: Session = Depends(get_db), current_user = Depends(get_current_user)):
    """Endpoint to create a new post."""
    new_post = create_post(db, post_data)
    return new_post

@router.get("/", response_model=list[PostSchema])
def get_posts(db: Session = Depends(get_db), current_user = Depends(get_current_user)):
    """Endpoint to get all posts of the current user."""
    posts = get_user_posts(db, user_id=current_user.id)
    return posts

@router.delete("/{post_id}")
def delete_existing_post(post_id: int, db: Session = Depends(get_db), current_user = Depends(get_current_user)):
    """Endpoint to delete a post."""
    try:
        result = delete_post(db, post_id, user_id=current_user.id)
        return {"message": result}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))