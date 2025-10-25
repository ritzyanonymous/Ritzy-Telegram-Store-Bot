import httpx
from bot.config import settings

class BTCPayClient:
    def __init__(self):
        self.host = settings.BTCPAY_HOST.rstrip("/")
        self.api_key = settings.BTCPAY_API_KEY
        self.store_id = settings.BTCPAY_STORE_ID
        self.headers = {"Authorization": f"token {self.api_key}"}

    async def create_invoice(self, amount_usd: float, telegram_id: int, payment_methods: list[str] | None = None) -> dict:
        url = f"{self.host}/api/v1/stores/{self.store_id}/invoices"
        payload = {
            "amount": str(round(amount_usd, 2)),
            "currency": "USD",
            "metadata": {
                "telegram_id": telegram_id,
                "purpose": "wallet_topup"
            }
        }
        if payment_methods:
            payload["checkout"] = {"paymentMethods": payment_methods}
        async with httpx.AsyncClient(timeout=30) as client:
            r = await client.post(url, json=payload, headers=self.headers)
            r.raise_for_status()
            return r.json()
