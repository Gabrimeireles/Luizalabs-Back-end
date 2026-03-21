from sqlalchemy import Select, func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.account import Account


async def create_account_for_user(
    db: AsyncSession,
    owner_id: int,
    limite,
    limite_saques: int,
    agencia: str = "0001",
) -> Account:
    count_query: Select[tuple[int]] = select(func.count()).select_from(Account)
    total = await db.scalar(count_query)
    numero = int(total or 0) + 1

    account = Account(
        owner_id=owner_id,
        numero=numero,
        agencia=agencia,
        limite=limite,
        limite_saques=limite_saques,
    )
    db.add(account)
    await db.commit()
    await db.refresh(account)
    return account


async def get_account_by_id_for_user(db: AsyncSession, account_id: int, owner_id: int) -> Account | None:
    query: Select[tuple[Account]] = select(Account).where(
        Account.id == account_id,
        Account.owner_id == owner_id,
    )
    result = await db.execute(query)
    return result.scalar_one_or_none()


async def list_accounts_by_user(db: AsyncSession, owner_id: int) -> list[Account]:
    query: Select[tuple[Account]] = select(Account).where(Account.owner_id == owner_id)
    result = await db.execute(query)
    return list(result.scalars().all())
