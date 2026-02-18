import uuid, bcrypt
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import or_ , select
from sqlalchemy.ext.asyncio import AsyncSession
from db.database import get_db
from models.user import User
from tools.create_token import create_access_token
from schemas.user_schema import SignUpResponse, UserLogin, UserSignUp, LoginResponse
 
router = APIRouter(
    prefix="/users",
    tags=["users"]
)

@router.post("/signup", response_model=SignUpResponse)
async def sign_up(user: UserSignUp,status_code = 201, description = "User created successfully", db: AsyncSession = Depends(get_db))->SignUpResponse:
    user_db = await db.execute(select(User).where(
        or_(
            User.email == user.email, User.username == user.username))
    )
    encrypted_password = bcrypt.hashpw(user.password.encode(), bcrypt.gensalt())
    if user_db.scalars().first():
        raise HTTPException(
            status_code=400,
            detail="User already exists!"
        )
    user_db = User(
        user_id = str(uuid.uuid4()),
        username=user.username.strip(),
        email=user.email.strip(),
        password_hash = encrypted_password,
    )
    try:
        db.add(user_db)
        await db.commit() 
        await db.refresh(user_db)
    except Exception as e:
        await db.rollback()
        raise e
    access_token = create_access_token(data={"sub":user_db.id})

    return SignUpResponse(user_id=user_db.user_id, access_token=access_token, token_type ="bearer")

@router.post("/login", status_code=200, response_model=LoginResponse)
async def login(user:UserLogin, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(User).where(
        or_(
            User.email == user.identity, User.username == user.identity)
            )
        )
    user_db = result.scalars().first()

    verified = verify_password(user.password, user_db.password_hash)

    if not user_db or not verified:
       raise HTTPException(status_code=401, detail="invalid credentials")

    access_token = create_access_token(data={"sub": user_db.user_id})

    return LoginResponse(
        access_token=access_token,
        token_type="bearer"
    )

def verify_password(plain_password, hashed_password) -> bool:
    return bcrypt.checkpw(plain_password.encode(), hashed_password)