from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase
from bot.config import settings

client = AsyncIOMotorClient(settings.MONGO_URI)
_db: AsyncIOMotorDatabase = client[settings.MONGO_DB]

class Database:
    def __init__(self, client, db):
        self.client = client
        self.db = db

db_instance = Database(client, _db)

users = db_instance.db.get_collection("users")
categories = db_instance.db.get_collection("categories")
products = db_instance.db.get_collection("products")
orders = db_instance.db.get_collection("orders")
transactions = db_instance.db.get_collection("transactions")
invoices = db_instance.db.get_collection("invoices")

async def ensure_indexes():
    await users.create_index("telegram_id", unique=True)
    await products.create_index("category")
    await invoices.create_index("invoice_id", unique=True)
