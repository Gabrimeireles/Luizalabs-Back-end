from datetime import datetime
from decimal import Decimal

from pydantic import BaseModel, ConfigDict, Field


class AccountCreate(BaseModel):
    limite: Decimal = Field(default=Decimal("500.00"), gt=0)
    limite_saques: int = Field(default=3, ge=1, le=10)


class AccountResponse(BaseModel):
    id: int
    numero: int
    agencia: str
    saldo: Decimal
    limite: Decimal
    limite_saques: int
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)
