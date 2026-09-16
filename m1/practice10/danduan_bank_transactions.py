from dataclasses import dataclass
from datetime import datetime
from decimal import Decimal

TRANSACTIONS_FILE = "transactions.txt"


@dataclass(frozen=True)
class Transaction:
    """Encapsulates one completed banking transaction."""

    timestamp: str
    account_number: str
    account_name: str
    account_type: str
    transaction_type: str
    amount: Decimal
    balance_after: Decimal

    def to_record(self):
        return {
            "timestamp": self.timestamp,
            "account_number": self.account_number,
            "account": self.account_name,
            "account_type": self.account_type,
            "transaction": self.transaction_type,
            "amount": float(self.amount),
            "balance_after": float(self.balance_after),
        }


def record_transaction(account, transaction_type, amount):
    transaction = Transaction(
        timestamp=datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        account_number=account.account_number,
        account_name=account.account_name,
        account_type=account.get_account_type(),
        transaction_type=transaction_type,
        amount=Decimal(str(amount)).quantize(Decimal("0.01")),
        balance_after=account.balance,
    )

    with open(TRANSACTIONS_FILE, "a", encoding="utf-8") as file:
        file.write(f"Timestamp: {transaction.timestamp}\n")
        file.write(f"Account Number: {transaction.account_number}\n")
        file.write(f"Account: {transaction.account_name}\n")
        file.write(f"Account Type: {transaction.account_type}\n")
        file.write(f"Transaction: {transaction.transaction_type}\n")
        file.write(f"Amount: ₱{transaction.amount:,.2f}\n")
        file.write(f"Balance After: ₱{transaction.balance_after:,.2f}\n\n")


def get_transactions():
    transactions = []
    current = {}

    try:
        with open(TRANSACTIONS_FILE, "r", encoding="utf-8") as file:
            lines = file.readlines()
    except FileNotFoundError:
        return transactions

    for raw_line in lines:
        line = raw_line.strip()

        if not line:
            continue

        if line.startswith("Timestamp:"):
            current["timestamp"] = line.split(":", 1)[1].strip()
        elif line.startswith("Account Number:"):
            current["account_number"] = line.split(":", 1)[1].strip()
        elif line.startswith("Account:"):
            current["account"] = line.split(":", 1)[1].strip()
        elif line.startswith("Account Type:"):
            current["account_type"] = line.split(":", 1)[1].strip()
        elif line.startswith("Transaction:"):
            current["transaction"] = line.split(":", 1)[1].strip()
        elif line.startswith("Amount:"):
            current["amount"] = _parse_money(line)
        elif line.startswith("Balance After:"):
            current["balance_after"] = _parse_money(line)

            required = {
                "timestamp", "account_number", "transaction",
                "amount", "balance_after"
            }
            if required.issubset(current):
                transactions.append(current.copy())

            current = {}

    return transactions


def _parse_money(line):
    value = line.split(":", 1)[1].replace("₱", "").replace(",", "").strip()
    try:
        return float(value)
    except ValueError:
        return 0.0

""" 
######### Learning Signature ######### 
Programmed by: Cristian Paul P Danduan
Date Submitted: September 14, 2026
 
Program Description: This program is about bank service.
Reflection: I learned how to improve an existing code.
 
AI Usage
[ ] No AI Assistance - Completed independently without AI.
[ ] AI as Support Tool - Used AI for explanations, syntax, or minor corrections.
[/] AI as Collaborative Partner - Used AI to design, structure, or co-create significant code.
"""