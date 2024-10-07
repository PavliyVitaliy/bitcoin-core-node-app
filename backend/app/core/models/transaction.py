from sqlalchemy import func, Integer, String, Numeric, DateTime
from sqlalchemy.orm import Mapped, mapped_column

from core.models import Base


class Transaction(Base):
    id: Mapped[int] = mapped_column(Integer, primary_key=True, unique=True)
    tx_id: Mapped[str] = mapped_column(String, unique=True, nullable=False)
    input_address: Mapped[str] = mapped_column(String)
    output_address: Mapped[str] = mapped_column(String)
    amount: Mapped[Numeric] = mapped_column(Numeric)
    timestamp: Mapped[DateTime] = mapped_column(DateTime)
    vouts: Mapped[int] = mapped_column(Integer)
