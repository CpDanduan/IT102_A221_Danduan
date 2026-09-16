import os
import tempfile

import danduan_bank_storage



def validate_pin(pin):
    """Return True when pin is exactly four digits."""
    pin = str(pin).strip()
    return len(pin) == 4 and pin.isdigit()



def _replace_pin_in_storage(account_number, new_pin):
    """Update only the PIN belonging to one account in users.txt."""
    users_file = danduan_bank_storage.USERS_FILE

    if not os.path.exists(users_file):
        return False

    with open(users_file, "r", encoding="utf-8") as file:
        lines = file.readlines()

    updated = False
    inside_account = False
    output = []

    for line in lines:
        stripped = line.strip()

        if stripped.startswith("Account Number:"):
            saved_number = stripped.split(":", 1)[1].strip()
            inside_account = saved_number == str(account_number).strip()

        if inside_account and stripped.startswith("PIN:"):
            output.append(f"PIN: {new_pin}\n")
            updated = True
        else:
            output.append(line)

        if inside_account and stripped == "":
            inside_account = False

    if not updated:
        return False

    directory = os.path.dirname(os.path.abspath(users_file)) or "."
    fd, temp_path = tempfile.mkstemp(
        prefix="danduan_users_",
        suffix=".tmp",
        dir=directory,
        text=True,
    )

    try:
        with os.fdopen(fd, "w", encoding="utf-8") as file:
            file.writelines(output)

        os.replace(temp_path, users_file)
        return True
    except OSError:
        try:
            os.remove(temp_path)
        except OSError:
            pass
        return False



def change_pin(account, current_pin, new_pin, confirm_pin):
    """Change an authenticated account's PIN.

    Returns:
        (True, success_message) or (False, error_message)
    """
    current_pin = str(current_pin).strip()
    new_pin = str(new_pin).strip()
    confirm_pin = str(confirm_pin).strip()

    if not account.verify_pin(current_pin):
        return False, "Current PIN is incorrect."

    if not validate_pin(new_pin):
        return False, "New PIN must contain exactly 4 digits."

    if new_pin != confirm_pin:
        return False, "New PIN confirmation does not match."

    if new_pin == current_pin:
        return False, "New PIN must be different from your current PIN."

    if not _replace_pin_in_storage(account.account_number, new_pin):
        return False, "Unable to save the new PIN. Please try again."

    # Keep the currently logged-in account synchronized with users.txt.
    account._pin = new_pin

    return True, "PIN changed successfully."
