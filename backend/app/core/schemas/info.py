from pydantic import BaseModel
from typing import Optional


class BlockchainInfoBaseSchema(BaseModel):
    block_height: Optional[int] = None
    latest_block_hash: Optional[str] = None
    transactions_number: Optional[int] = None
    total_amount_circulation: Optional[int] = None


class BlockchainInfoSchema(BlockchainInfoBaseSchema):
    block_height: int
    latest_block_hash: str
    transactions_number: int
    total_amount_circulation: int


class BlockchainInfoByNetworkSchema(BaseModel):
    network: str
    current_block_info: BlockchainInfoSchema
