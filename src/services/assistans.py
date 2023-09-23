import logging

import openai
from sqlalchemy.ext.asyncio import AsyncSession

from src import crud
from src.database import async_session_maker
from src.models import Role
from src.settings import settings

logger = logging.getLogger(__file__)
openai.api_key = settings.API_KEY


class TravelAssistant:
    def __init__(self) -> None:
        self.api = openai
        self.set_message = "Ты помощник для покупки билетов"
        self.system_message = {
            "role": Role.SYSTEM.value,
            "content": self.set_message
        }

    async def request(self, user_id: int, message: str) -> str:
        user_message = message.strip()
        async with async_session_maker() as db:
            context = await self.__get_context(db, user_id)

            messages = []
            messages.append(self.system_message)
            messages.extend(context)
            messages.append({"role": Role.USER.value, "content": user_message})
            response = await openai.ChatCompletion.acreate(
                model=settings.GPT_MODEL,
                messages=messages,
            )

            try:
                assistant_respose = \
                    response["choices"][0]["message"]["content"]
            except Exception as e:
                logger.error(e)
                assistant_respose = \
                    "Не удалось выоплнить запрос, попробуйте позже"

            await self.__save_context(db, Role.USER, user_id, message)
            await self.__save_context(
                db, Role.ASSISTANT, user_id, assistant_respose
            )
            await db.commit()
            return assistant_respose

    async def __save_context(
        self, db: AsyncSession, role: Role, user_id: int, content: str
    ) -> None:
        await crud.add_message(
            db=db,
            user_id=user_id,
            role=role,
            content=content,
        )

    async def __get_context(
        self, db: AsyncSession,  user_id: int
    ) -> list[dict]:
        db_contex = await crud.get_context(db, user_id)
        context = [
            {"role": msg.role.value, "content": msg.content}
            for msg in db_contex
        ]
        return context


trave_assistant = TravelAssistant()
