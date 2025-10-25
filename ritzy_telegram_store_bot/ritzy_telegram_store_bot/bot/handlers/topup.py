from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext
from bot.keyboards import topup_currency_kb
from utils.formatting import TOPUP_RULES
from database.mongo import invoices, users
from backend.btcpay import BTCPayClient
from bot.config import settings

router = Router()

class TopUpStates(StatesGroup):
    waiting_amount = State()
    waiting_currency = State()

@router.message(F.text == "Top Up 💳")
async def topup_entry(msg: Message, state: FSMContext):
    await msg.answer(TOPUP_RULES, reply_markup=topup_currency_kb())
    await state.set_state(TopUpStates.waiting_currency)

@router.callback_query(F.data.startswith("topup:"))
async def topup_select_currency(cb: CallbackQuery, state: FSMContext):
    payment_method = cb.data.split(":", 1)[1]
    await state.update_data(payment_method=payment_method)
    await cb.message.answer("Enter the amount in USD you want to deposit (e.g., 50):")
    await state.set_state(TopUpStates.waiting_amount)
    await cb.answer()

@router.message(TopUpStates.waiting_amount, F.text.regexp(r"^\d+(?:\.\d{1,2})?$"))
async def topup_create_invoice(msg: Message, state: FSMContext):
    amount = float(msg.text)
    if amount < 10:
        await msg.answer("Minimum deposit is $10. Please enter a higher amount:")
        return
    data = await state.get_data()
    pm = data.get("payment_method")

    # Ensure user exists
    await users.update_one(
        {"telegram_id": msg.from_user.id},
        {"$setOnInsert": {"telegram_id": msg.from_user.id, "username": msg.from_user.username, "balance_usd": 0.0}},
        upsert=True
    )

    client = BTCPayClient()
    payment_methods = [pm] if pm else None
    inv = await client.create_invoice(amount_usd=amount, telegram_id=msg.from_user.id, payment_methods=payment_methods)

    invoice_id = inv.get("id") or inv.get("invoiceId")
    checkout_link = inv.get("checkoutLink") or inv.get("checkoutUrl") or ""

    await invoices.insert_one({
        "invoice_id": invoice_id,
        "telegram_id": msg.from_user.id,
        "amount_usd": amount,
        "payment_methods": payment_methods,
        "status": "NEW",
    })

    txt = ("🔗 Your top-up invoice is ready!\n"
           f"Amount: ${amount:.2f}\n"
           f"Invoice ID: {invoice_id}\n"
           f"Pay here: {checkout_link}\n\n"
           "Note: The payment address might expire according to BTCPay settings.\n"
           "Once paid and confirmed, your balance will be credited automatically.")
    await msg.answer(txt)
    await state.clear()

@router.message(TopUpStates.waiting_amount)
async def topup_invalid_amount(msg: Message):
    await msg.answer("Invalid amount. Please enter a number like 50 or 12.99:")
