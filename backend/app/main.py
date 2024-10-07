from contextlib import asynccontextmanager
from fastapi import FastAPI

from api import router as api_router
from core.models import db_helper


@asynccontextmanager
async def lifespan(app: FastAPI):
    # startup
    yield
    # shutdown
    await db_helper.dispose()


app = FastAPI(
    lifespan=lifespan,
)
app.include_router(
    api_router,
)


@app.get("/ping")
async def ping() -> dict:
    return {"Success": True}
