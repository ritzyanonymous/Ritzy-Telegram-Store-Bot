from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase
from bot.config import settings

client = AsyncIOMotorClient(settings.MONGO_URI)
db: AsyncIOMotorDatabase = client[settings.MONGO_DB]

# Collections
users = db.get_collection("users")
categories = db.get_collection("categories")
products = db.get_collection("products")
orders = db.get_collection("orders")
transactions = db.get_collection("transactions")  # deposits & withdrawals
invoices = db.get_collection("invoices")          # btcpay invoices for top-ups

async def ensure_indexes():
    await users.create_index("telegram_id", unique=True)
    await products.create_index("category")
    await invoices.create_index("invoice_id", unique=True)
