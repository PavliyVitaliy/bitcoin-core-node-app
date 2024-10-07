from pydantic import BaseModel
from pydantic import PostgresDsn
from pydantic_settings import (
    BaseSettings,
    SettingsConfigDict,
)

from utils import get_env_file


class RunConfig(BaseModel):
    host: str = "0.0.0.0"
    port: int = 8000


class ApiV1Prefix(BaseModel):
    prefix: str = "/v1"
    bitcoin_info: str = "/info"
    bitcoin_wallet: str = "/wallet"


class ApiPrefix(BaseModel):
    prefix: str = "/api"
    v1: ApiV1Prefix = ApiV1Prefix()


class PostgresConfig(BaseModel):
    url: PostgresDsn
    echo: bool = False
    echo_pool: bool = False
    pool_size: int = 50
    max_overflow: int = 10

    naming_convention: dict[str, str] = {
        "ix": "ix_%(column_0_label)s",
        "uq": "uq_%(table_name)s_%(column_0_N_name)s",
        "ck": "ck_%(table_name)s_%(constraint_name)s",
        "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
        "pk": "pk_%(table_name)s",
    }


class BitcoinNode(BaseModel):
    network: str
    rpc_user: str
    rpc_password: str
    rpc_host: str
    rpc_port: int


class Settings(BaseSettings):
    current_env_file: str = get_env_file()
    model_config = SettingsConfigDict(
        env_file=(".env.template", current_env_file),
        case_sensitive=False,
        env_nested_delimiter="__",
        env_prefix="APP_CONFIG__",
        extra="allow",
    )
    run: RunConfig = RunConfig()
    api: ApiPrefix = ApiPrefix()
    db: PostgresConfig
    bitcoin_node: BitcoinNode


settings = Settings()
