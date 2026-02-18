from sqlalchemy import TEXT, VARCHAR, Column, LargeBinary, DateTime, func, Enum, BOOLEAN
from sqlalchemy.dialects.postgresql import TIMESTAMP
from sqlalchemy.orm import relationship
from db.database import Base

class User(Base):
    __tablename__ = "users"
    user_id = Column(TEXT, primary_key=True, index=True)
    username = Column(VARCHAR(50), unique=True, index=True, nullable=False)
    full_name = Column(VARCHAR(50), nullable=True)
    email = Column(VARCHAR(100), unique=True, index=True, nullable=False)
    bio = Column(TEXT, nullable=True)
    password_hash = Column(LargeBinary, nullable=False)
    profile_photo = Column(TEXT, nullable=True)
    background_photo = Column(TEXT, nullable=True)
    date_of_birth = Column(DateTime, nullable=True)
    address = Column(VARCHAR(255), nullable=True)
    phone_number = Column(VARCHAR(255), nullable=True)
    account_type = Column(Enum("private","public"))
    created_at = Column(TIMESTAMP(timezone=True, ), nullable=False, server_default=func.now())
    last_login = Column(TIMESTAMP(timezone=True, ), nullable=False, server_default=func.now())
    is_verified = Column(BOOLEAN, default=False)