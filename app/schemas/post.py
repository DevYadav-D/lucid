from pydantic import BaseModel, constr

class PostBase(BaseModel):
    """
    Base schema for post data, includes text and user ID validation.
    """
    text: constr(max_length = 1048576)
    user_id: int

class PostCreate(PostBase):
    pass

class Post(PostBase):
    id: int
    class Config:
        from_attributes = True
