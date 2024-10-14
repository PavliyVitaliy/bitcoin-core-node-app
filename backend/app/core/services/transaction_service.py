import datetime
from decimal import Decimal
from typing import List
from fastapi import HTTPException
from bitcoinrpc import BitcoinRPC, RPCError
from bitcoin_adapter.transaction import BitcoinTransaction
from sqlalchemy.ext.asyncio import AsyncSession
from core.models import Transaction
from core.services.helper_service import HelperService

import logging
logging.basicConfig()
logging.getLogger("BitcoinRPC").setLevel(logging.DEBUG)

"""
CRUD of bitcoin transactions
"""


class TransactionService:
    def __init__(self, rpc_client: BitcoinRPC):
        self.__client: BitcoinRPC = rpc_client

    """
        Create and broadcast transaction for test transaction using regtest only
    """
    async def create_and_broadcast_regtest_transaction(
            self,
            session: AsyncSession,
            from_address: str,
            to_address: str,
            amount: Decimal
    ) -> dict:
        try:
            # Step 1: You should already have enough funds to transfer between addresses.
            # For the first generation of funds in the regtest node, you can use API for generation(101 blocks).

            # Step 2: List unspent transactions for the from_address
            unspent_txs = await self.get_unspent_transactions_outputs(from_address)
            target_unspent_txs = self.find_unspent_list_for_target_amount(unspent_txs, amount)
            if len(target_unspent_txs) == 0:
                msg = f"Not enough funds available in the '{from_address}' address."
                logging.error(msg)
                raise HTTPException(422, msg)

            # Step 3: Create a raw transaction
            hex_raw_tx = await self.create_raw_transaction(target_unspent_txs, to_address, float(amount))

            # Step 4: Sign the raw transaction
            signed_tx = await self.sign_raw_transaction(hex_raw_tx)

            # Step 5: Broadcast the transaction
            tx_id = await self.send_raw_transaction(signed_tx["hex"])

            # Step 6: Confirm by generating a block
            await HelperService(self.__client).generate_blocks(from_address, 1)

            # Step 7: Verify the transaction
            transaction = await self.get_transaction(tx_id)
            vout = transaction["details"][0]["vout"]
            timestamp = datetime.datetime.fromtimestamp(transaction["time"])
            transaction_db = Transaction(
                tx_id=tx_id,
                input_address=from_address,
                output_address=to_address,
                amount=amount,
                timestamp=timestamp,
                vouts=vout
            )
            session.add(transaction_db)
            await session.commit()
            return transaction
        except RPCError as e:
            msg = f"RPC error: {e}"
            logging.error(msg)
            raise

    """
        Get list of unspent transaction outputs
    """
    async def get_unspent_transactions_outputs(self, from_address: str) -> List[dict]:
        unspent_txs = await BitcoinTransaction(self.__client).list_unspent(from_address)
        if not unspent_txs:
            msg = f"No funds available in the '{from_address}' address."
            logging.error(msg)
            raise HTTPException(422, msg)
        return unspent_txs

    """
        Create a transaction spending the given inputs and creating new outputs.
    """
    async def create_raw_transaction(
            self,
            unspent_txs: List[dict],
            to_address: str,
            amount: float,
    ) -> str:
        inputs = [{"txid": unspent['txid'], "vout": unspent['vout']} for unspent in unspent_txs]
        outputs = {to_address: amount}
        hex_raw_tx = await BitcoinTransaction(self.__client).create_raw_transaction(inputs, outputs)

        if not hex_raw_tx:
            msg = f"Hex-encoded raw transaction transaction not created for inputs ({inputs}) and outputs ({outputs})"
            logging.error(msg)
            raise HTTPException(422, msg)
        logging.info(f"Transaction successfully created. Transaction: {hex_raw_tx}")
        return hex_raw_tx

    """
       Sign inputs for raw transaction
    """
    async def sign_raw_transaction(self, hex_raw_tx: str) -> dict:
        signed_tx = await BitcoinTransaction(self.__client).sign_raw_transaction(hex_raw_tx)
        if not signed_tx.get("complete"):
            msg = "Transaction signing failed."
            logging.error(msg)
            raise HTTPException(422, msg)
        logging.info(f"Transaction successfully sign. Transaction hex: {signed_tx.get("hex")}")
        return signed_tx

    """
        Submits a raw transaction
    """
    async def send_raw_transaction(self, hex_str: str) -> str:
        try:
            tx_id = await BitcoinTransaction(self.__client).send_raw_transaction(hex_str)
            if not tx_id:
                msg = f"Transaction sending failed for hex '{hex_str}'."
                logging.error(msg)
                raise HTTPException(422, msg)
            logging.info(f"Transaction successfully broadcast. Transaction ID: {tx_id}")
            return tx_id
        except RPCError as e:
            self._is_fee_not_enough_error(e)
            raise

    """
        Get detailed information about an in-wallet transaction.
    """
    async def get_transaction(self, tx_id: str) -> dict:
        info = await BitcoinTransaction(self.__client).get_transaction(tx_id)
        if not info:
            msg = f"Can not find transaction for tx_id '{tx_id}'."
            logging.error(msg)
            raise HTTPException(422, msg)
        return info

    @staticmethod
    def find_unspent_list_for_target_amount(
            unspent_list: List[dict],
            target_amount: Decimal
    ) -> List[dict]:
        # Sort transactions in descending order for a greedy approach
        sorted_unspent_list = sorted(
            unspent_list,
            key=lambda x: x['amount'],
            reverse=True
        )
        current_sum = Decimal(0.0)
        selected_unspents = []

        for item in sorted_unspent_list:
            if current_sum >= target_amount:
                break
            current_sum += Decimal(item['amount'])
            selected_unspents.append(item)

        # Check if we reached or exceeded the target
        if current_sum >= target_amount:
            return selected_unspents
        else:
            return []  # No possible combination found

    @staticmethod
    def _is_fee_not_enough_error(rpc_error: RPCError) -> None:
        if str(rpc_error.error).find("min relay fee not met") != -1:
            exp_msg = f"Fee is not enough. Try changing the amount for the transaction"
            raise HTTPException(404, exp_msg)
