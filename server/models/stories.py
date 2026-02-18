from sqlalchemy.dialects.postgresql import TIMESTAMP

from db.database import Base
from sqlalchemy import Column, TEXT


class Story(Base):
    __tablename__ = "story"
    post_id = Column(TEXT, primary_key=True)
    created_at = Column(TIMESTAMP(timezone=True, ), nullable=False)
