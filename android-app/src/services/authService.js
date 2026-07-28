import { getDb, executeQuery, executeReadQuery } from '../database/database';
import { hashPin } from '../utils/security';
import {
  validateAccountNumber,
  validatePin,
  validateName,
  validateAmount,
} from '../utils/validators';
import {
  ValidationError,
  AuthenticationError,
  InvalidAccountError,
  DuplicateAccountError,
  InsufficientFundsError,
} from '../utils/exceptions';

class AuthService {
  constructor() {
    this.db = getDb();
  }

  async login(accountNumber, pin) {
    const { valid, error } = validateAccountNumber(accountNumber);
    if (!valid) throw new ValidationError(error);

    const { valid: pinValid, error: pinError } = validatePin(pin);
    if (!pinValid) throw new ValidationError(pinError);

    const users = await executeReadQuery(
      'SELECT * FROM users WHERE account_number = ?',
      [accountNumber.trim()]
    );

    if (users.length === 0) {
      throw new AuthenticationError('Invalid account number or PIN');
    }

    const user = users[0];
    const pinMatches = await verifyPin(pin, user.pin_hash);

    if (!pinMatches) {
      throw new AuthenticationError('Invalid account number or PIN');
    }

    return {
      id: user.id,
      account_number: user.account_number,
      name: user.name,
      balance: user.balance,
    };
  }

  async register(name, pin, confirmPin, initialBalance) {
    const { valid, error } = validateName(name);
    if (!valid) throw new ValidationError(error);

    const { valid: pinValid, error: pinError } = validatePin(pin);
    if (!pinValid) throw new ValidationError(pinError);

    if (pin !== confirmPin) {
      throw new ValidationError('PINs do not match');
    }

    if (initialBalance < 0) {
      throw new ValidationError('Initial balance cannot be negative');
    }

    const accountNumber = await this._getNextAccountNumber();
    const pinHash = await hashPin(pin);

    const result = await executeQuery(
      'INSERT INTO users (account_number, name, pin_hash, balance) VALUES (?, ?, ?, ?)',
      [accountNumber, name.trim(), pinHash, initialBalance]
    );

    const userId = result.insertId;

    await executeQuery(
      'INSERT INTO transactions (user_id, type, amount, description) VALUES (?, ?, ?, ?)',
      [userId, 'deposit', initialBalance, 'Initial deposit']
    );

    return {
      account_number: accountNumber,
      name: name,
      balance: initialBalance,
    };
  }

  async changePin(userId, oldPin, newPin) {
    const { valid, error } = validatePin(oldPin);
    if (!valid) throw new ValidationError(error);

    const { valid: newPinValid, error: newPinError } = validatePin(newPin);
    if (!newPinValid) throw new ValidationError(newPinError);

    const users = await executeReadQuery(
      'SELECT * FROM users WHERE id = ?',
      [userId]
    );

    if (users.length === 0) {
      throw new ValidationError('User not found');
    }

    const user = users[0];
    const oldPinMatches = await verifyPin(oldPin, user.pin_hash);

    if (!oldPinMatches) {
      throw new AuthenticationError('Current PIN is incorrect');
    }

    const newPinHash = await hashPin(newPin);

    await executeQuery(
      'UPDATE users SET pin_hash = ?, updated_at = ? WHERE id = ?',
      [newPinHash, new Date().toISOString(), userId]
    );

    return true;
  }

  async _getNextAccountNumber() {
    const rows = await executeReadQuery(
      'SELECT MAX(CAST(account_number AS INTEGER)) as max_num FROM users'
    );

    if (rows.length > 0 && rows[0].max_num) {
      return String(rows[0].max_num + 1);
    }

    return '100001';
  }
}

export default AuthService;