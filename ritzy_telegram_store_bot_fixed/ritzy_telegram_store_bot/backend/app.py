from fastapi import FastAPI, Request, HTTPException
from bot.config import settings
from database.mongo import db_instance, users, transactions, invoices
from utils.cashback import compute_fee_and_cashback
from pymongo import ReturnDocument
import hmac, hashlib, json, httpx

app = FastAPI(title="Ritzy Store Backend")

@app.get("/")
async def root():
    return {"ok": True, "service": "ritzy-backend"}

@app.post("/webhooks/btcpay")
async def btcpay_webhook(request: Request):
    raw = await request.body()
    signature = request.headers.get("BTCPAY-SIG") or request.headers.get("Btcpay-Sig") or ""
    secret = settings.BTCPAY_WEBHOOK_SECRET
    if secret:
        digest = hmac.new(secret.encode(), raw, hashlib.sha256).hexdigest()
        expected = f"sha256={digest}"
        if expected != signature:
            raise HTTPException(status_code=400, detail="Invalid signature")

    payload = json.loads(raw.decode("utf-8"))
    evt_type = payload.get("type", "")
    data = payload.get("data", {})
    invoice_id = data.get("id") or payload.get("invoiceId") or ""

    if evt_type not in ("InvoiceSettled", "invoice.settled", "InvoiceProcessing", "InvoicePaid"):
        return {"ignored": True, "event": evt_type}

    result = await invoices.find_one_and_update(
        {"invoice_id": invoice_id, "status": {"$ne": "CONFIRMED"}},
        {"$set": {"status": "CONFIRMED"}},
        return_document=ReturnDocument.AFTER
    )
    if not result:
        return {"ok": True, "detail": "already processed or not found"}

    amount_usd = float(result.get("amount_usd", 0))
    telegram_id = int(result.get("telegram_id"))
    fee, cashback = compute_fee_and_cashback(amount_usd)
    credit = round(amount_usd - fee + cashback, 2)

    await users.update_one(
        {"telegram_id": telegram_id},
        {"$inc": {"balance_usd": credit}},
        upsert=True
    )
    await transactions.insert_one({
        "telegram_id": telegram_id,
        "type": "DEPOSIT",
        "amount_usd": amount_usd,
        "fee_usd": fee,
        "cashback_usd": cashback,
        "tx_ref": invoice_id,
        "status": "CONFIRMED",
    })

    try:
        async with httpx.AsyncClient(timeout=15) as client:
            msg = (f"✅ Deposit received: ${amount_usd:.2f}\n"
                   f"Fee: ${fee:.2f} | Cashback: ${cashback:.2f}\n"
                   f"Credited: ${credit:.2f}\n"
                   f"Thank you!" )
            await client.post(
                f"https://api.telegram.org/bot{settings.TELEGRAM_BOT_TOKEN}/sendMessage",
                json={"chat_id": telegram_id, "text": msg}
            )
    except Exception:
        pass

    return {"ok": True, "event": evt_type, "invoice": invoice_id}
