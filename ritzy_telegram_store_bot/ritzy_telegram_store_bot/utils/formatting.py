def format_profile(telegram_id: int, username: str | None, email: str | None, balance: float) -> str:
    handle = f"@{username}" if username else "Not set"
    mail = email if email else "Not set"
    return (            "My Profile 👤\n"
        "--------------\n"
        f"🆔: {telegram_id}\n"
        f"👤: {handle}\n"
        f"📧: {mail}\n"
        f"💰: {balance:.2f} $\n"
        f"🔗: {handle}\n"
        "--------------"        )

TOPUP_RULES = (        "Please Note The Following Deposit Rules ‼️‼️‼️\n"
    "🔘 3% Fee will be applied to the top-up amount \n"
    "🔘 Deposit less than the minimum will be lost \n"
    "🔘 Payment to old or expired addresses will be lost \n"
    "🔘 Once an address is generated it will stay valid for 5 hours \n"
    "🔘 Generate a New Address every time and pay to the latest Address\n"
    "-----------New Addition---------------\n"
    "💎 CashBack of $3 for a Deposit between $105 -$200 \n"
    "💎 CashBack of $10 for a Deposit between $210-$500 \n"
    "💎 CashBack of $35 for Deposit of $520 and more\n"
    "Please select the Currency for Top Up💰"    )
