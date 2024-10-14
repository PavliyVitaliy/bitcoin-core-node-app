from fastapi import APIRouter

from bitcoin_adapter.rpc_helper import get_bitcoin_rpc_client
from core.config import settings
from core.schemas.wallet import (
    WalletReadSchema,
    WalletCreateSchema,
    WalletLoadSchema,
    WalletAddressCreateSchema,
    WalletBalanceSchema,
)
from core.services.wallet_service import WalletService

router = APIRouter(
    prefix=settings.api.v1.bitcoin_wallet,
    tags=["Bitcoin Wallet"],
)


@router.get("/{wallet_name}", response_model=WalletReadSchema)
async def get_wallet(wallet_name: str):
    network = settings.bitcoin_node.network
    path = f"/wallet/{wallet_name}"
    rpc_client = get_bitcoin_rpc_client(path)
    info = await WalletService(rpc_client).get_wallet_info()
    return {
        "network": network,
        "wallet_name": wallet_name,
        "addresses": info,
    }


@router.get("/{wallet_name}/balance", response_model=WalletBalanceSchema)
async def get_wallet_balance(wallet_name: str):
    network = settings.bitcoin_node.network
    path = f"/wallet/{wallet_name}"
    rpc_client = get_bitcoin_rpc_client(path)
    balance = await WalletService(rpc_client).get_wallet_balance()
    return {
        "network": network,
        "wallet_name": wallet_name,
        "balance": balance,
    }


@router.post("/create", response_model=WalletCreateSchema, status_code=201)
async def create_wallet(wallet_name: str):
    network = settings.bitcoin_node.network
    rpc_client = get_bitcoin_rpc_client()
    name = await WalletService(rpc_client).create_wallet(wallet_name)
    return {
        "network": network,
        "wallet_name": name,
    }


@router.post("/load", response_model=WalletLoadSchema, status_code=201)
async def load_wallet(wallet_name: str):
    network = settings.bitcoin_node.network
    rpc_client = get_bitcoin_rpc_client()
    name = await WalletService(rpc_client).load_wallet(wallet_name)
    return {
        "network": network,
        "wallet_name": name,
    }


@router.post("/createnewaddress", response_model=WalletAddressCreateSchema, status_code=201)
async def create_new_address(wallet_name: str):
    network = settings.bitcoin_node.network
    path = f"/wallet/{wallet_name}"
    rpc_client = get_bitcoin_rpc_client(path)
    address = await WalletService(rpc_client).create_new_address()
    return {
        "network": network,
        "wallet_name": wallet_name,
        "address": address,
    }
