import uuid
from fastapi import Depends, File, HTTPException, UploadFile
from sqlalchemy import select
from db.database import get_db
from models.user import User
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import APIRouter

from schemas.profile_schema import ProfileResponse
from tools.images import imagekit
from tools.get_current_user import get_current_user

router = APIRouter(
    prefix="/profile/upload",
    tags = ["profile photo"]
)


@router.patch("/myprofile", response_model=dict)
async def upload_profile_photo(
    user_db: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
    profile_image: UploadFile = File(None),
    background_image: UploadFile = File(None),
)->ProfileResponse:

    contents = await profile_image.read()
    ext = profile_image.filename.rsplit(".", 1)[-1]
    unique_name = f"{uuid.uuid4().hex}.{ext}"
    response = imagekit.files.upload(
        file = contents,
        file_name= unique_name,
        folder = "profile/avatar",
        use_unique_file_name=True,

    )
    p_url = response.url
    contents = await background_image.read()
    ext = background_image.filename.rsplit(".",1)[-1]
    unique_name = f"{uuid.uuid4().hex}.{ext}"
    response = imagekit.files.upload(
        file = contents,
        file_name = background_image.filename,
        folder = "profile/background",
        use_unique_file_name=True,
    )
    bg_url = response.url
    try:
        if user_db:
            user_db.profile_picture_url = p_url
            user_db.background_picture_url = bg_url
            db.add(user_db)

        try:
            await db.commit()
            await db.refresh(user_db)
        except Exception as e:
            await db.rollback()
            raise HTTPException(status_code=500, detail="Database error occurred.")
    except Exception as e:
        await db.rollback()
        raise HTTPException(status_code=500, detail="Database error occurred.")
    return ProfileResponse(
        message = f"Profile picture upload successful."
    )