from bitcoinrpc import BitcoinRPC
from core.config import settings


def get_bitcoin_rpc_client(path=""):
    url = f"http://{settings.bitcoin_node.rpc_host}:{settings.bitcoin_node.rpc_port}{path}"
    user_name = settings.bitcoin_node.rpc_user
    user_password = settings.bitcoin_node.rpc_password
    rpc_client = BitcoinRPC.from_config(url, (user_name, user_password))
    return rpc_client
