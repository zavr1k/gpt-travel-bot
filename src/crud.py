from typing import Optional

from sqlalchemy import insert, select, update
from sqlalchemy.ext.asyncio import AsyncSession

from .models import Message, Role, User


async def get_user(db: AsyncSession, user_id: int) -> Optional[User]:
    query = select(User).filter_by(id=user_id)
    result = await db.execute(query)
    return result.scalar_one_or_none()


async def create_user(
    db: AsyncSession,
    user_id: int,
    first_name: str,
    last_name: Optional[str] = None,
    username: Optional[str] = None,
):
    exist = await get_user(db, user_id)
    if not exist:
        stmt = (
            insert(User)
            .values(
                id=user_id,
                first_name=first_name,
                last_name=last_name,
                username=username,
            )
            .returning(User.id)
        )
        await db.execute(stmt)


async def add_message(
    db: AsyncSession,
    user_id: int,
    role: Role,
    content: Optional[str] = None,
) -> int:
    stmt = (
        insert(Message)
        .values(
            user_id=user_id,
            role=role,
            content=content,
        )
        .returning(Message.id)
    )
    insert_result = await db.execute(stmt)
    return insert_result.scalar_one()


async def get_context(db: AsyncSession, user_id: int):
    stmt = select(Message).filter_by(user_id=user_id, is_in_context=True)
    insert_result = await db.execute(stmt)
    return insert_result.scalars().all()


async def clear_context(db: AsyncSession, user_id: int) -> None:
    stmt = (
        update(Message)
        .where(
            Message.user_id == user_id,
            Message.is_in_context.is_(True),
        )
        .values(is_in_context=False)
    )
    await db.execute(stmt)
