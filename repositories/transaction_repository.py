from typing import List, Dict, Any, Optional
from datetime import datetime
import sqlite3
from models import get_db
from utils import DatabaseError


class TransactionRepository:
    def __init__(self):
        self.db = get_db()

    def create_transaction(
        self,
        user_id: int,
        transaction_type: str,
        amount: float,
        description: str = "",
        related_account: Optional[str] = None
    ) -> int:
        try:
            with self.db.transaction() as conn:
                cursor = conn.cursor()
                cursor.execute(
                    """INSERT INTO transactions
                    (user_id, type, amount, description, related_account)
                    VALUES (?, ?, ?, ?, ?)""",
                    (user_id, transaction_type, amount, description, related_account)
                )
                return cursor.lastrowid
        except Exception as e:
            raise DatabaseError(f"Failed to create transaction: {str(e)}")

    def get_user_transactions(self, user_id: int, limit: int = 10) -> List[Dict[str, Any]]:
        try:
            with self.db.get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute(
                    """SELECT id, type, amount, description, related_account, timestamp
                    FROM transactions WHERE user_id = ?
                    ORDER BY timestamp DESC LIMIT ?""",
                    (user_id, limit)
                )
                return [dict(row) for row in cursor.fetchall()]
        except Exception as e:
            raise DatabaseError(f"Failed to fetch transactions: {str(e)}")

    def get_transaction_by_id(self, transaction_id: int) -> Optional[Dict[str, Any]]:
        try:
            with self.db.get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute(
                    "SELECT * FROM transactions WHERE id = ?",
                    (transaction_id,)
                )
                row = cursor.fetchone()
                if row:
                    return dict(row)
                return None
        except Exception as e:
            raise DatabaseError(f"Failed to fetch transaction: {str(e)}")