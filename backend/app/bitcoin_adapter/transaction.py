from decimal import Decimal
from typing import List
from bitcoinrpc import BitcoinRPC

"""
    bitcoin-cli chain query for bitcoin transaction
"""


class BitcoinTransaction:
    def __init__(self, rpc_client: BitcoinRPC):
        self.__client: BitcoinRPC = rpc_client

    """
        The listunspent RPC returns array of unspent transaction outputs 
        with between minconf and maxconf (inclusive) confirmations. 
        Optionally filter to only include txouts paid to specified addresses.
        https://chainquery.com/bitcoin-cli/listunspent
    """
    async def list_unspent(
            self,
            from_address: str,
            min_conf=0,
            max_conf: int = 9999999
    ) -> List[dict] | None:
        unspent_txs = await self.__client.acall(
            "listunspent",
            [min_conf, max_conf, [from_address]]
        )
        return unspent_txs

    """
        The createrawtransaction RPC creates a transaction spending the given inputs and creating new outputs.
        Outputs can be addresses or data. Returns hex-encoded raw transaction.
        Note that the transaction's inputs are not signed, 
        and it is not stored in the wallet or transmitted to the network.
        https://chainquery.com/bitcoin-cli/createrawtransaction
    """
    async def create_raw_transaction(self, inputs: List[dict], outputs: dict) -> str | None:
        hex_raw_tx = await self.__client.acall("createrawtransaction", [inputs, outputs])
        return str(hex_raw_tx)

    """
        The signrawtransactionwithwallet RPC signs inputs for raw transaction (serialized, hex-encoded)
        https://chainquery.com/bitcoin-cli/signrawtransactionwithwallet
    """
    async def sign_raw_transaction(self, hex_raw_tx: str) -> dict | None:
        signed_tx = await self.__client.acall("signrawtransactionwithwallet", [hex_raw_tx])
        return signed_tx

    """
        The sendrawtransaction RPC submits a raw transaction (serialized, hex-encoded) to local node and network.
        https://chainquery.com/bitcoin-cli/sendrawtransaction
    """
    async def send_raw_transaction(self, hex_str: str, max_fee_rate: Decimal = 0) -> str | None:
        tx_id = await self.__client.acall("sendrawtransaction", [hex_str, max_fee_rate])
        return str(tx_id)

    """
        The gettransaction RPC gets detailed information about an in-wallet transaction.
        https://chainquery.com/bitcoin-cli/gettransaction
    """
    async def get_transaction(self, tx_id: str) -> dict | None:
        info = await self.__client.acall("gettransaction", [tx_id])
        return info
