from fastapi import APIRouter

from core.config import settings
from .bitcoin_info import router as bitcoin_info_router
from .bitcoin_wallet import router as bitcoin_wallet_router
from .bitcoin_transaction import router as bitcoin_transaction_router
from .bitcoin_block import router as bitcoin_block_router

router = APIRouter(
    prefix=settings.api.v1.prefix,
)

router.include_router(bitcoin_info_router)
router.include_router(bitcoin_wallet_router)
router.include_router(bitcoin_transaction_router)
router.include_router(bitcoin_block_router)
