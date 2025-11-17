import httpx
from backend.app.core.config import settings
from backend.app.services.auth_service import auth_client


class BoomNowClient:
    """Handles integration with BoomNow API."""

    async def healthcheck(self):
        url = f"{settings.BOOMNOW_BASE_URL}/open_api/v1/status"

        async with httpx.AsyncClient(timeout=10) as client:
            resp = await client.get(url)
            return {"status": resp.status_code, "text": resp.text}

    async def search_hotels(self, city: str, adults: int):
        token = await auth_client.get_token()

        headers = {
            "Authorization": f"Bearer {token}"
        }

        params = {"city": city, "adults": adults}

        async with httpx.AsyncClient(timeout=10) as client:
            resp = await client.get(
                f"{settings.BOOMNOW_BASE_URL}/open_api/v1/search",
                params=params,
                headers=headers,
            )
            resp.raise_for_status()
            return resp.json()