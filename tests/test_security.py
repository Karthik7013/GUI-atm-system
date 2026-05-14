import pytest
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils.security import hash_pin, verify_pin, validate_pin_strength, validate_password_strength


class TestPinHashing:
    def test_hash_pin_returns_string(self):
        result = hash_pin("1234")
        assert isinstance(result, str)
        assert "$" in result

    def test_same_pin_different_hash(self):
        hash1 = hash_pin("1234")
        hash2 = hash_pin("1234")
        assert hash1 != hash2

    def test_verify_correct_pin(self):
        pin = "123456"
        hashed = hash_pin(pin)
        assert verify_pin(pin, hashed) is True

    def test_verify_wrong_pin(self):
        pin = "123456"
        hashed = hash_pin(pin)
        assert verify_pin("000000", hashed) is False

    def test_verify_invalid_hash(self):
        assert verify_pin("1234", "invalid") is False


class TestPinStrengthValidation:
    def test_valid_4_digit_pin(self):
        is_valid, error = validate_pin_strength("1234")
        assert is_valid is True
        assert error is None

    def test_valid_6_digit_pin(self):
        is_valid, error = validate_pin_strength("123456")
        assert is_valid is True

    def test_pin_too_short(self):
        is_valid, error = validate_pin_strength("123")
        assert is_valid is False
        assert "4" in error

    def test_pin_with_letters(self):
        is_valid, error = validate_pin_strength("12ab")
        assert is_valid is False
        assert "digits" in error.lower()


class TestPasswordStrengthValidation:
    def test_valid_strong_password(self):
        is_valid, error = validate_password_strength("Password1!")
        assert is_valid is True

    def test_password_too_short(self):
        is_valid, error = validate_password_strength("Pass1!")
        assert is_valid is False
        assert "8" in error

    def test_password_no_uppercase(self):
        is_valid, error = validate_password_strength("password1!")
        assert is_valid is False

    def test_password_no_lowercase(self):
        is_valid, error = validate_password_strength("PASSWORD1!")
        assert is_valid is False

    def test_password_no_digit(self):
        is_valid, error = validate_password_strength("Password!!"
)
        assert is_valid is False

    def test_password_no_special(self):
        is_valid, error = validate_password_strength("Password1"
)
        assert is_valid is False