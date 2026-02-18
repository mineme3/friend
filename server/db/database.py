from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from core.config import settings

Base = declarative_base()
engine = create_async_engine(settings.DATABASE_URL, echo=True)
AsyncSessionLocal = async_sessionmaker(engine, expire_on_commit= False)
async def get_db():
    try:
        async with AsyncSessionLocal() as session:
            yield session
    except Exception as e:
        await session.rollback()
        raise 
    finally:
        await session.close()
