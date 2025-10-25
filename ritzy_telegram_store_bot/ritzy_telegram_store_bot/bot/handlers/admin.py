from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext
from bot.keyboards import admin_menu_kb
from bot.config import settings
from database.mongo import categories, products, users, orders, transactions

router = Router()

def is_admin(msg: Message | CallbackQuery) -> bool:
    uid = msg.from_user.id if isinstance(msg, Message) else msg.from_user.id
    return uid == settings.ADMIN_ID

@router.message(F.text == "/admin")
async def admin_menu(msg: Message):
    if not is_admin(msg):
        return
    await msg.answer("🔐 Admin Panel", reply_markup=admin_menu_kb())

class AddCategoryStates(StatesGroup):
    name = State()
    emoji = State()

@router.callback_query(F.data == "admin:addcat")
async def admin_add_cat(cb: CallbackQuery, state: FSMContext):
    if not is_admin(cb):
        await cb.answer("Not allowed", show_alert=True)
        return
    await cb.message.answer("Enter category name:")
    await state.set_state(AddCategoryStates.name)
    await cb.answer()

@router.message(AddCategoryStates.name)
async def admin_add_cat_name(msg: Message, state: FSMContext):
    if not is_admin(msg):
        return
    await state.update_data(name=msg.text.strip())
    await msg.answer("Enter emoji (or send '-' to skip):")
    await state.set_state(AddCategoryStates.emoji)

@router.message(AddCategoryStates.emoji)
async def admin_add_cat_finish(msg: Message, state: FSMContext):
    if not is_admin(msg):
        return
    data = await state.get_data()
    name = data.get("name")
    emoji = None if msg.text.strip() == "-" else msg.text.strip()
    await categories.update_one({"name": name}, {"$set": {"name": name, "emoji": emoji}}, upsert=True)
    await msg.answer(f"✅ Category saved: {emoji + ' ' if emoji else ''}{name}")
    await state.clear()

class AddProductStates(StatesGroup):
    name = State()
    price = State()
    category = State()
    description = State()
    image_url = State()

@router.callback_query(F.data == "admin:addprod")
async def admin_add_prod(cb: CallbackQuery, state: FSMContext):
    if not is_admin(cb):
        await cb.answer("Not allowed", show_alert=True)
        return
    await cb.message.answer("Enter product name:")
    await state.set_state(AddProductStates.name)
    await cb.answer()

@router.message(AddProductStates.name)
async def admin_add_prod_name(msg: Message, state: FSMContext):
    if not is_admin(msg):
        return
    await state.update_data(name=msg.text.strip())
    await msg.answer("Enter price in USD (e.g., 49.99):")
    await state.set_state(AddProductStates.price)

@router.message(AddProductStates.price, F.text.regexp(r"^\d+(?:\.\d{1,2})?$"))
async def admin_add_prod_price(msg: Message, state: FSMContext):
    if not is_admin(msg):
        return
    await state.update_data(price=float(msg.text))
    await msg.answer("Enter category name (must exist):")
    await state.set_state(AddProductStates.category)

@router.message(AddProductStates.category)
async def admin_add_prod_category(msg: Message, state: FSMContext):
    if not is_admin(msg):
        return
    await state.update_data(category=msg.text.strip())
    await msg.answer("Enter description (or '-' to skip):")
    await state.set_state(AddProductStates.description)

@router.message(AddProductStates.description)
async def admin_add_prod_desc(msg: Message, state: FSMContext):
    if not is_admin(msg):
        return
    desc = None if msg.text.strip() == "-" else msg.text.strip()
    await state.update_data(description=desc)
    await msg.answer("Enter image URL (or '-' to skip):")
    await state.set_state(AddProductStates.image_url)

@router.message(AddProductStates.image_url)
async def admin_add_prod_finish(msg: Message, state: FSMContext):
    if not is_admin(msg):
        return
    data = await state.get_data()
    image_url = None if msg.text.strip() == "-" else msg.text.strip()
    doc = {
        "name": data.get("name"),
        "price_usd": data.get("price"),
        "category": data.get("category"),
        "description": data.get("description"),
        "image_url": image_url,
        "active": True
    }
    await products.update_one({"name": doc["name"]}, {"$set": doc}, upsert=True)
    await msg.answer(f"✅ Product saved: {doc['name']} — ${doc['price_usd']}")
    await state.clear()

@router.callback_query(F.data == "admin:listprod")
async def admin_list_products(cb: CallbackQuery):
    if not is_admin(cb):
        await cb.answer("Not allowed", show_alert=True)
        return
    docs = [p async for p in products.find({}, {"_id": 0}).sort("category", 1)]
    if not docs:
        await cb.message.answer("No products yet.")
        await cb.answer()
        return
    out = []
    for d in docs:
        out.append(f"• [{d.get('category')}] {d.get('name')} — ${d.get('price_usd')} ")
    await cb.message.answer("\n".join(out))
    await cb.answer()

class DeleteProductStates(StatesGroup):
    name = State()

@router.callback_query(F.data == "admin:delprod")
async def admin_delprod(cb: CallbackQuery, state: FSMContext):
    if not is_admin(cb):
        await cb.answer("Not allowed", show_alert=True)
        return
    await cb.message.answer("Enter the exact product name to delete:")
    await state.set_state(DeleteProductStates.name)
    await cb.answer()

@router.message(DeleteProductStates.name)
async def admin_delprod_name(msg: Message, state: FSMContext):
    if not is_admin(msg):
        return
    name = msg.text.strip()
    res = await products.delete_one({"name": name})
    if res.deleted_count:
        await msg.answer(f"🗑️ Deleted: {name}")
    else:
        await msg.answer("Not found.")
    await state.clear()

@router.callback_query(F.data == "admin:stats")
async def admin_stats(cb: CallbackQuery):
    if not is_admin(cb):
        await cb.answer("Not allowed", show_alert=True)
        return
    users_count = await users.count_documents({})
    orders_count = await orders.count_documents({})
    tx_count = await transactions.count_documents({"type": "DEPOSIT"})
    await cb.message.answer(f"👥 Users: {users_count}\n🧾 Orders: {orders_count}\n💳 Deposits: {tx_count}")
    await cb.answer()
