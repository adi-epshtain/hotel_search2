import httpx
from backend.app.core.config import settings


class BoomNowClient:
    """Handles integration with BoomNow API."""

    async def healthcheck(self):
        url = f"{settings.BOOMNOW_BASE_URL}/open_api/v1/status"

        async with httpx.AsyncClient(timeout=10) as client:
            resp = await client.get(url)
            return {"status": resp.status_code, "text": resp.text}

    async def search_hotels(self, city: str, adults: int):
        headers = {
            "Accept": "application/json",
            "Authorization": f"Bearer {settings.BOOMNOW_API_TOKEN}"
        }

        async with httpx.AsyncClient(timeout=15) as client:
            resp = await client.get(
                f"{settings.BOOMNOW_BASE_URL}/open_api/v1/listings",
                headers=headers,
                params={"city": city, "adults": adults} if city or adults else None
            )
            resp.raise_for_status()
            
            # Try to parse JSON
            try:
                return resp.json()
            except Exception as e:
                print(f"Error parsing JSON response: {e}")
                print(f"Response status: {resp.status_code}")
                print(f"Response text: {resp.text[:500]}")
                raise

    async def get_cities(self):
        headers = {
            "Accept": "application/json",
            "Authorization": f"Bearer {settings.BOOMNOW_API_TOKEN}"
        }

        async with httpx.AsyncClient(timeout=10) as client:
            resp = await client.get(
                f"{settings.BOOMNOW_BASE_URL}/open_api/v1/listings/cities",
                headers=headers
            )
            resp.raise_for_status()
            return resp.json()
