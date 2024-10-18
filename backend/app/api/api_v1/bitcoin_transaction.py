from fastapi import APIRouter, Depends
from sqlalchemy import select
from sqlalchemy.engine import Result
from sqlalchemy.ext.asyncio import AsyncSession
from bitcoin_adapter.rpc_helper import get_bitcoin_rpc_client
from core.config import settings
from core.models import db_helper, Transaction
from core.schemas.transaction import TransactionSchema
from core.services.transaction_service import TransactionService

router = APIRouter(
    prefix=settings.api.v1.bitcoin_transaction,
    tags=["Bitcoin Transaction"],
)


@router.post("/test", response_model=dict, status_code=201)
async def create_transaction(
        post_data: TransactionSchema,
        session: AsyncSession = Depends(db_helper.session_getter),
) -> dict:
    network = settings.bitcoin_node.network
    path = f"/wallet/{post_data.wallet_name}"
    rpc_client = get_bitcoin_rpc_client(path)
    info = await TransactionService(rpc_client).create_and_broadcast_regtest_transaction(
        session,
        post_data.from_address,
        post_data.to_address,
        post_data.amount,
    )
    return {
        "network": network,
        "wallet_name": post_data.wallet_name,
        "transaction_data": info,
    }


@router.get("/all")
async def get_transactions(session: AsyncSession = Depends(db_helper.session_getter)):
    stmt = select(Transaction).order_by(Transaction.id)
    result: Result = await session.execute(stmt)
    transactions = result.scalars().all()
    return list(transactions)
