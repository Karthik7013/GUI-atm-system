from typing import Dict, Any
from datetime import datetime
from repositories import UserRepository, TransactionRepository
from utils import (
    InvalidAccountError,
    audit_logger
)


class AccountService:
    def __init__(self):
        self.user_repo = UserRepository()
        self.transaction_repo = TransactionRepository()

    def get_balance(self, user_id: int) -> float:
        balance = self.user_repo.get_balance(user_id)
        audit_logger.info(f"Balance checked for user_id: {user_id}")
        return balance

    def get_account_info(self, user_id: int) -> Dict[str, Any]:
        user = self.user_repo.get_by_id(user_id)
        if not user:
            raise InvalidAccountError("Account not found")

        return {
            'account_number': user['account_number'],
            'name': user['name'],
            'balance': user['balance'],
            'created_at': user['created_at']
        }

    def get_transaction_history(self, user_id: int, limit: int = 10):
        transactions = self.transaction_repo.get_user_transactions(user_id, limit)
        return transactions