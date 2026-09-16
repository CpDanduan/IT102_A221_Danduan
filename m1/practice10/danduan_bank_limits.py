import json
import os
from datetime import datetime

import danduan_bank_transactions


LIMITS_FILE = "withdrawal_limits.json"
DEFAULT_DAILY_LIMIT = 10000.00
MIN_DAILY_LIMIT = 500.00
MAX_DAILY_LIMIT = 100000.00



def _load_limits():
    try:
        with open(LIMITS_FILE, "r", encoding="utf-8") as file:
            data = json.load(file)
            return data if isinstance(data, dict) else {}
    except (FileNotFoundError, json.JSONDecodeError):
        return {}



def _save_limits(limits):
    with open(LIMITS_FILE, "w", encoding="utf-8") as file:
        json.dump(limits, file, indent=4)



def get_daily_limit(account_number):
    """Get an account's daily withdrawal limit."""
    limits = _load_limits()
    return float(limits.get(str(account_number), DEFAULT_DAILY_LIMIT))



def set_daily_limit(account_number, new_limit):
    """Set a daily withdrawal limit within the allowed range."""
    try:
        new_limit = float(new_limit)
    except (TypeError, ValueError):
        return False, "Daily withdrawal limit must be a valid number."

    if new_limit < MIN_DAILY_LIMIT:
        return False, (
            f"Daily withdrawal limit cannot be below "
            f"₱{MIN_DAILY_LIMIT:,.2f}."
        )

    if new_limit > MAX_DAILY_LIMIT:
        return False, (
            f"Daily withdrawal limit cannot exceed "
            f"₱{MAX_DAILY_LIMIT:,.2f}."
        )

    limits = _load_limits()
    limits[str(account_number)] = round(new_limit, 2)
    _save_limits(limits)

    return True, "Daily withdrawal limit updated successfully."



def get_today_withdrawn(account_number):
    """Calculate today's withdrawals from the existing transaction history."""
    today = datetime.now().date()
    total = 0.0

    for transaction in danduan_bank_transactions.get_transactions():
        if str(transaction.get("account_number")) != str(account_number):
            continue

        if transaction.get("transaction") != "Withdraw":
            continue

        try:
            timestamp = datetime.strptime(
                transaction.get("timestamp", ""),
                "%Y-%m-%d %H:%M:%S",
            )
        except ValueError:
            continue

        if timestamp.date() == today:
            total += float(transaction.get("amount", 0))

    return round(total, 2)



def get_remaining_limit(account_number):
    """Return the amount that can still be withdrawn today."""
    remaining = (
        get_daily_limit(account_number)
        - get_today_withdrawn(account_number)
    )

    return round(max(0.0, remaining), 2)



def can_withdraw(account_number, amount):
    """Check whether a withdrawal stays within today's limit."""
    try:
        amount = float(amount)
    except (TypeError, ValueError):
        return False, "Withdrawal amount must be a valid number."

    if amount <= 0:
        return False, "Withdrawal amount must be greater than zero."

    remaining = get_remaining_limit(account_number)

    if amount > remaining:
        return False, (
            f"Daily withdrawal limit exceeded. "
            f"You have ₱{remaining:,.2f} remaining today."
        )

    return True, "Withdrawal is within the daily limit."
