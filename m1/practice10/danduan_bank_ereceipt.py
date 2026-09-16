import json
import os
from datetime import datetime


SETTINGS_FILE = "ereceipt_settings.json"
RECEIPT_DIRECTORY = "e_receipts"



def _load_settings():
    try:
        with open(SETTINGS_FILE, "r", encoding="utf-8") as file:
            data = json.load(file)
            return data if isinstance(data, dict) else {}
    except (FileNotFoundError, json.JSONDecodeError):
        return {}



def _save_settings(settings):
    with open(SETTINGS_FILE, "w", encoding="utf-8") as file:
        json.dump(settings, file, indent=4)



def is_enabled(account_number):
    """Return whether e-receipts are enabled for an account.

    New accounts default to enabled so receipts work immediately.
    """
    settings = _load_settings()
    return settings.get(str(account_number), True)



def set_enabled(account_number, enabled):
    """Enable or disable e-receipts for an account."""
    settings = _load_settings()
    settings[str(account_number)] = bool(enabled)
    _save_settings(settings)
    return bool(enabled)



def get_status_text(account_number):
    return "Enabled" if is_enabled(account_number) else "Disabled"



def generate_receipt(account, transaction_type, amount, balance_after):
    """Create and save a text e-receipt.

    Returns the receipt text. If e-receipts are disabled, returns None.
    """
    if not is_enabled(account.account_number):
        return None

    now = datetime.now()
    timestamp = now.strftime("%Y-%m-%d %H:%M:%S")
    file_timestamp = now.strftime("%Y%m%d_%H%M%S_%f")
    masked_account = f"•••• {str(account.account_number)[-4:]}"

    receipt = (
        "=" * 42 + "\n"
        "          DANDUAN BANK\n"
        "        ELECTRONIC RECEIPT\n"
        "=" * 42 + "\n"
        f"Date & Time : {timestamp}\n"
        f"Account     : {masked_account}\n"
        f"Account Type: {account.get_account_type()}\n"
        f"Transaction : {transaction_type}\n"
        f"Amount      : ₱{float(amount):,.2f}\n"
        f"Balance     : ₱{float(balance_after):,.2f}\n"
        "=" * 42 + "\n"
        "Thank you for banking with Danduan Bank.\n"
        "This is an electronic receipt.\n"
        "=" * 42 + "\n"
    )

    os.makedirs(RECEIPT_DIRECTORY, exist_ok=True)

    filename = (
        f"receipt_{account.account_number}_"
        f"{file_timestamp}.txt"
    )

    path = os.path.join(RECEIPT_DIRECTORY, filename)

    with open(path, "w", encoding="utf-8") as file:
        file.write(receipt)

    return receipt
