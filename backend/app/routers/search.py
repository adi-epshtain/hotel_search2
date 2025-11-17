from fastapi import APIRouter, Query, HTTPException
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
    try:
        result = await client.search_hotels(city, adults)
        return result
    except Exception as e:
        print(f"Error in search_hotels: {e}")
        raise HTTPException(status_code=500, detail=f"Error fetching hotels: {str(e)}")


@router.get("/cities")
async def list_cities():
    return await client.get_cities()