from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import Command
from aiogram.utils.keyboard import InlineKeyboardBuilder
from fastapi import FastAPI
from sqlalchemy import select
import uvicorn
import asyncio
import logging
from datetime import date  # Добавлен импорт

from database import async_session_maker
from posts.models import Posts
from posts.router import router as posts_router
from env import token

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI()
app.include_router(posts_router)

bot = Bot(token=token)
dp = Dispatcher()

@dp.message(Command("posts"))
async def show_posts(message: types.Message):
    async with async_session_maker() as session:
        result = await session.execute(select(Posts))
        posts = result.scalars().all()

        if not posts:
            await message.answer("Пока нет доступных постов.")
            return

        builder = InlineKeyboardBuilder()
        for post in posts:
            builder.button(
                text=post.headline,
                callback_data=f"show_post:{post.id}"
            )
        builder.adjust(1)

        await message.answer(
            "Список постов:",
            reply_markup=builder.as_markup()
        )


@dp.callback_query(F.data.startswith("show_post:"))
async def show_post_content(callback: types.CallbackQuery):
    post_id = int(callback.data.split(":")[1])

    async with async_session_maker() as session:
        result = await session.execute(select(Posts).where(Posts.id == post_id))
        post = result.scalar_one_or_none()

        if not post:
            await callback.answer("Пост не найден!", show_alert=True)
            return

        created_date = post.created.strftime("%d.%m.%Y") if post.created else "Не указана"

        response = (
            f"<b>{post.headline}</b>\n\n"
            f"{post.text}\n\n"
            f"<i>Дата создания: {created_date}</i>"
        )

        await callback.message.answer(
            response,
            parse_mode="HTML"
        )
        await callback.answer()


async def start_bot():
    try:
        await dp.start_polling(bot)
    except Exception as e:
        logger.error(f"Bot polling error: {e}")
    finally:
        await bot.session.close()
        logger.info("Bot stopped")


@app.on_event("startup")
async def startup_event():
    asyncio.create_task(start_bot())


@app.on_event("shutdown")
async def shutdown_event():
    await bot.session.close()
    logger.info("Bot session closed")


if __name__ == "__main__":
    config = uvicorn.Config(
        "main:app",
        host="127.0.0.1",
        port=8000,
        reload=True,
        workers=1
    )
    server = uvicorn.Server(config)
    asyncio.run(server.serve())