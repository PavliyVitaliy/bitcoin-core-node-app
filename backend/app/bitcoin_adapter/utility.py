from bitcoinrpc import BitcoinRPC


class BitcoinUtility:
    """
    Class representing a bitcoin-cli chain query for bitcoin utility
    :param rpc_client: rpc client of the Bitcoin node.
    """

    def __init__(self, rpc_client: BitcoinRPC):
        self.__client: BitcoinRPC = rpc_client

    async def estimate_smart_fee(
            self,
            conf_target: int = 1,
            estimate_mode: str = "conservative"
    ) -> dict | None:
        """
        The estimatesmartfee RPC estimates the approximate fee per kilobyte
        needed for a transaction to begin confirmation within conf_target blocks
        if possible and return the number of blocks for which the estimate is valid.
        https://chainquery.com/bitcoin-cli/estimatesmartfee
        :param conf_target: Confirmation target in blocks (1 - 1008)
        :param estimate_mode: The fee estimate mode.
                    Whether to return a more conservative estimate which also satisfies
                    a longer history. A conservative estimate potentially returns a
                    higher fee rate and is more likely to be sufficient for the desired
                    target, but is not as responsive to short term drops in the
                    prevailing fee market. Must be one of (case-insensitive):
                    "unset" / "economical" / "conservative"
        """

        return await self.__client.acall("estimatesmartfee", [conf_target, estimate_mode])
