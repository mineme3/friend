import datetime
import jwt
from core.config import settings


def create_access_token(data: dict, expires_minutes: int = 5):
    to_encode = data.copy()
    expire = datetime.datetime.now() + datetime.timedelta(minutes=expires_minutes)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    return encoded_jwt 