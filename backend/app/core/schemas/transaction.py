from decimal import Decimal
from pydantic import BaseModel
from typing import List, Optional


class TransactionBaseSchema(BaseModel):
    wallet_name: Optional[str] = None
    from_address: Optional[str] = None
    to_address: Optional[str] = None
    amount: Optional[Decimal] = None


class TransactionSchema(TransactionBaseSchema):
    wallet_name: str
    from_address: str
    to_address: str
    amount: Decimal
