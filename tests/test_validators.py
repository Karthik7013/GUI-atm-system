import pytest
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils.validators import Validator
from utils.exceptions import ValidationError


class TestAccountNumberValidator:
    def test_valid_account_number(self):
        is_valid, error = Validator.validate_account_number("123456")
        assert is_valid is True
        assert error is None

    def test_valid_12_digit_account(self):
        is_valid, error = Validator.validate_account_number("123456789012")
        assert is_valid is True

    def test_account_number_too_short(self):
        is_valid, error = Validator.validate_account_number("12345")
        assert is_valid is False
        assert "6" in error

    def test_account_number_too_long(self):
        is_valid, error = Validator.validate_account_number("1234567890123")
        assert is_valid is False
        assert "12" in error

    def test_account_number_with_letters(self):
        is_valid, error = Validator.validate_account_number("12345ab")
        assert is_valid is False
        assert "digits" in error.lower()

    def test_empty_account_number(self):
        is_valid, error = Validator.validate_account_number("")
        assert is_valid is False


class TestAmountValidator:
    def test_valid_amount(self):
        is_valid, error = Validator.validate_amount("100")
        assert is_valid is True

    def test_valid_500_amount(self):
        is_valid, error = Validator.validate_amount("500")
        assert is_valid is True

    def test_valid_2000_amount(self):
        is_valid, error = Validator.validate_amount("2000")
        assert is_valid is True

    def test_amount_not_multiple_of_100(self):
        is_valid, error = Validator.validate_amount("150")
        assert is_valid is False
        assert "100" in error

    def test_amount_too_small(self):
        is_valid, error = Validator.validate_amount("50")
        assert is_valid is False

    def test_amount_with_letters(self):
        is_valid, error = Validator.validate_amount("100abc")
        assert is_valid is False


class TestNameValidator:
    def test_valid_name(self):
        is_valid, error = Validator.validate_name("John Doe")
        assert is_valid is True

    def test_name_with_spaces(self):
        is_valid, error = Validator.validate_name("John Michael")
        assert is_valid is True

    def test_name_too_short(self):
        is_valid, error = Validator.validate_name("J")
        assert is_valid is False

    def test_name_with_numbers(self):
        is_valid, error = Validator.validate_name("John123")
        assert is_valid is False

    def test_name_with_special_chars(self):
        is_valid, error = Validator.validate_name("John@Doe")
        assert is_valid is False

    def test_empty_name(self):
        is_valid, error = Validator.validate_name("")
        assert is_valid is False


class TestPinValidator:
    def test_valid_4_digit_pin(self):
        is_valid, error = Validator.validate_pin("1234")
        assert is_valid is True

    def test_valid_6_digit_pin(self):
        is_valid, error = Validator.validate_pin("123456")
        assert is_valid is True

    def test_pin_too_short(self):
        is_valid, error = Validator.validate_pin("123")
        assert is_valid is False

    def test_pin_with_letters(self):
        is_valid, error = Validator.validate_pin("12ab")
        assert is_valid is False

    def test_empty_pin(self):
        is_valid, error = Validator.validate_pin("")
        assert is_valid is False