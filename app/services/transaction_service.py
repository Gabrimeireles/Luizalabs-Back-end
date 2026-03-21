from decimal import Decimal

from fastapi import HTTPException, status
from sqlalchemy import Select, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.account import Account
from app.models.transaction import Transaction


async def create_transaction(
    db: AsyncSession,
    account: Account,
    tipo: str,
    valor: Decimal,
) -> Transaction:
    if valor <= 0:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="O valor deve ser maior que zero.",
        )

    if tipo == "deposito":
        account.saldo += valor

    elif tipo == "saque":
        if valor > account.limite:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="O valor do saque excede o limite por operacao.",
            )

        count_query: Select[tuple[Transaction]] = select(Transaction).where(
            Transaction.account_id == account.id,
            Transaction.tipo == "saque",
        )
        saques = (await db.execute(count_query)).scalars().all()

        if len(saques) >= account.limite_saques:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Numero maximo de saques excedido.",
            )

        if valor > account.saldo:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Saldo insuficiente para saque.",
            )

        account.saldo -= valor

    else:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="Tipo de transacao invalido.",
        )

    transaction = Transaction(tipo=tipo, valor=valor, account_id=account.id)
    db.add(transaction)
    await db.commit()
    await db.refresh(transaction)
    return transaction


async def get_statement(db: AsyncSession, account_id: int) -> list[Transaction]:
    query: Select[tuple[Transaction]] = (
        select(Transaction)
        .where(Transaction.account_id == account_id)
        .order_by(Transaction.created_at.desc())
    )
    result = await db.execute(query)
    return list(result.scalars().all())
