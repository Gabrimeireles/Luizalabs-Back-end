from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_current_user
from app.db.session import get_db
from app.models.user import User
from app.schemas.transaction import StatementResponse, TransactionCreate, TransactionResponse
from app.services.account_service import get_account_by_id_for_user
from app.services.transaction_service import create_transaction, get_statement

router = APIRouter(prefix="/accounts/{account_id}", tags=["Transacoes"])


@router.post(
    "/transactions",
    response_model=TransactionResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Registrar transacao",
    description="Registra um deposito ou saque para a conta corrente informada.",
)
async def register_transaction(
    account_id: int,
    payload: TransactionCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    account = await get_account_by_id_for_user(db, account_id, current_user.id)
    if not account:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Conta nao encontrada.")

    transaction = await create_transaction(db, account, payload.tipo, payload.valor)
    return transaction


@router.get(
    "/statement",
    response_model=StatementResponse,
    summary="Consultar extrato",
    description="Retorna o extrato da conta com saldo atual e lista de transacoes.",
)
async def statement(
    account_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    account = await get_account_by_id_for_user(db, account_id, current_user.id)
    if not account:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Conta nao encontrada.")

    transactions = await get_statement(db, account_id=account.id)
    return StatementResponse(conta_id=account.id, saldo_atual=account.saldo, transacoes=transactions)
