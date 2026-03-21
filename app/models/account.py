from datetime import datetime
from decimal import Decimal

from sqlalchemy import DateTime, ForeignKey, Numeric, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base


class Account(Base):
    __tablename__ = "accounts"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    numero: Mapped[int] = mapped_column(unique=True, index=True)
    agencia: Mapped[str] = mapped_column(String(10), default="0001")
    saldo: Mapped[Decimal] = mapped_column(Numeric(12, 2), default=Decimal("0.00"))
    limite: Mapped[Decimal] = mapped_column(Numeric(12, 2), default=Decimal("500.00"))
    limite_saques: Mapped[int] = mapped_column(default=3)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    owner_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), index=True)
    owner = relationship("User", back_populates="contas")
    transacoes = relationship(
        "Transaction",
        back_populates="account",
        cascade="all, delete-orphan",
        order_by="Transaction.created_at.desc()",
    )
