import danduan_bank_transactions


def analyze_transactions(account_number=None):
    transactions = danduan_bank_transactions.get_transactions()

    if account_number is not None:
        transactions = [
            transaction
            for transaction in transactions
            if transaction.get("account_number") == account_number
        ]

    total_transactions = len(transactions)
    deposits = 0
    withdrawals = 0
    total_deposited = 0.0
    total_withdrawn = 0.0
    largest_transaction = 0.0

    for transaction in transactions:
        transaction_type = transaction.get("transaction", "")
        amount = transaction.get("amount", 0.0)

        if transaction_type == "Deposit":
            deposits += 1
            total_deposited += amount
        elif transaction_type == "Withdraw":
            withdrawals += 1
            total_withdrawn += amount

        largest_transaction = max(largest_transaction, amount)

    total_transaction_amount = total_deposited + total_withdrawn
    average_transaction = (
        total_transaction_amount / total_transactions
        if total_transactions
        else 0.0
    )

    latest = transactions[-1] if transactions else {}

    return {
        "total_transactions": total_transactions,
        "deposits": deposits,
        "withdrawals": withdrawals,
        "total_deposited": total_deposited,
        "total_withdrawn": total_withdrawn,
        "net_cash_flow": total_deposited - total_withdrawn,
        "largest_transaction": largest_transaction,
        "average_transaction": average_transaction,
        "latest_transaction": latest.get("transaction", "None"),
        "latest_timestamp": latest.get("timestamp", "None"),
    }

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