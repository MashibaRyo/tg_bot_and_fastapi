from sqlalchemy import insert, select

from database import async_session_maker

class BaseDAO:
    model = None

    @classmethod
    async def create(cls, **kwargs):
        async with async_session_maker() as session:
            query = await session.execute(
                insert(cls.model).values(**kwargs)
            )
            await session.commit()

    @classmethod
    async def find_one_or_none(cls, **kwargs) -> dict | None :
        async with async_session_maker() as session:
            query = await session.execute(
                select(cls.model).filter_by(**kwargs)
            )
            result = query.scalars().first()
            if result:
                return {c.key: getattr(result, c.key) for c in result.__table__.columns}
            return None




