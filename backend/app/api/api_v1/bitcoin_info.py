from fastapi import APIRouter
from bitcoinrpc import BitcoinRPC

from bitcoin_adapter.info_service import BitcoinInfoService
from bitcoin_adapter.rpc_helper import get_bitcoin_rpc_client
from core.config import settings

router = APIRouter(
    prefix=settings.api.v1.bitcoin_info,
    tags=["Bitcoin Info"],
)


@router.get("/current-block")
async def get_current_block() -> dict:
    network = settings.bitcoin_node.network
    rpc_client = get_bitcoin_rpc_client()
    info = await BitcoinInfoService(rpc_client).get_current_block_info()
    return {
        "network": network,
        "current_block_info": info,
    }
