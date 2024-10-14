from decimal import Decimal
from typing import List

from bitcoinrpc import BitcoinRPC

"""
    bitcoin-cli chain query for bitcoin wallet
"""


class BitcoinWallet:
    def __init__(self, rpc_client: BitcoinRPC):
        self.__client: BitcoinRPC = rpc_client

    """
        The listreceivedbyaddress RPC lists balances by receiving address.
        https://chainquery.com/bitcoin-cli/listreceivedbyaddress
    """
    async def list_received_by_address(self, min_conf=0, include_empty=True) -> List[dict] | None:
        return await self.__client.acall("listreceivedbyaddress", [min_conf, include_empty])

    """
        The getbalance RPC returns the total available balance.
        https://chainquery.com/bitcoin-cli/getbalance
    """
    async def get_wallet_balance(self) -> Decimal:
        balance = await self.__client.acall("getbalance", [])
        return Decimal(balance)

    """
       The createwallet RPC creates and loads a new wallet.
       https://chainquery.com/bitcoin-cli/createwallet
    """
    async def create_wallet(self, wallet_name: str) -> dict:
        return await self.__client.acall("createwallet", [wallet_name])

    """
        The loadwallet RPC loads a wallet from a wallet file or directory.
        https://chainquery.com/bitcoin-cli/loadwallet
    """
    async def load_wallet(self, wallet_name: str) -> dict:
        return await self.__client.acall("loadwallet", [wallet_name])

    """
        The getnewaddress RPC returns a new Bitcoin address for receiving payments.
        If an account is specified, payments received with the address will be credited to that account.
        https://chainquery.com/bitcoin-cli/getnewaddress
    """
    async def create_new_address(self) -> str:
        return await self.__client.acall("getnewaddress", [])
