# Danduan Bank - OOP Improvements

## Main improvements
1. Fixed inconsistent module names (`balaman_*` -> `danduan_*`).
2. Added `BankService` to keep the Streamlit UI separate from banking operations.
3. Added `Transaction` as an object instead of treating every transaction only as a loose dictionary.
4. Improved encapsulation with private account state and read-only properties.
5. Used `Decimal` for monetary calculations to reduce floating-point rounding problems.
6. Centralized account creation in an account factory-style helper.
7. Removed direct modification of `_balance` from the storage layer; balance restoration now goes through `_restore_balance()`.
8. Simplified transaction parsing and analysis.
9. Added account descriptions so polymorphism is visible in the user interface.

## OOP pillars in the source

### 1. Encapsulation
**File:** `danduan_bank_account.py`

- `BankAccount` stores `_account_number`, `_account_name`, `_pin`, and `_balance` as internal attributes.
- `account_number`, `account_name`, and `balance` are exposed through read-only `@property` methods.
- `deposit()`, `withdraw()`, `verify_pin()`, and `_restore_balance()` control how account state changes.
- The UI does not directly change `_balance`.

**File:** `danduan_bank_transactions.py`

- `Transaction` groups timestamp, account information, transaction type, amount, and balance-after into one object.
- `@dataclass(frozen=True)` prevents a completed transaction from being changed accidentally.

### 2. Abstraction
**File:** `danduan_bank_account.py`

- `BankAccount` is an `ABC` (Abstract Base Class).
- `get_account_type()` and `get_account_description()` are abstract methods.
- Code that works with a `BankAccount` does not need to know the exact subclass.

**File:** `danduan_bank_service.py`

- `BankService` hides the sequence of updating the account, saving it, and recording a transaction.
- The Streamlit application only calls `bank_service.deposit()` or `bank_service.withdraw()`.

### 3. Inheritance
**File:** `danduan_bank_account.py`

- `SavingsAccount(BankAccount)`
- `StudentAccount(BankAccount)`

Both subclasses inherit balance handling, PIN verification, deposit, and withdrawal behavior from `BankAccount`.

### 4. Polymorphism
**File:** `danduan_bank_account.py`

Both subclasses provide their own implementations of:
- `get_account_type()`
- `get_account_description()`

For example, the app can call:

```python
account.get_account_type()
account.get_account_description()
```

without checking whether `account` is a `SavingsAccount` or `StudentAccount`. Python dispatches the correct implementation at runtime.

**File:** `danduan_bank_storage.py`

`_account_from_record()` creates different subclasses from the saved account type. After creation, the rest of the application treats them uniformly as `BankAccount` objects.

## Why the design is better
The original project already had all four OOP pillars, but some of them were demonstrated only minimally. The improved version makes them easier to identify during an OOP/code review:

- Encapsulation is stronger because account state is controlled.
- Abstraction is stronger because the UI depends on `BankService` and `BankAccount` interfaces rather than implementation details.
- Inheritance remains simple and meaningful.
- Polymorphism is visible through account-specific behavior instead of only being a comment above an overridden method.

## Running the application

Install Streamlit if needed:

```bash
pip install streamlit
```

Then run:

```bash
streamlit run danduan_bank_app.py
```

The application creates `users.txt` and `transactions.txt` in the working directory if they do not exist.
