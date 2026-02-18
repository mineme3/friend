from pydantic import BaseModel, EmailStr, Field
class UserSignUp(BaseModel):
    username: str = Field(...,min_length=3,max_length=50)
    email: EmailStr = Field(..., max_length=255,min_length=6)
    password: str = Field(...,min_length=8)
    
    class Config:
        json_schema_extra = {
            "example": {
                "username": "testuser",
                "email": "testuser@gmail.com",
                "password": "strongpassword123"
            }
        }

    
class SignUpResponse(BaseModel):
    user_id: str
    access_token: str
    token_type:str  = "bearer"

class UserLogin(BaseModel):
    identity:str = Field(...,min_length=3,max_length=255)
    password: str = Field(...,min_length=8)


class LoginResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
