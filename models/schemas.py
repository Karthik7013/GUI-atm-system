import sqlite3
from utils.security import hash_pin


def init_database(db_path: str) -> None:
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            account_number TEXT UNIQUE NOT NULL,
            name TEXT NOT NULL,
            pin_hash TEXT NOT NULL,
            balance REAL DEFAULT 0.0,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS transactions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            type TEXT NOT NULL CHECK(type IN ('deposit', 'withdraw', 'transfer_in', 'transfer_out')),
            amount REAL NOT NULL,
            description TEXT,
            related_account TEXT,
            timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users(id)
        )
    """)

    cursor.execute("""
        CREATE INDEX IF NOT EXISTS idx_users_account
        ON users(account_number)
    """)

    cursor.execute("""
        CREATE INDEX IF NOT EXISTS idx_transactions_user
        ON transactions(user_id, timestamp)
    """)

    _migrate_userdata(cursor, conn)

    conn.commit()
    conn.close()


def _migrate_userdata(cursor, conn) -> None:
    cursor.execute(
        "SELECT name FROM sqlite_master WHERE type='table' AND name='userdata'"
    )
    if not cursor.fetchone():
        return

    cursor.execute(
        "SELECT Account_no, Name, Pincode, balance FROM userdata"
    )
    rows = cursor.fetchall()

    for row in rows:
        account_no, name, pincode, balance = row
        try:
            cursor.execute(
                "INSERT OR IGNORE INTO users (account_number, name, pin_hash, balance) VALUES (?, ?, ?, ?)",
                (str(account_no), name, hash_pin(str(pincode)), balance or 0.0)
            )
        except sqlite3.IntegrityError:
            pass

    cursor.execute(
        "DROP TABLE IF EXISTS userdata"
    )