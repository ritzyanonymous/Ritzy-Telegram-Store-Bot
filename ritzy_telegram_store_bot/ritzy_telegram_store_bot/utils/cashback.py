def compute_fee_and_cashback(amount_usd: float) -> tuple[float, float]:
    """Returns (fee, cashback) in USD.
    Fee: 3% of amount
    Cashback tiers:
      - $3 for $105–$200
      - $10 for $210–$500
      - $35 for $520+
    """
    fee = round(amount_usd * 0.03, 2)
    cashback = 0.0
    if 105 <= amount_usd <= 200:
        cashback = 3.0
    elif 210 <= amount_usd <= 500:
        cashback = 10.0
    elif amount_usd >= 520:
        cashback = 35.0
    return fee, cashback
