from abc import ABC, abstractmethod
from decimal import Decimal, InvalidOperation


class BankAccount(ABC):
    """Abstract base class for all bank account types."""

    def __init__(self, account_number, name, pin, starting_balance=0):
        self._account_number = str(account_number).strip()
        self._account_name = str(name).strip()
        self._pin = str(pin).strip()
        self._balance = self._to_money(starting_balance)

        if self._balance < Decimal("0"):
            raise ValueError("Starting balance cannot be negative.")

    @staticmethod
    def _to_money(amount):
        try:
            value = Decimal(str(amount))
        except (InvalidOperation, ValueError):
            raise ValueError("Amount must be a valid number.")

        return value.quantize(Decimal("0.01"))

    # Encapsulation: public read-only properties expose controlled data.
    @property
    def account_number(self):
        return self._account_number

    @property
    def account_name(self):
        return self._account_name

    @property
    def balance(self):
        return self._balance

    def check_balance(self):
        return self._balance

    def deposit(self, amount):
        amount = self._to_money(amount)

        if amount <= Decimal("0"):
            return False

        self._balance += amount
        return True

    def withdraw(self, amount):
        amount = self._to_money(amount)

        if not self.can_withdraw(amount):
            return False

        self._balance -= amount
        return True

    def can_withdraw(self, amount):
        amount = self._to_money(amount)
        return amount > Decimal("0") and amount <= self._balance

    def verify_pin(self, pin):
        return self._pin == str(pin).strip()

    # Kept for the existing text-file format.
    # The PIN remains internal and is not exposed as a normal property.
    def get_pin(self):
        return self._pin

    # Controlled internal update used by persistence code.
    def _restore_balance(self, balance):
        balance = self._to_money(balance)
        if balance < Decimal("0"):
            raise ValueError("Balance cannot be negative.")
        self._balance = balance

    # Abstraction: subclasses must provide their own account identity.
    @abstractmethod
    def get_account_type(self):
        pass

    @abstractmethod
    def get_account_description(self):
        pass


# Inheritance + Polymorphism
class SavingsAccount(BankAccount):

    def get_account_type(self):
        return "Savings Account"

    def get_account_description(self):
        return "For saving money and building a balance."


# Inheritance + Polymorphism
class StudentAccount(BankAccount):

    def get_account_type(self):
        return "Student Account"

    def get_account_description(self):
        return "Designed for students with simple everyday banking."

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