from fastapi import FastAPI, HTTPException, Depends
from fastapi.security import OAuth2PasswordBearer
from pydantic import BaseModel
from passlib.context import CryptContext
from jose import jwt, JWTError
from datetime import datetime, timedelta

oauth2_schema = OAuth2PasswordBearer(tokenUrl = "login")
SECRET_KEY = "super-secret-key"# the secret key should be more complex and kept on the environment variables of the server 
ALGORITHM = "HS256"


app = FastAPI()
pwd_context = CryptContext(schemes = ["bcrypt"], deprecated = "auto")
class LoginRequest(BaseModel):
    username: str
    password: str

def get_current_user(token: str = Depends(oauth2_schema)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms = [ALGORITHM])
        return payload
    except JWTError:
        raise HTTPException(status_code = 401, detail = "Invalid token")
# this function is used to hash the incoming password using passlib context
def hash_password(password: str) -> str:
    return pwd_context.hash(password)
# verify password is the function i created to cerify the hashed password with the plain password
# it uses the verify method from passlib context
def verify_password(plain_password: str , hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

#this function creates the access token using the jose jwt library
# it takes the data to be encoded and the expiration time in minutes as parameters
def create_access_token(data:dict,expire_minutes:int = 2) -> str:
    payload = data.copy()
    expire = datetime.utcnow() + timedelta(minutes = expire_minutes)
    payload.update({"exp": expire})
    token = jwt.encode(payload, SECRET_KEY, algorithm = ALGORITHM )
    return token




test_user = {
    "username" : "testuser"
    ,"password" : hash_password("123456")
}

@app.post("/login")
def login(data: LoginRequest):
    verified = verify_password(data.password, test_user["password"])
    if data.username != test_user["username"] or not verified:
        raise HTTPException(status_code = 401, detail = "invalid credentials")
    token = create_access_token({"sub": data.username})
    return {"access_token": token, "token-type": "bearer"}


@app.get("/profile")
def profile(current_user: dict = Depends(get_current_user)):
    return current_user
