from sqlalchemy.ext.asyncio.engine import create_async_engine

from app.models import Base
import os
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")


engine = create_async_engine(DATABASE_URL)

async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)