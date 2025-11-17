import os
from dotenv import load_dotenv

load_dotenv()


class Settings:
    BOOMNOW_BASE_URL: str = os.getenv("BOOMNOW_BASE_URL", "https://api.boomnow.com")
    BOOMNOW_API_TOKEN: str = os.getenv("BOOMNOW_API_TOKEN")
    BOOMNOW_API_KEY: str = os.getenv("BOOMNOW_API_KEY", "")
    BOOMNOW_CLIENT_ID: str = os.getenv("BOOMNOW_CLIENT_ID")
    BOOMNOW_CLIENT_SECRET: str = os.getenv("BOOMNOW_CLIENT_SECRET")


settings = Settings()
