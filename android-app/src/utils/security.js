function simpleHash(str) {
  let hash = 0;
  for (let i = 0; i < str.length; i++) {
    const char = str.charCodeAt(i);
    hash = (hash << 5) - hash + char;
    hash = hash & hash;
  }
  return 'hash_' + Math.abs(hash).toString(16);
}

async function hashPin(pin) {
  return simpleHash(pin);
}

function verifyPin(pin, pinHash) {
  return Promise.resolve(simpleHash(pin) === pinHash);
}

function validatePin(pin) {
  if (!pin || pin.length < 4 || pin.length > 6) {
    return { valid: false, error: 'PIN must be 4 to 6 digits' };
  }
  if (!/^\d+$/.test(pin)) {
    return { valid: false, error: 'PIN must contain only digits' };
  }
  return { valid: true, error: null };
}

function validateAccountNumber(accountNumber) {
  if (!accountNumber || accountNumber.trim().length === 0) {
    return { valid: false, error: 'Account number is required' };
  }
  if (!/^\d+$/.test(accountNumber.trim())) {
    return { valid: false, error: 'Account number must contain only digits' };
  }
  return { valid: true, error: null };
}

function validateName(name) {
  if (!name || name.trim().length === 0) {
    return { valid: false, error: 'Name is required' };
  }
  if (name.trim().length < 2) {
    return { valid: false, error: 'Name must be at least 2 characters' };
  }
  if (!/^[a-zA-Z\s]+$/.test(name.trim())) {
    return { valid: false, error: 'Name must contain only letters and spaces' };
  }
  return { valid: true, error: null };
}

function validateAmount(amount) {
  const num = parseInt(amount, 10);
  if (!amount || isNaN(num)) {
    return { valid: false, error: 'Amount must be a valid number' };
  }
  if (num <= 0) {
    return { valid: false, error: 'Amount must be greater than zero' };
  }
  if (num % 100 !== 0) {
    return { valid: false, error: 'Amount must be in multiples of 100' };
  }
  return { valid: true, error: null };
}

export { hashPin, verifyPin, validatePin, validateAccountNumber, validateName, validateAmount };