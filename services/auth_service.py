from typing import Dict, Any, Optional
from datetime import datetime
from repositories import UserRepository, TransactionRepository
from utils import (
    Validator,
    AuthenticationError,
    ValidationError,
    DuplicateAccountError,
    audit_logger
)


class AuthService:
    def __init__(self):
        self.user_repo = UserRepository()
        self.transaction_repo = TransactionRepository()

    def login(self, account_number: str, pin: str) -> Dict[str, Any]:
        is_valid, error = Validator.validate_account_number(account_number)
        if not is_valid:
            raise ValidationError(error)

        is_valid, error = Validator.validate_pin(pin)
        if not is_valid:
            raise ValidationError(error)

        user = self.user_repo.verify_credentials(account_number, pin)

        if not user:
            audit_logger.warning(f"Failed login attempt for account: {account_number}")
            raise AuthenticationError("Invalid account number or PIN")

        audit_logger.info(f"User logged in successfully: {account_number}")

        return {
            'id': user['id'],
            'account_number': user['account_number'],
            'name': user['name'],
            'balance': user['balance']
        }

    def register(
        self,
        name: str,
        pin: str,
        confirm_pin: str,
        initial_balance: float
    ) -> Dict[str, Any]:
        is_valid, error = Validator.validate_name(name)
        if not is_valid:
            raise ValidationError(error)

        is_valid, error = Validator.validate_pin(pin)
        if not is_valid:
            raise ValidationError(error)

        if pin != confirm_pin:
            raise ValidationError("PINs do not match")

        if initial_balance < 0:
            raise ValidationError("Initial balance cannot be negative")

        account_number = self.user_repo.get_next_account_number()

        user_id = self.user_repo.create_user(
            account_number=account_number,
            name=name.strip(),
            pin=pin,
            initial_balance=initial_balance
        )

        self.transaction_repo.create_transaction(
            user_id=user_id,
            transaction_type='deposit',
            amount=initial_balance,
            description='Initial deposit'
        )

        audit_logger.info(f"New user registered: {account_number}")

        return {
            'account_number': account_number,
            'name': name,
            'balance': initial_balance
        }

    def change_pin(self, user_id: int, old_pin: str, new_pin: str) -> bool:
        is_valid, error = Validator.validate_pin(old_pin)
        if not is_valid:
            raise ValidationError(error)

        is_valid, error = Validator.validate_pin(new_pin)
        if not is_valid:
            raise ValidationError(error)

        user = self.user_repo.get_by_id(user_id)
        if not user:
            raise ValidationError("User not found")

        from utils.security import verify_pin
        if not verify_pin(old_pin, user['pin_hash']):
            audit_logger.warning(f"Failed PIN change attempt for user_id: {user_id}")
            raise AuthenticationError("Current PIN is incorrect")

        self.user_repo.update_pin(user_id, new_pin)

        audit_logger.info(f"PIN changed successfully for user_id: {user_id}")
        return True