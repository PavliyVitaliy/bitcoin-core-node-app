from bitcoin_adapter.utils import calculate_total_btc
from bitcoinrpc import BitcoinRPC, RPCError

"""
Retrieve bitcoin blockchain information
"""


class BitcoinInfoService:
    def __init__(self, rpc_client: BitcoinRPC):
        self.__client: BitcoinRPC = rpc_client

    """
    Get info for current block height:
      - Current block height
      - Hash of the latest block
      - Number of transactions in the latest block
      - Total amount of Bitcoin currently in circulation
    """
    async def get_current_block_info(self) -> dict:
        try:
            block_height = await self.__client.getblockcount()
            latest_block_hash = await self.__client.getblockhash(block_height)
            latest_block = await self.__client.getblock(latest_block_hash)
            num_transactions = len(latest_block['tx'])

            return {
                "block_height": block_height,
                "latest_block_hash": latest_block_hash,
                "transactions_number": num_transactions,
                "total_amount_circulation": calculate_total_btc(block_height),
            }
        except RPCError as e:
            print(f"RPC error: {e}")
        except Exception as e:
            print(f"Connection error: {e}")
            raise
