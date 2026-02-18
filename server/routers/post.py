from fastapi import HTTPException, APIRouter,Depends
from tools.get_current_user import get_current_user
from models.user import User

from models.posts import Post

router= APIRouter(prefix="/posts", tags=["posts"])

@router.post("/posts", status_code=201,response_model=dict)
async def post(post:Post,current_user: User = Depends(get_current_user)):
    pass