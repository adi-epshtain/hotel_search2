from fastapi import APIRouter
from backend.app.services.boomnow_client import BoomNowClient

router = APIRouter()
client = BoomNowClient()


@router.get("/health")
async def boomnow_health():
    return await client.healthcheck()
