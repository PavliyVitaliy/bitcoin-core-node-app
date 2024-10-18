from typing import List
from bitcoinrpc import BitcoinRPC


class BitcoinHelper:
    """
    Class representing a bitcoin-cli chain query helper
    :param rpc_client: rpc client of the Bitcoin node.
    """

    def __init__(self, rpc_client: BitcoinRPC):
        self.__client: BitcoinRPC = rpc_client

    async def generate_to_address(self, address: str, blocks: int = 1) -> List[str] | None:
        """
        The generatetoaddress RPC mines to a specified address and returns the block hashes.
        https://chainquery.com/bitcoin-cli/generatetoaddress
        :param address: The address to send the newly generated bitcoin to
        :param blocks: How many blocks are generated
        """

        return await self.__client.acall("generatetoaddress", [blocks, address])
