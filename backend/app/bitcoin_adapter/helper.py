from typing import List
from bitcoinrpc import BitcoinRPC

"""
    bitcoin-cli chain query helper
"""


class BitcoinHelper:
    def __init__(self, rpc_client: BitcoinRPC):
        self.__client: BitcoinRPC = rpc_client

    """
        The generatetoaddress RPC mines to a specified address and returns the block hashes.
        https://chainquery.com/bitcoin-cli/generatetoaddress
    """
    async def generate_to_address(self, address: str, blocks: int = 1) -> List[str] | None:
        return await self.__client.acall("generatetoaddress", [blocks, address])
