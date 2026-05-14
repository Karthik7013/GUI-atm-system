from typing import Dict, Any
from repositories import UserRepository, TransactionRepository
from utils import (
    Validator,
    ValidationError,
    InvalidAccountError,
    InsufficientFundsError,
    audit_logger
)


class TransactionService:
    def __init__(self):
        self.user_repo = UserRepository()
        self.transaction_repo = TransactionRepository()

    def deposit(self, user_id: int, amount: int) -> Dict[str, Any]:
        is_valid, error = Validator.validate_amount(str(amount))
        if not is_valid:
            raise ValidationError(error)

        user = self.user_repo.get_by_id(user_id)
        if not user:
            raise InvalidAccountError("User not found")

        new_balance = user['balance'] + amount

        self.user_repo.update_balance(user_id, new_balance)

        self.transaction_repo.create_transaction(
            user_id=user_id,
            transaction_type='deposit',
            amount=amount,
            description=f"Cash deposit of {amount} ₹"
        )

        audit_logger.info(f"Deposit: {amount} ₹ to user_id: {user_id}")

        return {
            'success': True,
            'new_balance': new_balance,
            'amount': amount
        }

    def withdraw(self, user_id: int, amount: int) -> Dict[str, Any]:
        is_valid, error = Validator.validate_amount(str(amount))
        if not is_valid:
            raise ValidationError(error)

        user = self.user_repo.get_by_id(user_id)
        if not user:
            raise InvalidAccountError("User not found")

        if user['balance'] < amount:
            raise InsufficientFundsError(
                f"Insufficient balance. Available: {user['balance']} ₹"
            )

        new_balance = user['balance'] - amount

        self.user_repo.update_balance(user_id, new_balance)

        self.transaction_repo.create_transaction(
            user_id=user_id,
            transaction_type='withdraw',
            amount=amount,
            description=f"Cash withdrawal of {amount} ₹"
        )

        audit_logger.info(f"Withdrawal: {amount} ₹ from user_id: {user_id}")

        return {
            'success': True,
            'new_balance': new_balance,
            'amount': amount
        }

    def transfer(
        self,
        from_user_id: int,
        to_account_number: str,
        amount: int
    ) -> Dict[str, Any]:
        is_valid, error = Validator.validate_amount(str(amount))
        if not is_valid:
            raise ValidationError(error)

        is_valid, error = Validator.validate_account_number(to_account_number)
        if not is_valid:
            raise ValidationError(error)

        from_user = self.user_repo.get_by_id(from_user_id)
        if not from_user:
            raise InvalidAccountError("Sender account not found")

        if from_user['account_number'] == to_account_number:
            raise ValidationError("Cannot transfer to your own account")

        if from_user['balance'] < amount:
            raise InsufficientFundsError(
                f"Insufficient balance. Available: {from_user['balance']} ₹"
            )

        to_user = self.user_repo.get_by_account_number(to_account_number)
        if not to_user:
            raise InvalidAccountError("Recipient account not found")

        from_new_balance = from_user['balance'] - amount
        to_new_balance = to_user['balance'] + amount

        self.user_repo.update_balance(from_user_id, from_new_balance)
        self.user_repo.update_balance(to_user['id'], to_new_balance)

        self.transaction_repo.create_transaction(
            user_id=from_user_id,
            transaction_type='transfer_out',
            amount=amount,
            description=f"Transfer to {to_account_number}",
            related_account=to_account_number
        )

        self.transaction_repo.create_transaction(
            user_id=to_user['id'],
            transaction_type='transfer_in',
            amount=amount,
            description=f"Transfer from {from_user['account_number']}",
            related_account=from_user['account_number']
        )

        audit_logger.info(
            f"Transfer: {amount} ₹ from {from_user['account_number']} to {to_account_number}"
        )

        return {
            'success': True,
            'new_balance': from_new_balance,
            'amount': amount,
            'recipient': to_user['name']
        }