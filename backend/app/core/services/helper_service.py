from typing import List
from fastapi import HTTPException
from bitcoinrpc import BitcoinRPC
from bitcoin_adapter.helper import BitcoinHelper

import logging
logging.basicConfig()
logging.getLogger("BitcoinRPC").setLevel(logging.DEBUG)


class HelperService:
    """
    Class representing a Helper Service
    :param rpc_client: rpc client of the Bitcoin node.
    """

    def __init__(self, rpc_client: BitcoinRPC):
        self.__client: BitcoinRPC = rpc_client

    async def generate_blocks(self, address: str, blocks: int = 1) -> List[str]:
        """
        Mines to a specified address and returns the block hashes.
        Uses for regtest node
        """

        mined_blocks = await BitcoinHelper(self.__client).generate_to_address(address, blocks)
        if not mined_blocks:
            msg = f"Blocks generation failed for address: {address}"
            logging.error(msg)
            raise HTTPException(422, msg)
        logging.info(f"Blocks successfully generated for address: {address}")
        return mined_blocks
