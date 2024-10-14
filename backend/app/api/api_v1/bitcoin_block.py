from fastapi import APIRouter
from bitcoin_adapter.rpc_helper import get_bitcoin_rpc_client
from core.config import settings
from core.services.helper_service import HelperService

router = APIRouter(
    prefix=settings.api.v1.bitcoin_block,
    tags=["Bitcoin Block"],
)


@router.post(
    "/generate",
    response_model=dict,
    description="Uses for regtest node only"
)
async def generate_blocks(
        wallet_name: str,
        address: str,
        blocks: int,
):
    network = settings.bitcoin_node.network
    path = f"/wallet/{wallet_name}"
    rpc_client = get_bitcoin_rpc_client(path)
    generated_blocks = await HelperService(rpc_client).generate_blocks(address, blocks)
    return {
        "network": network,
        "wallet_name": wallet_name,
        "address": address,
        "generated_blocks": generated_blocks,
    }
