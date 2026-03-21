from datetime import timedelta

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import settings
from app.core.security import create_access_token
from app.db.session import get_db
from app.schemas.user import Token, UserCreate, UserResponse
from app.services.auth_service import authenticate_user, create_user, get_user_by_username

router = APIRouter(prefix="/auth", tags=["Autenticacao"])


@router.post(
    "/register",
    response_model=UserResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Cadastrar usuario",
    description="Cria um novo usuario para autenticacao e acesso aos recursos da API.",
)
async def register(payload: UserCreate, db: AsyncSession = Depends(get_db)):
    user_exists = await get_user_by_username(db, payload.username)
    if user_exists:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Ja existe usuario com esse username.",
        )

    user = await create_user(db, payload.username, payload.password)
    return user


@router.post(
    "/login",
    response_model=Token,
    summary="Autenticar usuario",
    description="Retorna um token JWT para uso nos endpoints protegidos.",
)
async def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: AsyncSession = Depends(get_db),
):
    user = await authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Usuario ou senha invalidos.",
            headers={"WWW-Authenticate": "Bearer"},
        )

    token_expires = timedelta(minutes=settings.access_token_expire_minutes)
    access_token = create_access_token(subject=user.username, expires_delta=token_expires)
    return Token(access_token=access_token)
