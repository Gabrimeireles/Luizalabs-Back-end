from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_current_user
from app.db.session import get_db
from app.models.user import User
from app.schemas.account import AccountCreate, AccountResponse
from app.services.account_service import (
    create_account_for_user,
    get_account_by_id_for_user,
    list_accounts_by_user,
)

router = APIRouter(prefix="/accounts", tags=["Contas"])


@router.post(
    "",
    response_model=AccountResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Criar conta corrente",
    description="Cria uma conta corrente vinculada ao usuario autenticado.",
)
async def create_account(
    payload: AccountCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    account = await create_account_for_user(
        db,
        owner_id=current_user.id,
        limite=payload.limite,
        limite_saques=payload.limite_saques,
    )
    return account


@router.get(
    "",
    response_model=list[AccountResponse],
    summary="Listar contas do usuario",
    description="Retorna todas as contas correntes do usuario autenticado.",
)
async def list_accounts(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return await list_accounts_by_user(db, owner_id=current_user.id)


@router.get(
    "/{account_id}",
    response_model=AccountResponse,
    summary="Detalhar conta",
    description="Retorna os dados da conta corrente do usuario autenticado.",
)
async def get_account(
    account_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    account = await get_account_by_id_for_user(db, account_id, current_user.id)
    if not account:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Conta nao encontrada.")
    return account
