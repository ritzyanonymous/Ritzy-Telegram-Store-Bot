from pydantic import BaseModel
import os
from dotenv import load_dotenv

load_dotenv()

def get_admin_id() -> int:
    admin_id = int(os.getenv("ADMIN_ID", "0"))
    if admin_id == 0:
        raise ValueError("ADMIN_ID not set in .env file. Please set your Telegram user ID.")
    if admin_id == 1014293448:
        raise ValueError("SECURITY WARNING: Example ADMIN_ID detected. Change ADMIN_ID in .env to your real Telegram user ID.")
    return admin_id

class Settings(BaseModel):
    TELEGRAM_BOT_TOKEN: str = os.getenv("TELEGRAM_BOT_TOKEN", "")
    ADMIN_ID: int = get_admin_id()
    SUPPORT_USERNAME: str = os.getenv("SUPPORT_USERNAME", "YourAdminUsername")
    MONGO_URI: str = os.getenv("MONGO_URI", "mongodb://localhost:27017")
    MONGO_DB: str = os.getenv("MONGO_DB", "ritzy_store")
    PUBLIC_BASE_URL: str = os.getenv("PUBLIC_BASE_URL", "http://localhost:8000")
    BTCPAY_HOST: str = os.getenv("BTCPAY_HOST", "")
    BTCPAY_API_KEY: str = os.getenv("BTCPAY_API_KEY", "")
    BTCPAY_STORE_ID: str = os.getenv("BTCPAY_STORE_ID", "")
    BTCPAY_WEBHOOK_SECRET: str = os.getenv("BTCPAY_WEBHOOK_SECRET", "")

settings = Settings()
