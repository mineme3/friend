from fastapi import APIRouter, Depends,UploadFile, File, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from db.database import get_db
from models.profile import Profile
from models.user import User
from routers.auth import get_current_user
from schemas.user_schema import SignUpResponse
from pathlib import Path
from PIL import Image
import aiofiles, io, uuid

router = APIRouter(
    prefix="/profiles",
    tags=["profiles"]
)
UPLOAD_DIR = Path("uploads/profiles")
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)

async def upload_profile_picture(
    file:UploadFile = File(),
    current_user: User = Depends(get_current_user)
):
    # Validate file type and size
    if file.content_type not in ["image/jpeg", "image/png", "image/webp"]:
        raise HTTPException(400, "Only JPG, PNG, WebP allowed")

    if file.size > 5 * 1024 * 1024:           # 5 MB limit
        raise HTTPException(400, "File too large")
    #validate the file cotent is an actual image
    content =await file.read()
    await file.seek(0)
    try:
        img = Image.open(io.BytesIO(content))
        img.verify()
    except Exception:
        raise HTTPException(400, "Invalid image file")
    # taking the file extension and generating a unique filename
    ext = file.filename.split(".")[-1].lower()
    filename = f"{uuid.uuid4()}.{ext}"
    file_path = UPLOAD_DIR / filename

    async with aiofiles.open(file_path, "wb") as f:
        await f.write(content)
    #TODO : save the url into the user's profile in the database

@router.post("/create")
async def create_profile(profile: Profile, db: AsyncSession = Depends(get_db)):
    profile_db = Profile(
        id = SignUpResponse.id,  # taking the user id from the signup response
        first_name = profile.first_name,
        last_name = profile.last_name,
        bio = profile.bio,
        date_of_birth = profile.date_of_birth,
        address = profile.address,
        phone_number = profile.phone_number
    )
    try:
        db.add(profile_db)
        await db.commit() 
        await db.refresh(profile_db)
    except Exception as e:
        await db.rollback()
        raise e

    return {"message": "Profile created successfully", "profile_id": profile_db.id}