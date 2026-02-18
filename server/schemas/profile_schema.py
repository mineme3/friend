from datetime import date
from typing import Optional
from pydantic import BaseModel, HttpUrl, Field

class UserProfile(BaseModel):
    full_name: str = Field(...)
    bio: str= Field(None, max_length=500)
    date_of_birth: str = None
    address: str= Field(None, example="street , city, Country")
    phone_number: str = Field(None, example="+251 912345678")
class ProfileResponse(BaseModel):
    message: str
    display_name:str
    bio:str
    address:str
    phone_number:str
    isVerified: bool
    account_type:str
