from aiogram import Dispatcher, F
from aiogram.filters import CommandStart
from aiogram.types import Message

from src import crud
from src.chat_bot.keyboards import clear_context_keyboard
from src.database import async_session_maker
from src.services.assistans import trave_assistant


async def cmd_start(message: Message) -> None:
    async with async_session_maker() as db:
        await crud.create_user(
            db=db,
            user_id=message.from_user.id,
            first_name=message.from_user.first_name,
            last_name=message.from_user.last_name,
            username=message.from_user.username,
        )
        await db.commit()

    await message.answer(f"Привет, {message.from_user.full_name}!")


async def cmd_clear_content(message: Message) -> None:
    async with async_session_maker() as db:
        await crud.clear_context(
            db=db,
            user_id=message.from_user.id,
        )
        await db.commit()

    await message.answer("Контекст очищен")


async def handle_message(msg: Message) -> None:
    assistant_respose = await trave_assistant.request(
        msg.from_user.id, msg.text
    )
    await msg.answer(assistant_respose, reply_markup=clear_context_keyboard)


def register_main_handlers(dp: Dispatcher):
    dp.message.register(cmd_start, CommandStart())
    dp.message.register(cmd_clear_content, F.text == "Очистить контекст")
    dp.message.register(handle_message)
