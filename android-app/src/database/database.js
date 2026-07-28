import * as SQLite from 'expo-sqlite';

const db = SQLite.openDatabase('sbi_atm.db');

function initDatabase() {
  db.transaction((tx) => {
    tx.executeSql(
      `CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        account_number TEXT UNIQUE NOT NULL,
        name TEXT NOT NULL,
        pin_hash TEXT NOT NULL,
        balance REAL DEFAULT 0.0,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
      );`
    );

    tx.executeSql(
      `CREATE TABLE IF NOT EXISTS transactions (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER NOT NULL,
        type TEXT NOT NULL CHECK(type IN ('deposit', 'withdraw', 'transfer_in', 'transfer_out')),
        amount REAL NOT NULL,
        description TEXT,
        related_account TEXT,
        timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (user_id) REFERENCES users(id)
      );`
    );

    tx.executeSql(
      `CREATE INDEX IF NOT EXISTS idx_users_account ON users(account_number);`
    );

    tx.executeSql(
      `CREATE INDEX IF NOT EXISTS idx_transactions_user ON transactions(user_id, timestamp);`
    );
  });
}

function getDb() {
  return db;
}

function executeQuery(sql, params = []) {
  return new Promise((resolve, reject) => {
    db.transaction((tx) => {
      tx.executeSql(sql, params, (_, result) => {
        resolve(result);
      }, (_, error) => {
        reject(error);
      });
    });
  });
}

function executeReadQuery(sql, params = []) {
  return new Promise((resolve, reject) => {
    db.transaction((tx) => {
      tx.executeSql(sql, params, (_, result) => {
        const rows = [];
        for (let i = 0; i < result.rows.length; i++) {
          rows.push(result.rows.item(i));
        }
        resolve(rows);
      }, (_, error) => {
        reject(error);
      });
    });
  });
}

export { initDatabase, getDb, executeQuery, executeReadQuery };