from decimal import Decimal
from fastapi import HTTPException
from bitcoinrpc import BitcoinRPC, RPCError
from bitcoin_adapter.utility import BitcoinUtility

import logging

logging.basicConfig()
logging.getLogger("BitcoinRPC").setLevel(logging.DEBUG)


class FeeService:
    """
    Class representing a Fee Service for CRUD of bitcoin transaction fee
    :param rpc_client: rpc client of the Bitcoin node.
    """

    def __init__(self, rpc_client: BitcoinRPC):
        self.__client: BitcoinRPC = rpc_client

    async def get_approximate_fee(self) -> Decimal:
        """
        Get approximate fee per kilobyte for a transaction
        """

        try:
            fee = await BitcoinUtility(self.__client).estimate_smart_fee()
            if fee is None or fee.get("feerate", None) is None:
                msg = f"Can not estimate approximate fee."
                logging.error(msg)
                raise HTTPException(404, msg)
            return Decimal(fee["feerate"])
        except RPCError as e:
            msg = f"RPC error: {e}"
            logging.error(msg)
            raise
