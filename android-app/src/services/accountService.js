import { getDb, executeQuery, executeReadQuery } from '../database/database';
import {
  validateAccountNumber,
  validateAmount,
} from '../utils/validators';
import {
  ValidationError,
  InvalidAccountError,
  InsufficientFundsError,
} from '../utils/exceptions';

class AccountService {
  constructor() {
    this.db = getDb();
  }

  async getBalance(userId) {
    const users = await executeReadQuery(
      'SELECT balance FROM users WHERE id = ?',
      [userId]
    );

    if (users.length === 0) {
      throw new InvalidAccountError('Account not found');
    }

    return users[0].balance;
  }

  async getAccountInfo(userId) {
    const users = await executeReadQuery(
      'SELECT account_number, name, balance, created_at FROM users WHERE id = ?',
      [userId]
    );

    if (users.length === 0) {
      throw new InvalidAccountError('Account not found');
    }

    return {
      account_number: users[0].account_number,
      name: users[0].name,
      balance: users[0].balance,
      created_at: users[0].created_at,
    };
  }

  async getTransactionHistory(userId, limit = 10) {
    const rows = await executeReadQuery(
      'SELECT id, type, amount, description, related_account, timestamp FROM transactions WHERE user_id = ? ORDER BY timestamp DESC LIMIT ?',
      [userId, limit]
    );

    return rows;
  }
}

export default AccountService;