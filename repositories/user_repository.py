from typing import Optional, List, Dict, Any
from datetime import datetime
import sqlite3
from models import get_db
from utils import (
    InvalidAccountError,
    DuplicateAccountError,
    DatabaseError,
    hash_pin,
    verify_pin
)


class UserRepository:
    def __init__(self):
        self.db = get_db()

    def create_user(self, account_number: str, name: str, pin: str, initial_balance: float = 0.0) -> int:
        try:
            with self.db.transaction() as conn:
                cursor = conn.cursor()
                cursor.execute(
                    "INSERT INTO users (account_number, name, pin_hash, balance) VALUES (?, ?, ?, ?)",
                    (account_number, name, hash_pin(pin), initial_balance)
                )
                user_id = cursor.lastrowid
                return user_id
        except sqlite3.IntegrityError as e:
            if "UNIQUE constraint failed" in str(e):
                raise DuplicateAccountError("Account number already exists")
            raise DatabaseError(str(e))
        except Exception as e:
            raise DatabaseError(f"Failed to create user: {str(e)}")

    def get_by_account_number(self, account_number: str) -> Optional[Dict[str, Any]]:
        try:
            with self.db.get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute(
                    "SELECT id, account_number, name, pin_hash, balance, created_at FROM users WHERE account_number = ?",
                    (account_number,)
                )
                row = cursor.fetchone()
                if row:
                    return dict(row)
                return None
        except Exception as e:
            raise DatabaseError(f"Failed to fetch user: {str(e)}")

    def get_by_id(self, user_id: int) -> Optional[Dict[str, Any]]:
        try:
            with self.db.get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute(
                    "SELECT id, account_number, name, pin_hash, balance, created_at FROM users WHERE id = ?",
                    (user_id,)
                )
                row = cursor.fetchone()
                if row:
                    return dict(row)
                return None
        except Exception as e:
            raise DatabaseError(f"Failed to fetch user: {str(e)}")

    def verify_credentials(self, account_number: str, pin: str) -> Optional[Dict[str, Any]]:
        user = self.get_by_account_number(account_number)
        if user and verify_pin(pin, user['pin_hash']):
            return user
        return None

    def update_pin(self, user_id: int, new_pin: str) -> bool:
        try:
            with self.db.transaction() as conn:
                cursor = conn.cursor()
                cursor.execute(
                    "UPDATE users SET pin_hash = ?, updated_at = ? WHERE id = ?",
                    (hash_pin(new_pin), datetime.now().isoformat(), user_id)
                )
                return cursor.rowcount > 0
        except Exception as e:
            raise DatabaseError(f"Failed to update PIN: {str(e)}")

    def update_balance(self, user_id: int, new_balance: float) -> bool:
        try:
            with self.db.transaction() as conn:
                cursor = conn.cursor()
                cursor.execute(
                    "UPDATE users SET balance = ?, updated_at = ? WHERE id = ?",
                    (new_balance, datetime.now().isoformat(), user_id)
                )
                return cursor.rowcount > 0
        except Exception as e:
            raise DatabaseError(f"Failed to update balance: {str(e)}")

    def get_balance(self, user_id: int) -> float:
        user = self.get_by_id(user_id)
        if user:
            return user['balance']
        raise InvalidAccountError("User not found")

    def get_all_accounts(self) -> List[Dict[str, Any]]:
        try:
            with self.db.get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute("SELECT account_number FROM users")
                return [dict(row) for row in cursor.fetchall()]
        except Exception as e:
            raise DatabaseError(f"Failed to fetch accounts: {str(e)}")

    def get_next_account_number(self) -> str:
        try:
            with self.db.get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute("SELECT MAX(CAST(account_number AS INTEGER)) FROM users")
                result = cursor.fetchone()[0]
                if result:
                    return str(result + 1)
                return "100001"
        except Exception:
            return "100001"