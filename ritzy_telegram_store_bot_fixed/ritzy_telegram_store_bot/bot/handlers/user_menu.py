from aiogram import Router, F
from aiogram.types import Message
from bot.keyboards import main_menu_kb, support_kb
from database.mongo import users
from utils.formatting import format_profile
from bot.config import settings

router = Router()

@router.message(F.text == "/start")
async def start_cmd(msg: Message):
    await users.update_one(
        {"telegram_id": msg.from_user.id},
        {"$setOnInsert": {"telegram_id": msg.from_user.id, "username": msg.from_user.username, "balance_usd": 0.0}},
        upsert=True
    )
    await msg.answer("Welcome to Ritzy Store 🏬\nPlease choose an option below 👇", reply_markup=main_menu_kb())

@router.message(F.text == "MyID 👤")
async def myid(msg: Message):
    u = await users.find_one({"telegram_id": msg.from_user.id}) or {}
    text = format_profile(
        telegram_id=msg.from_user.id,
        username=msg.from_user.username,
        email=u.get("email"),
        balance=u.get("balance_usd", 0.0)
    )
    await msg.answer(text)

@router.message(F.text == "Rules / Manual 📜")
async def rules(msg: Message):
    await msg.answer("📜 Store Rules & Manual\n\n(Coming Soon…)")

@router.message(F.text == "Support ✋🏻")
async def support(msg: Message):
    await msg.answer(
        "💬💬💬 Support Team 💬💬💬\n"
        f"🌐 Website: https://example.com\n\n"
        "❓ If you need any help with the bot, click the button below to chat with our Support Team:\n\n"
        "⛑️ We're here to assist you anytime ⛑️",
        reply_markup=support_kb(settings.SUPPORT_USERNAME)
    )
