from fastapi import APIRouter, HTTPException

from bitcoin_adapter.rpc_helper import get_bitcoin_rpc_client
from bitcoin_adapter.wallet_service import BitcoinWalletService
from core.config import settings

router = APIRouter(
    prefix=settings.api.v1.bitcoin_wallet,
    tags=["Bitcoin Wallet"],
)


@router.get("/{wallet_name}")
async def get_wallet(wallet_name: str) -> dict:
    network = settings.bitcoin_node.network
    path = f"/wallet/{wallet_name}"
    rpc_client = get_bitcoin_rpc_client(path)
    info = await BitcoinWalletService(rpc_client).get_wallet_info()
    if info is None:
        raise HTTPException(404, f"'{wallet_name}' wallet does not exist")
    return {
        "network": network,
        "wallet_name": wallet_name,
        "addresses": info,
    }
