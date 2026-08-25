from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from config import ADMIN_IDS
from database.models import Admin


async def is_admin(
    session: AsyncSession,
    telegram_id: int,
) -> bool:

    result = await session.execute(
        select(Admin).where(
            Admin.telegram_id == telegram_id,
            Admin.is_active.is_(True),
        )
    )

    return result.scalar_one_or_none() is not None


async def get_admin(
    session: AsyncSession,
    telegram_id: int,
) -> Admin | None:

    result = await session.execute(
        select(Admin).where(
            Admin.telegram_id == telegram_id,
            Admin.is_active.is_(True),
        )
    )

    return result.scalar_one_or_none()


async def create_default_admins(
    session: AsyncSession,
) -> None:

    for telegram_id in ADMIN_IDS:

        result = await session.execute(
            select(Admin).where(
                Admin.telegram_id == telegram_id
            )
        )

        admin = result.scalar_one_or_none()

        if admin is None:

            admin = Admin(
                telegram_id=telegram_id,
                name="Administrator",
                is_active=True,
                is_super_admin=True,
            )

            session.add(admin)

    await session.commit()