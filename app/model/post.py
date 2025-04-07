from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from core.database import user_db_base_orm

class Post(user_db_base_orm):
    __tablename__ = "posts"  

    id = Column(Integer, primary_key=True, index=True)
    text = Column(String, nullable=False)  
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)  

    # Relationship to user
    user = relationship("User", back_populates="posts")
