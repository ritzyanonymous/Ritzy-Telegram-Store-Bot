# Ritzy Telegram Store Bot (Fixed)

Python (aiogram + FastAPI + MongoDB) with BTCPay top-ups, wallet balances, categories/products, and admin panel.

## What's Fixed (from review)
- DB client access (webhook no longer crashes)
- Integer prices accepted in admin
- Atomic invoice processing (no double-credit on duplicate webhooks)
- Robust BTCPay error handling
- Timezone-aware datetimes
- Validation for names (no ':'; max lengths)
- Admin ID validation (prevent shipping with example)

## Quick Start
1) Copy `.env.example` → `.env` and fill values
2) Install deps:
   ```bash
   pip install -r requirements.txt
   ```
3) Run:
   ```bash
   # Webhook server (FastAPI)
   uvicorn backend.app:app --host 0.0.0.0 --port 8000 --reload
   # Bot (aiogram)
   python -m bot.main
   ```
4) Point BTCPay webhook to: `POST {PUBLIC_BASE_URL}/webhooks/btcpay`
