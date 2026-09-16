import danduan_bank_storage
import danduan_bank_transactions
from decimal import Decimal


class BankService:
    """Application-level abstraction for banking operations."""

    def deposit(self, account, amount):
        if not account.deposit(amount):
            return False, "Invalid deposit amount."

        danduan_bank_storage.update_account(account)
        danduan_bank_transactions.record_transaction(
            account, "Deposit", amount
        )
        return True, "Deposit successful."

    def withdraw(self, account, amount):
        amount = Decimal(str(amount))

        if amount <= 0:
            return False, "Invalid withdrawal amount."

        if not account.can_withdraw(amount):
            return False, "Insufficient balance."

        if not account.withdraw(amount):
            return False, "Withdrawal failed."

        danduan_bank_storage.update_account(account)
        danduan_bank_transactions.record_transaction(
            account, "Withdraw", amount
        )
        return True, "Withdrawal successful."
    
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
