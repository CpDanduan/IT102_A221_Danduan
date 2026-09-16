from danduan_bank_account import SavingsAccount, StudentAccount

USERS_FILE = "users.txt"


def _account_from_record(record):
    account_classes = {
        "Savings Account": SavingsAccount,
        "Student Account": StudentAccount,
    }

    account_class = account_classes.get(record.get("account_type"))
    if account_class is None:
        return None

    return account_class(
        record["account_number"],
        record["account_name"],
        record["pin"],
        record.get("balance", "0.00"),
    )


def account_exists(account_number):
    return find_account(account_number) is not None


def save_account(account):
    with open(USERS_FILE, "a", encoding="utf-8") as file:
        file.write(f"Account Number: {account.account_number}\n")
        file.write(f"Account Name: {account.account_name}\n")
        file.write(f"PIN: {account.get_pin()}\n")
        file.write(f"Account Type: {account.get_account_type()}\n")
        file.write(f"Balance: {account.balance:.2f}\n\n")


def load_accounts():
    accounts = []
    current = {}

    try:
        with open(USERS_FILE, "r", encoding="utf-8") as file:
            lines = file.readlines()
    except FileNotFoundError:
        return accounts

    for raw_line in lines:
        line = raw_line.strip()

        if not line:
            continue

        if line.startswith("Account Number:"):
            current["account_number"] = line.split(":", 1)[1].strip()
        elif line.startswith("Account Name:"):
            current["account_name"] = line.split(":", 1)[1].strip()
        elif line.startswith("PIN:"):
            current["pin"] = line.split(":", 1)[1].strip()
        elif line.startswith("Account Type:"):
            current["account_type"] = line.split(":", 1)[1].strip()
        elif line.startswith("Balance:"):
            current["balance"] = line.split(":", 1)[1].strip()

            required = {"account_number", "account_name", "pin", "account_type"}
            if required.issubset(current):
                try:
                    account = _account_from_record(current)
                    if account is not None:
                        accounts.append(account)
                except (ValueError, KeyError):
                    pass

            current = {}

    return accounts


def find_account(account_number):
    for account in load_accounts():
        if account.account_number == account_number:
            return account
    return None


def update_account(account):
    accounts = load_accounts()

    with open(USERS_FILE, "w", encoding="utf-8") as file:
        for saved_account in accounts:
            if saved_account.account_number == account.account_number:
                saved_account._restore_balance(account.balance)

            file.write(f"Account Number: {saved_account.account_number}\n")
            file.write(f"Account Name: {saved_account.account_name}\n")
            file.write(f"PIN: {saved_account.get_pin()}\n")
            file.write(f"Account Type: {saved_account.get_account_type()}\n")
            file.write(f"Balance: {saved_account.balance:.2f}\n\n")

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