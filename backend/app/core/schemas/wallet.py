from decimal import Decimal

from pydantic import BaseModel
from typing import List, Optional


class AddressBaseSchema(BaseModel):
    address: Optional[str] = None
    amount: Optional[float] = None
    confirmations: Optional[int] = None
    label: Optional[str] = None
    tx_ids: Optional[List[str]] = None


class WalletBaseSchema(BaseModel):
    network: Optional[str] = None
    wallet_name: Optional[str] = None


class WalletCreateSchema(WalletBaseSchema):
    network: str
    wallet_name: str


class WalletLoadSchema(WalletCreateSchema):
    pass


class WalletReadSchema(WalletBaseSchema):
    network: str
    wallet_name: str
    addresses: Optional[List[AddressBaseSchema]] = None


class WalletAddressCreateSchema(WalletBaseSchema):
    network: str
    wallet_name: str
    address: str


class WalletBalanceSchema(WalletBaseSchema):
    network: str
    wallet_name: str
    balance: Decimal
