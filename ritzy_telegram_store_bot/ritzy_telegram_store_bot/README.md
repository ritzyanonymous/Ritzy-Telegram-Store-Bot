# Ritzy Telegram Store Bot (Python / aiogram + FastAPI + MongoDB) with BTCPay

A ready-to-run starter for a Telegram storefront bot with user balances, crypto top-ups via **BTCPay Server**, product **categories**, an in-bot **admin panel**, and a **FastAPI** backend for webhooks.

## Features
- 5-button main menu: **MyID**, **Top Up**, **Rules / Manual**, **Support**, **Store**
- User accounts (Telegram ID, username), wallet **balance** in USD (pegged)
- **Top Up** via BTCPay invoice (3% fee + cashback tiers applied on credit)
- **Store** with categories → products → Buy using balance
- **Admin panel** (restricted by `ADMIN_ID`) to add categories/products directly in the bot
- MongoDB (async with `motor`)
- FastAPI backend with **BTCPay webhook** endpoint

## Quick Start
1. Create `.env` from `.env.example` and fill values:
   - `TELEGRAM_BOT_TOKEN` (BotFather)
   - `ADMIN_ID=1014293448` (already set)
   - `MONGO_URI`, `MONGO_DB`
   - `PUBLIC_BASE_URL` (public HTTPS exposed URL for webhooks)
   - `BTCPAY_HOST`, `BTCPAY_API_KEY`, `BTCPAY_STORE_ID`
   - Optional: `BTCPAY_WEBHOOK_SECRET` for signature verification

2. Install deps and run services (two terminals):
   ```bash
   pip install -r requirements.txt
   # Terminal A (FastAPI webhook server):
   uvicorn backend.app:app --host 0.0.0.0 --port 8000 --reload
   # Terminal B (Telegram bot long-polling):
   python -m bot.main
   ```

3. Expose your FastAPI to the public (for BTCPay webhooks), e.g.:
   ```bash
   # Example with ngrok
   ngrok http http://localhost:8000
   # Put the HTTPS URL into PUBLIC_BASE_URL in .env 
   ```

4. In BTCPay Server:
   - Create an API key (Permissions: Invoices.Create, Invoices.Read, Webhooks.CanModify)
   - Create a webhook pointing to: `POST {PUBLIC_BASE_URL}/webhooks/btcpay`
   - (Optional) Set a webhook secret; put it in `.env` as `BTCPAY_WEBHOOK_SECRET`

## Notes
- **Currency** is pegged to USD in this starter. BTCPay will offer whatever payment methods you enabled (BTC, Lightning, etc.).
- **Invoice amount** is the top-up amount the user chooses; upon webhook confirmation, we credit **(amount - 3% fee + cashback)**.
- Cashback tiers (applied on credited USD amount):
  - $3 for $105–$200
  - $10 for $210–$500
  - $35 for $520+

## Project Structure
```
/bot
  main.py
  config.py
  keyboards.py
  /handlers
    admin.py
    store.py
    topup.py
    user_menu.py
/backend
  app.py
  btcpay.py
/database
  mongo.py
  models.py
/utils
  cashback.py
  formatting.py
.env.example
requirements.txt
README.md
```

## Safety & Production Tips
- Keep only small hot balances. Move funds to cold storage periodically.
- Use HTTPS everywhere; set webhook signature verification in production.
- Add rate limiting and basic ACLs on admin commands.
