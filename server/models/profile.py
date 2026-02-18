from sqlalchemy import DATE, TEXT, Column, ForeignKey
from sqlalchemy.orm import relationship

from db.database import Base


class Profile(Base):
    __tablename__ = "profiles"
    id = Column(TEXT, primary_key=True, index=True)
    user_id = Column(TEXT, ForeignKey("users.id"),unique=True,nullable=False, index=True)
    first_name = Column(TEXT, nullable=True)
    father_name = Column(TEXT, nullable=True)
    grand_father_name = Column(TEXT, nullable=True)
    profile_picture_url = Column(TEXT, nullable=True)
    background_picture_url = Column(TEXT, nullable=True)
    bio = Column(TEXT, nullable=True)
    date_of_birth = Column(DATE, nullable=True)
    address = Column(TEXT, nullable=True)
    phone_number = Column(TEXT, nullable=True)
    owner = relationship("User", back_populates="profile", uselist=False)