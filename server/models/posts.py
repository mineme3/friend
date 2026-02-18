from sqlalchemy import Column, Integer, Text, ForeignKey, TEXT, func
from sqlalchemy.dialects.postgresql import ENUM, TIMESTAMP, JSON
from sqlalchemy.orm import relationship
from db.database import Base
class Post(Base):
    __tablename__ = 'posts'
    post_id = Column(TEXT,primary_key=True,index=True)
    user_id = Column(TEXT,ForeignKey("users.id"),nullable=False, index=True)
    caption = Column(TEXT,nullable=False, index=True)
    media_type = Column(ENUM("video","image"))
    created_at = Column(TIMESTAMP(timezone=True),nullable=False,server_default= func.now())
    tagged_users = Column(JSON)
    #TODO: relate the post table and user table
    post = relationship("Post", back_populates="tagged_users")
