from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException

from sqlalchemy.ext.asyncio import AsyncSession

from db.database import get_db

from tools.get_current_user import get_current_user
from schemas.profile_schema import ProfileResponse, UserProfile
from models.user import User


router = APIRouter(prefix="/profile", tags=["profile"])


@router.post("/my_profile", response_model=ProfileResponse)
async def create_my_profile(
    profile:UserProfile,
    profiles: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
)->ProfileResponse:# Assuming this function can fetch user by ID
    if not profiles:
        raise HTTPException(status_code=404, detail="User not found")
    if profiles:
        profiles.full_name = profile.full_name
        profiles.address = profile.address
        profiles.bio = profile.bio
        profiles.phone_number = profile.phone_number
        if profile.date_of_birth:
            if isinstance(profile.date_of_birth, str):
                try:
                    profiles.date_of_birth = datetime.strptime(profile.date_of_birth, "%Y-%m-%d").date()
                except ValueError:
                    raise HTTPException(status_code=400, detail="Invalid date format. Use YYYY-MM-DD.")
            else:
                profiles.date_of_birth = profile.date_of_birth

        db.add(profiles)
    try:
        await db.commit()
        await db.refresh(profiles)
    except Exception as e:
        await db.rollback()
        raise HTTPException(status_code=500, detail="Database error occurred.")


    return ProfileResponse(
        display_name=profiles.full_name,
        address=profiles.address,
        bio=profiles.bio,
        phone_number=profiles.phone_number,
        account_type=profiles.account_type,
        isVerified=profiles.is_verified,
    )
