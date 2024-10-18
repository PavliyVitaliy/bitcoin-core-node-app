from bitcoin_adapter.utils import calculate_total_btc
from bitcoinrpc import BitcoinRPC, RPCError
from core.schemas.info import BlockchainInfoSchema

import logging

logging.basicConfig()
logging.getLogger("BitcoinRPC").setLevel(logging.DEBUG)


class InfoService:
    """
    Class representing an Info Service for retrieve bitcoin blockchain information
    :param rpc_client: rpc client of the Bitcoin node.
    """

    def __init__(self, rpc_client: BitcoinRPC):
        self.__client: BitcoinRPC = rpc_client

    async def get_current_block_info(self) -> BlockchainInfoSchema:
        """
        Get info for current block height:
            - Current block height
            - Hash of the latest block
            - Number of transactions in the latest block
            - Total amount of Bitcoin currently in circulation
        """

        try:
            block_height = await self.__client.getblockcount()
            latest_block_hash = await self.__client.getblockhash(block_height)
            latest_block = await self.__client.getblock(latest_block_hash)
            num_transactions = len(latest_block['tx'])

            return BlockchainInfoSchema(
                block_height=block_height,
                latest_block_hash=latest_block_hash,
                transactions_number=num_transactions,
                total_amount_circulation=calculate_total_btc(block_height)
            )
        except RPCError as e:
            msg = f"RPC error: {e}"
            logging.error(msg)
            raise
