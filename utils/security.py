import hashlib
import secrets
import re
from typing import Optional


def hash_pin(pin: str) -> str:
    salt = secrets.token_hex(16)
    hash_obj = hashlib.pbkdf2_hmac(
        'sha256',
        pin.encode('utf-8'),
        salt.encode('utf-8'),
        100000
    )
    return f"{salt}${hash_obj.hex()}"


def verify_pin(pin: str, stored_hash: str) -> bool:
    try:
        salt, key = stored_hash.split('$')
        hash_obj = hashlib.pbkdf2_hmac(
            'sha256',
            pin.encode('utf-8'),
            salt.encode('utf-8'),
            100000
        )
        return hash_obj.hex() == key
    except (ValueError, AttributeError):
        return False


def validate_pin_strength(pin: str) -> tuple[bool, Optional[str]]:
    if len(pin) < 4:
        return False, "PIN must be at least 4 digits"

    if not pin.isdigit():
        return False, "PIN must contain only digits"

    return True, None


def validate_password_strength(password: str) -> tuple[bool, Optional[str]]:
    if len(password) < 8:
        return False, "Password must be at least 8 characters"

    has_digit = bool(re.search(r'\d', password))
    has_upper = bool(re.search(r'[A-Z]', password))
    has_lower = bool(re.search(r'[a-z]', password))
    has_special = bool(re.search(r'[!@#$%^&_*]', password))

    if not (has_digit and has_upper and has_lower and has_special):
        return False, "Password must contain uppercase, lowercase, digit, and special character"

    return True, None