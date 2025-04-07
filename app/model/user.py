from sqlalchemy import Column, Integer, String
from core.database import user_db_base_orm
from sqlalchemy.orm import relationship

class User(user_db_base_orm):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    password = Column(String, nullable=False)

    # Relationship to posts
    posts = relationship("Post", back_populates="user")

