from decimal import Decimal
from typing import List
from fastapi import HTTPException
from bitcoinrpc import BitcoinRPC, RPCError

from bitcoin_adapter.wallet import BitcoinWallet

import logging

logging.basicConfig()
logging.getLogger("BitcoinRPC").setLevel(logging.DEBUG)

"""
CRUD of bitcoin wallet
"""


class WalletService:
    def __init__(self, rpc_client: BitcoinRPC):
        self.__client: BitcoinRPC = rpc_client

    """
    Get wallet info:
      - Addresses with data(amount, confirmations, etc)
    """
    async def get_wallet_info(self) -> List[dict] | None:
        try:
            return await BitcoinWallet(self.__client).list_received_by_address()
        except RPCError as e:
            msg = f"RPC error: {e}"
            logging.error(msg)
            self._is_wallet_not_exist_error(e)
            raise

    """
        Get wallet balance:
    """
    async def get_wallet_balance(self) -> Decimal:
        try:
            return await BitcoinWallet(self.__client).get_wallet_balance()
        except RPCError as e:
            msg = f"RPC error: {e}"
            logging.error(msg)
            self._is_wallet_not_exist_error(e)
            raise

    """
       Create wallet
    """
    async def create_wallet(self, wallet_name: str) -> str:
        try:
            wallet = await BitcoinWallet(self.__client).create_wallet(wallet_name)
            return wallet["name"]
        except RPCError as e:
            msg = f"RPC error: {e}"
            logging.error(msg)
            if str(e.error).find("Database already exists") != -1:
                exp_msg = f"'{wallet_name}' wallet already exists. Try using load wallet API"
                raise HTTPException(409, exp_msg)
            raise

    """
        Load wallet
    """
    async def load_wallet(self, wallet_name: str) -> str:
        try:
            wallet = await BitcoinWallet(self.__client).load_wallet(wallet_name)
            return wallet["name"]
        except RPCError as e:
            msg = f"RPC error: {e}"
            logging.error(msg)
            if str(e.error).find("Path does not exist") != -1:
                exp_msg = f"'{wallet_name}' wallet has not yet been created. Try using create wallet API"
                raise HTTPException(409, exp_msg)
            raise

    """
        Create new address for wallet
    """
    async def create_new_address(self) -> str:
        try:
            return await BitcoinWallet(self.__client).create_new_address()
        except RPCError as e:
            msg = f"RPC error: {e}"
            logging.error(msg)
            self._is_wallet_not_exist_error(e)
            raise

    @staticmethod
    def _is_wallet_not_exist_error(rpc_error: RPCError) -> None:
        if str(rpc_error.error).find("Requested wallet does not exist or is not loaded") != -1:
            exp_msg = f"Wallet does not exist. Try using create or load wallet API"
            raise HTTPException(404, exp_msg)
