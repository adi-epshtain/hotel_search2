import httpx
import time

from app.core.config import settings


class BoomNowAuth:
    _token = None
    _expires_at = 0

    async def get_token(self):
        """Return existing token if valid, otherwise request a new one."""

        now = time.time()

        # אם הטוקן עדיין בתוקף
        if self._token and now < self._expires_at:
            return self._token

        async with httpx.AsyncClient(timeout=10) as client:
            resp = await client.post(
                f"{settings.BOOMNOW_BASE_URL}/open_api/v1/auth/token",
                json={
                    "client_id": settings.BOOMNOW_CLIENT_ID,
                    "client_secret": settings.BOOMNOW_CLIENT_SECRET
                }
            )

            print("AUTH STATUS:", resp.status_code)
            print("AUTH TEXT:", resp.text)

            if resp.status_code == 201:
                data = resp.json()
                token = data.get("access_token")
                expires_in = data.get("expires_in", 3600)

                self._token = token
                self._expires_at = now + expires_in - 20  # margin
                return self._token

            elif resp.status_code == 403:
                raise Exception("BoomNow Auth failed: 403 Forbidden")

            else:
                raise Exception(
                    f"Unexpected auth response: {resp.status_code}")


auth_client = BoomNowAuth()
