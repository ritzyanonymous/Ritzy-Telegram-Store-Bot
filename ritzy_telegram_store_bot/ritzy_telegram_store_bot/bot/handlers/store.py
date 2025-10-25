from aiogram import Router, F
from aiogram.types import Message, CallbackQuery, InputMediaPhoto
from bot.keyboards import categories_kb, products_kb, product_actions_kb
from database.mongo import categories, products, users, orders
from datetime import datetime
import uuid

router = Router()

@router.message(F.text == "Store 🛍️")
async def store_entry(msg: Message):
    cats = [c async for c in categories.find({}, {"_id": 0})]
    await msg.answer("🛒 Product Categories:", reply_markup=categories_kb(cats))

@router.callback_query(F.data.startswith("cat:"))
async def open_category(cb: CallbackQuery):
    name = cb.data.split(":", 1)[1]
    prods = [p async for p in products.find({"category": name, "active": True}, {"_id": 0})]
    await cb.message.answer(f"{name}:", reply_markup=products_kb(prods))
    await cb.answer()

@router.callback_query(F.data.startswith("prod:"))
async def open_product(cb: CallbackQuery):
    name = cb.data.split(":", 1)[1]
    p = await products.find_one({"name": name})
    if not p:
        await cb.answer("Product not found", show_alert=True)
        return
    desc = p.get("description") or "No description."
    price = p.get("price_usd", 0)
    img = p.get("image_url")
    caption = f"{name}\n\n{desc}\n\nPrice: ${price}"
    if img:
        await cb.message.answer_photo(photo=img, caption=caption, reply_markup=product_actions_kb(name))
    else:
        await cb.message.answer(caption, reply_markup=product_actions_kb(name))
    await cb.answer()

@router.callback_query(F.data.startswith("info:"))
async def info_product(cb: CallbackQuery):
    return await open_product(cb)  # Reuse

@router.callback_query(F.data.startswith("buy:"))
async def buy_product(cb: CallbackQuery):
    name = cb.data.split(":", 1)[1]
    p = await products.find_one({"name": name})
    if not p:
        await cb.answer("Product not found", show_alert=True)
        return
    price = p.get("price_usd", 0.0)
    u = await users.find_one({"telegram_id": cb.from_user.id}) or {}
    bal = float(u.get("balance_usd", 0.0))
    if bal < price:
        await cb.message.answer("❌ Insufficient balance. Please use Top Up 💳 to continue.")
        await cb.answer()
        return
    # Deduct and create order
    new_bal = round(bal - price, 2)
    await users.update_one({"telegram_id": cb.from_user.id}, {"$set": {"balance_usd": new_bal}})
    order_id = f"ORD-{uuid.uuid4().hex[:8].upper()}"
    await orders.insert_one({
        "order_id": order_id,
        "telegram_id": cb.from_user.id,
        "product_name": name,
        "amount_usd": price,
        "status": "PAID",
        "created_at": datetime.utcnow()
    })
    await cb.message.answer(f"✅ Purchased *{name}* for ${price:.2f}.\nRemaining balance: ${new_bal:.2f}", parse_mode="Markdown")
    await cb.answer()
