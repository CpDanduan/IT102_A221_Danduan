from danduan_bank_account import SavingsAccount, StudentAccount
import danduan_bank_storage


def validate_pin(pin):
    pin = str(pin).strip()
    return pin.isdigit() and len(pin) == 4


def _create_account(account_type, account_number, name, pin, starting_balance):
    """Factory-style helper that hides account-object creation."""
    account_classes = {
        "Savings Account": SavingsAccount,
        "Student Account": StudentAccount,
    }

    account_class = account_classes.get(account_type)
    if account_class is None:
        return None

    return account_class(account_number, name, pin, starting_balance)


def register_account(
    name,
    account_number,
    pin,
    confirm_pin,
    account_type,
    starting_balance,
):
    name = str(name).strip()
    account_number = str(account_number).strip()
    pin = str(pin).strip()
    confirm_pin = str(confirm_pin).strip()

    if not name:
        return None, "Please enter your name."

    if not account_number:
        return None, "Please enter an account number."

    if danduan_bank_storage.account_exists(account_number):
        return None, "Account number already exists."

    if not validate_pin(pin):
        return None, "PIN must contain exactly 4 digits."

    if pin != confirm_pin:
        return None, "PIN confirmation does not match."

    if starting_balance < 0:
        return None, "Starting balance cannot be negative."

    account = _create_account(
        account_type, account_number, name, pin, starting_balance
    )

    if account is None:
        return None, "Invalid account type."

    danduan_bank_storage.save_account(account)
    return account, "Registration successful."


def login_account(account_number, pin):
    account_number = str(account_number).strip()
    pin = str(pin).strip()

    account = danduan_bank_storage.find_account(account_number)

    if account is None or not account.verify_pin(pin):
        return None, "Invalid account number or PIN."

    return account, "Login successful."

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