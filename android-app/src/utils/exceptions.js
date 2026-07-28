class AtmException extends Error {
  constructor(message) {
    super(message);
    this.name = 'AtmException';
  }
}

class ValidationError extends AtmException {
  constructor(message) {
    super(message);
    this.name = 'ValidationError';
  }
}

class AuthenticationError extends AtmException {
  constructor(message) {
    super(message);
    this.name = 'AuthenticationError';
  }
}

class InvalidAccountError extends AtmException {
  constructor(message) {
    super(message);
    this.name = 'InvalidAccountError';
  }
}

class InsufficientFundsError extends AtmException {
  constructor(message) {
    super(message);
    this.name = 'InsufficientFundsError';
  }
}

class DuplicateAccountError extends AtmException {
  constructor(message) {
    super(message);
    this.name = 'DuplicateAccountError';
  }
}

class DatabaseError extends AtmException {
  constructor(message) {
    super(message);
    this.name = 'DatabaseError';
  }
}

export {
  AtmException,
  ValidationError,
  AuthenticationError,
  InvalidAccountError,
  InsufficientFundsError,
  DuplicateAccountError,
  DatabaseError,
};