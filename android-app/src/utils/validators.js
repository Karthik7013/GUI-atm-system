function validateAccountNumber(accountNumber) {
  if (!accountNumber || accountNumber.trim().length === 0) {
    return { valid: false, error: 'Account number is required' };
  }
  if (!/^\d+$/.test(accountNumber.trim())) {
    return { valid: false, error: 'Account number must contain only digits' };
  }
  return { valid: true, error: null };
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

function validateName(name) {
  if (!name || name.trim().length === 0) {
    return { valid: false, error: 'Name is required' };
  }
  if (name.trim().length < 2) {
    return { valid: false, error: 'Name must be at least 2 characters' };
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

export { validateAccountNumber, validatePin, validateName, validateAmount };