class AtmException(Exception):
    def __init__(self, message: str, code: str = "ATM_ERROR"):
        self.message = message
        self.code = code
        super().__init__(self.message)


class AuthenticationError(AtmException):
    def __init__(self, message: str = "Authentication failed"):
        super().__init__(message, "AUTH_ERROR")


class InvalidAccountError(AtmException):
    def __init__(self, message: str = "Account not found"):
        super().__init__(message, "INVALID_ACCOUNT")


class InsufficientFundsError(AtmException):
    def __init__(self, message: str = "Insufficient balance"):
        super().__init__(message, "INSUFFICIENT_FUNDS")


class InvalidAmountError(AtmException):
    def __init__(self, message: str = "Invalid amount"):
        super().__init__(message, "INVALID_AMOUNT")


class ValidationError(AtmException):
    def __init__(self, message: str = "Validation failed"):
        super().__init__(message, "VALIDATION_ERROR")


class DatabaseError(AtmException):
    def __init__(self, message: str = "Database operation failed"):
        super().__init__(message, "DB_ERROR")


class DuplicateAccountError(AtmException):
    def __init__(self, message: str = "Account already exists"):
        super().__init__(message, "DUPLICATE_ACCOUNT")