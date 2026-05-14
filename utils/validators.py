import re
from typing import Optional
from .exceptions import ValidationError


class Validator:
    @staticmethod
    def validate_account_number(account_no: str) -> tuple[bool, Optional[str]]:
        if not account_no:
            return False, "Account number is required"

        if not account_no.isdigit():
            return False, "Account number must contain only digits"

        if len(account_no) < 6 or len(account_no) > 12:
            return False, "Account number must be between 6 and 12 digits"

        return True, None

    @staticmethod
    def validate_amount(amount: str, min_amount: int = 100, max_amount: int = 100000) -> tuple[bool, Optional[str]]:
        if not amount:
            return False, "Amount is required"

        if not amount.isdigit():
            return False, "Amount must be a valid number"

        amount_int = int(amount)

        if amount_int < min_amount:
            return False, f"Minimum amount is {min_amount} ₹"

        if amount_int > max_amount:
            return False, f"Maximum amount is {max_amount} ₹"

        if amount_int % 100 != 0:
            return False, "Amount must be a multiple of 100"

        return True, None

    @staticmethod
    def validate_name(name: str) -> tuple[bool, Optional[str]]:
        if not name or not name.strip():
            return False, "Name is required"

        name = name.strip()

        if len(name) < 2:
            return False, "Name must be at least 2 characters"

        if len(name) > 50:
            return False, "Name must not exceed 50 characters"

        if not re.match(r'^[a-zA-Z\s]+$', name):
            return False, "Name must contain only letters and spaces"

        return True, None

    @staticmethod
    def validate_pin(pin: str) -> tuple[bool, Optional[str]]:
        if not pin:
            return False, "PIN is required"

        if not pin.isdigit():
            return False, "PIN must contain only digits"

        if len(pin) < 4 or len(pin) > 6:
            return False, "PIN must be 4-6 digits"

        return True, None