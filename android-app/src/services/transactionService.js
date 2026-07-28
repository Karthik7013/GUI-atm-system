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

class TransactionService {
  constructor() {
    this.db = getDb();
  }

  async deposit(userId, amount) {
    const { valid, error } = validateAmount(String(amount));
    if (!valid) throw new ValidationError(error);

    const users = await executeReadQuery(
      'SELECT * FROM users WHERE id = ?',
      [userId]
    );

    if (users.length === 0) {
      throw new InvalidAccountError('User not found');
    }

    const user = users[0];
    const newBalance = user.balance + amount;

    await executeQuery(
      'UPDATE users SET balance = ?, updated_at = ? WHERE id = ?',
      [newBalance, new Date().toISOString(), userId]
    );

    await executeQuery(
      'INSERT INTO transactions (user_id, type, amount, description) VALUES (?, ?, ?, ?)',
      [userId, 'deposit', amount, `Cash deposit of ${amount} ₹`]
    );

    return {
      success: true,
      new_balance: newBalance,
      amount: amount,
    };
  }

  async withdraw(userId, amount) {
    const { valid, error } = validateAmount(String(amount));
    if (!valid) throw new ValidationError(error);

    const users = await executeReadQuery(
      'SELECT * FROM users WHERE id = ?',
      [userId]
    );

    if (users.length === 0) {
      throw new InvalidAccountError('User not found');
    }

    const user = users[0];

    if (user.balance < amount) {
      throw new InsufficientFundsError(
        `Insufficient balance. Available: ${user.balance} ₹`
      );
    }

    const newBalance = user.balance - amount;

    await executeQuery(
      'UPDATE users SET balance = ?, updated_at = ? WHERE id = ?',
      [newBalance, new Date().toISOString(), userId]
    );

    await executeQuery(
      'INSERT INTO transactions (user_id, type, amount, description) VALUES (?, ?, ?, ?)',
      [userId, 'withdraw', amount, `Cash withdrawal of ${amount} ₹`]
    );

    return {
      success: true,
      new_balance: newBalance,
      amount: amount,
    };
  }

  async transfer(fromUserId, toAccountNumber, amount) {
    const { valid, error } = validateAmount(String(amount));
    if (!valid) throw new ValidationError(error);

    const { valid: accValid, error: accError } = validateAccountNumber(toAccountNumber);
    if (!accValid) throw new ValidationError(accError);

    const fromUsers = await executeReadQuery(
      'SELECT * FROM users WHERE id = ?',
      [fromUserId]
    );

    if (fromUsers.length === 0) {
      throw new InvalidAccountError('Sender account not found');
    }

    const fromUser = fromUsers[0];

    if (fromUser.account_number === toAccountNumber.trim()) {
      throw new ValidationError('Cannot transfer to your own account');
    }

    if (fromUser.balance < amount) {
      throw new InsufficientFundsError(
        `Insufficient balance. Available: ${fromUser.balance} ₹`
      );
    }

    const toUsers = await executeReadQuery(
      'SELECT * FROM users WHERE account_number = ?',
      [toAccountNumber.trim()]
    );

    if (toUsers.length === 0) {
      throw new InvalidAccountError('Recipient account not found');
    }

    const toUser = toUsers[0];
    const fromNewBalance = fromUser.balance - amount;
    const toNewBalance = toUser.balance + amount;

    await executeQuery(
      'UPDATE users SET balance = ?, updated_at = ? WHERE id = ?',
      [fromNewBalance, new Date().toISOString(), fromUserId]
    );

    await executeQuery(
      'UPDATE users SET balance = ?, updated_at = ? WHERE id = ?',
      [toNewBalance, new Date().toISOString(), toUser.id]
    );

    await executeQuery(
      'INSERT INTO transactions (user_id, type, amount, description, related_account) VALUES (?, ?, ?, ?, ?)',
      [fromUserId, 'transfer_out', amount, `Transfer to ${toAccountNumber}`, toAccountNumber]
    );

    await executeQuery(
      'INSERT INTO transactions (user_id, type, amount, description, related_account) VALUES (?, ?, ?, ?, ?)',
      [toUser.id, 'transfer_in', amount, `Transfer from ${fromUser.account_number}`, fromUser.account_number]
    );

    return {
      success: true,
      new_balance: fromNewBalance,
      amount: amount,
      recipient: toUser.name,
    };
  }
}

export default TransactionService;