from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from core.config import settings
from db.database import engine, Base
from routers import auth, create_user_profile, create_profile_photo

async def create_tables():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

@asynccontextmanager
async def lifespan(app: FastAPI):
    await create_tables()
    yield

app = FastAPI(
        title="Mini social API",
        description="backend",
        version="1.0.0",
        docs_url="/docs",
        redoc_url="/redoc",
        lifespan=lifespan
)

#for front end to let from allowed origins
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=settings.ALLOWED_METHODS,
    allow_headers=["*"],
)

app.include_router(auth.router, prefix = settings.API_PREFIX)
app.include_router(create_user_profile.router, prefix = settings.API_PREFIX)
app.include_router(upload_image.router, prefix=settings.API_PREFIX)