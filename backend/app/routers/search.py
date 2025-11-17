from fastapi import APIRouter, Query
from backend.app.services.boomnow_client import BoomNowClient

router = APIRouter()
client = BoomNowClient()


@router.get("/")
async def search_hotels(
    city: str = Query(...),
    adults: int = Query(..., ge=1)
):
    """
    Search hotels via BoomNow.
    Returns raw JSON from BoomNow API.
    """
    return await client.search_hotels(city, adults)
