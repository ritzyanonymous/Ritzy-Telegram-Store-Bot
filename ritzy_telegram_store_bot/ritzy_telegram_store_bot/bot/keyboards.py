from aiogram.utils.keyboard import ReplyKeyboardBuilder, InlineKeyboardBuilder
from aiogram.types import KeyboardButton, InlineKeyboardButton

def main_menu_kb():
    kb = ReplyKeyboardBuilder()
    kb.button(text="MyID 👤")
    kb.button(text="Top Up 💳")
    kb.button(text="Rules / Manual 📜")
    kb.button(text="Support ✋🏻")
    kb.button(text="Store 🛍️")
    kb.adjust(2,2,1)
    return kb.as_markup(resize_keyboard=True)

def topup_currency_kb():
    ikb = InlineKeyboardBuilder()
    # Note: BTCPay will show available methods; these are hints we pass.
    ikb.button(text="💰 BTC", callback_data="topup:BTC")
    ikb.button(text="⚡ Lightning", callback_data="topup:BTC-LightningNetwork")
    # Add more if your BTCPay store supports them.
    ikb.adjust(2)
    return ikb.as_markup()

def support_kb(admin_username: str):
    ikb = InlineKeyboardBuilder()
    ikb.button(text="🧑‍💻 Admin", url=f"https://t.me/{admin_username}")
    return ikb.as_markup()

def categories_kb(categories: list[dict]):
    ikb = InlineKeyboardBuilder()
    for cat in categories:
        emoji = cat.get("emoji") or "📦"
        name = cat.get("name")
        ikb.button(text=f"{emoji} {name}", callback_data=f"cat:{name}")
    if not categories:
        ikb.button(text="(No categories yet)", callback_data="noop")
    ikb.adjust(1)
    return ikb.as_markup()

def products_kb(products: list[dict]):
    ikb = InlineKeyboardBuilder()
    for p in products:
        name = p.get("name")
        price = p.get("price_usd", 0)
        ikb.button(text=f"🛒 {name} — ${price}", callback_data=f"prod:{name}")
    if not products:
        ikb.button(text="(No products in this category)", callback_data="noop")
    ikb.adjust(1)
    return ikb.as_markup()

def product_actions_kb(product_name: str):
    ikb = InlineKeyboardBuilder()
    ikb.button(text="Buy 💰", callback_data=f"buy:{product_name}")
    ikb.button(text="More Info ℹ️", callback_data=f"info:{product_name}")
    ikb.adjust(2)
    return ikb.as_markup()

# Admin menus
def admin_menu_kb():
    kb = InlineKeyboardBuilder()
    kb.button(text="➕ Add Category", callback_data="admin:addcat")
    kb.button(text="➕ Add Product", callback_data="admin:addprod")
    kb.button(text="🗂️ List Products", callback_data="admin:listprod")
    kb.button(text="🗑️ Delete Product", callback_data="admin:delprod")
    kb.button(text="📊 Stats", callback_data="admin:stats")
    kb.adjust(2,2,1)
    return kb.as_markup()
