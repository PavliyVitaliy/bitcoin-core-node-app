from decimal import Decimal
from typing import List
from bitcoinrpc import BitcoinRPC


class BitcoinTransaction:
    """
    Class representing a bitcoin-cli chain query for bitcoin transaction
    :param rpc_client: rpc client of the Bitcoin node.
    """

    def __init__(self, rpc_client: BitcoinRPC):
        self.__client: BitcoinRPC = rpc_client

    async def list_unspent(
            self,
            from_address: str,
            min_conf=0,
            max_conf: int = 9999999
    ) -> List[dict] | None:
        """
        The listunspent RPC returns array of unspent transaction outputs
        with between minconf and maxconf (inclusive) confirmations.
        Optionally filter to only include txouts paid to specified addresses.
        https://chainquery.com/bitcoin-cli/listunspent
        :param from_address: Bitcoin address
        :param min_conf: The minimum confirmations to filter
        :param max_conf: The maximum confirmations to filter
        """

        unspent_txs = await self.__client.acall(
            "listunspent",
            [min_conf, max_conf, [from_address]]
        )
        return unspent_txs

    async def create_raw_transaction(self, inputs: List[dict], outputs: dict) -> str | None:
        """
        The createrawtransaction RPC creates a transaction spending the given inputs and creating new outputs.
        Outputs can be addresses or data. Returns hex-encoded raw transaction.
        Note that the transaction's inputs are not signed,
        and it is not stored in the wallet or transmitted to the network.
        https://chainquery.com/bitcoin-cli/createrawtransaction
        :param inputs: The inputs
        :param outputs: The outputs (key-value pairs), where none of the keys are duplicated.
        """

        hex_raw_tx = await self.__client.acall("createrawtransaction", [inputs, outputs])
        return str(hex_raw_tx)

    async def sign_raw_transaction(self, hex_raw_tx: str) -> dict | None:
        """
        The signrawtransactionwithwallet RPC signs inputs for raw transaction (serialized, hex-encoded)
        https://chainquery.com/bitcoin-cli/signrawtransactionwithwallet
        :param hex_raw_tx: The transaction hex string
        """

        signed_tx = await self.__client.acall("signrawtransactionwithwallet", [hex_raw_tx])
        return signed_tx

    async def send_raw_transaction(self, hex_str: str, max_fee_rate: Decimal = 0) -> str | None:
        """
        The sendrawtransaction RPC submits a raw transaction (serialized, hex-encoded) to local node and network.
        https://chainquery.com/bitcoin-cli/sendrawtransaction
        :param hex_str: The hex string of the raw transaction
        :param max_fee_rate: Reject transactions whose fee rate is higher than the specified value,
            expressed in BTC/kvB. Set to 0 to accept any fee rate
        """

        tx_id = await self.__client.acall("sendrawtransaction", [hex_str, max_fee_rate])
        return str(tx_id)

    async def get_transaction(self, tx_id: str) -> dict | None:
        """
        The gettransaction RPC gets detailed information about an in-wallet transaction.
        https://chainquery.com/bitcoin-cli/gettransaction
        :param tx_id: The transaction id
        """

        info = await self.__client.acall("gettransaction", [tx_id])
        return info
