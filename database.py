from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker, DeclarativeBase
from env import DATABASE_URL

engine = create_async_engine(
    DATABASE_URL,
    echo=True,
    future=True
)

async_session_maker = sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False,
    autoflush=False
)
class Base(DeclarativeBase):
    pass
