from model.post import Post
from schemas.post import PostCreate, Post as postschema
from sqlalchemy.orm import Session


def create_post(db: Session, post_data: PostCreate) -> Post:
    """Creates a new post for the given user."""
    new_post = Post(text=post_data.text, user_id=post_data.user_id)
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post

def get_user_posts(db: Session, user_id: int) -> list[Post]:
    """Retrieves all posts created by a specific user."""
    posts = db.query(Post).filter(Post.user_id == user_id).all()
    return posts

def delete_post(db: Session, post_id: int, user_id: int) -> str:
    """Deletes a post for the given user."""
    post = db.query(Post).filter(Post.id == post_id, Post.user_id == user_id).first()
    if not post:
        raise Exception("Post not found or user is not authorized to delete it.")
    db.delete(post)
    db.commit()
    return f"Post {post_id} deleted successfully."