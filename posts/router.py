from fastapi import APIRouter, HTTPException
from sqlalchemy import insert, update, select, delete

from database import async_session_maker
from posts.models import Posts
from posts.shemas import SPostsUpdate, SPosts

router = APIRouter(
    prefix="/posts",
    tags=["posts"],
)

@router.post("/create")
async def create_new_post(data: SPosts):
    valid_data = data.dict()
    async with async_session_maker() as session:
        result = await session.execute(
            insert(Posts).values(**valid_data)
        )
        await session.commit()
    return {"session": "success"}

@router.patch("/update/{post_id}")
async def update_post(post_id: int, data: SPostsUpdate):
    update_data = data.dict(exclude_unset=True)

    if not update_data:
        raise HTTPException(status_code=404, detail="No data found")

    async with async_session_maker() as session:

        search_post = await session.execute(
            select(Posts).where(Posts.id == post_id)
        )

        if search_post.scalar_one_or_none() is None:
            raise HTTPException(status_code=404, detail="No post found")

        result = await session.execute(
            update(Posts).values(**update_data)
        )

        await session.commit()

    return {"session": "success"}

@router.get("/delete/{post_id}")
async def delete_post(post_id: int):
    async with async_session_maker() as session:
        search_post = await session.execute(
            select(Posts).where(Posts.id == post_id)
        )

        if search_post.scalar_one_or_none() is None:
            raise HTTPException(status_code=404, detail="No post found")

        result = await session.execute(
            delete(Posts).where(Posts.id == post_id)
        )
        await session.commit()
    return {"session": "success"}