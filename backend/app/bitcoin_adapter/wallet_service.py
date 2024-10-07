from bitcoinrpc import BitcoinRPC, RPCError

"""
CRUD of bitcoin wallet
"""


class BitcoinWalletService:
    def __init__(self, rpc_client: BitcoinRPC):
        self.__client: BitcoinRPC = rpc_client

    """
    Get wallet info:
      - Addresses with data(amount, confirmations, etc)
    """
    async def get_wallet_info(self) -> list | None:
        try:
            addresses = await self.__client.acall("listreceivedbyaddress", [0, True])
            return list(addresses)
        except RPCError as e:
            print(f"RPC error: {e}")
            if e.error == "Requested wallet does not exist or is not loaded":
                return None
        except Exception as e:
            print(f"Connection error: {e}")
            raise
