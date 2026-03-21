from contextlib import asynccontextmanager

from fastapi import FastAPI

from app import models  # noqa: F401
from app.api.router import api_router
from app.core.config import settings
from app.db.base import Base
from app.db.session import engine


@asynccontextmanager
async def lifespan(_: FastAPI):
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield


app = FastAPI(
    title=settings.app_name,
    version="1.0.0",
    description=(
        "API bancaria assincrona com autenticacao JWT para contas correntes, "
        "depositos, saques e consulta de extrato."
    ),
    lifespan=lifespan,
)

app.include_router(api_router)


@app.get("/health", tags=["Health"], summary="Saude da API")
async def health_check():
    return {"status": "ok"}
