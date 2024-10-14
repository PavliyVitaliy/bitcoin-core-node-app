from fastapi import APIRouter

from bitcoin_adapter.rpc_helper import get_bitcoin_rpc_client
from core.config import settings
from core.schemas.info import BlockchainInfoByNetworkSchema
from core.services.info_service import InfoService

router = APIRouter(
    prefix=settings.api.v1.bitcoin_info,
    tags=["Bitcoin Info"],
)


@router.get("/current-block", response_model=BlockchainInfoByNetworkSchema)
async def get_current_block():
    network = settings.bitcoin_node.network
    rpc_client = get_bitcoin_rpc_client()
    info = await InfoService(rpc_client).get_current_block_info()
    return {
        "network": network,
        "current_block_info": info,
    }
