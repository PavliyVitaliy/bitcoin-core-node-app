from decimal import Decimal
from typing import List
from bitcoinrpc import BitcoinRPC


class BitcoinWallet:
    """
    Class representing a bitcoin-cli chain query for bitcoin wallet
    :param rpc_client: rpc client of the Bitcoin node.
    """

    def __init__(self, rpc_client: BitcoinRPC):
        self.__client: BitcoinRPC = rpc_client

    async def list_received_by_address(self, min_conf=0, include_empty=True) -> List[dict] | None:
        """
        The listreceivedbyaddress RPC lists balances by receiving address.
        https://chainquery.com/bitcoin-cli/listreceivedbyaddress
        :param min_conf: The minimum number of confirmations before payments are included
        :param include_empty: Whether to include addresses that haven't received any payments
        """

        return await self.__client.acall("listreceivedbyaddress", [min_conf, include_empty])

    async def get_wallet_balance(self) -> Decimal:
        """
        The getbalance RPC returns the total available balance.
        https://chainquery.com/bitcoin-cli/getbalance
        """

        balance = await self.__client.acall("getbalance", [])
        return Decimal(balance)

    async def create_wallet(self, wallet_name: str) -> dict:
        """
        The createwallet RPC creates and loads a new wallet.
        https://chainquery.com/bitcoin-cli/createwallet
        :param wallet_name: The name for the new wallet.
            If this is a path, the wallet will be created at the path location
        """

        return await self.__client.acall("createwallet", [wallet_name])

    async def load_wallet(self, wallet_name: str) -> dict:
        """
        The loadwallet RPC loads a wallet from a wallet file or directory.
        https://chainquery.com/bitcoin-cli/loadwallet
        :param wallet_name: The wallet directory or .dat file
        """

        return await self.__client.acall("loadwallet", [wallet_name])

    async def create_new_address(self) -> str:
        """
        The getnewaddress RPC returns a new Bitcoin address for receiving payments.
        If an account is specified, payments received with the address will be credited to that account.
        https://chainquery.com/bitcoin-cli/getnewaddress
        """

        return await self.__client.acall("getnewaddress", [])
