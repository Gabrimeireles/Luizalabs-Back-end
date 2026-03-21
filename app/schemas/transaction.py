from datetime import datetime
from decimal import Decimal
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field


class TransactionCreate(BaseModel):
    tipo: Literal["deposito", "saque"]
    valor: Decimal = Field(gt=0)


class TransactionResponse(BaseModel):
    id: int
    tipo: str
    valor: Decimal
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


class StatementResponse(BaseModel):
    conta_id: int
    saldo_atual: Decimal
    transacoes: list[TransactionResponse]
