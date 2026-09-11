from typing import Any, Optional

class AppException(Exception):
    """Base exception for application errors"""
    def __init__(self, message: str, status_code: int = 400, details: Optional[Any] = None):
        super().__init__(message)
        self.message = message
        self.status_code = status_code
        self.details = details

class UserAlreadyExistsException(AppException):
    def __init__(self, message: str = "Email is already registered and verified. Please login instead."):
        super().__init__(message=message, status_code=400)

class UserNotFoundException(AppException):
    def __init__(self, message: str = "User account not found."):
        super().__init__(message=message, status_code=404)

class InvalidCredentialsException(AppException):
    def __init__(self, message: str = "Incorrect email or password"):
        super().__init__(message=message, status_code=401)

class EmailNotVerifiedException(AppException):
    def __init__(self, message: str = "Please verify your email before logging in. A verification code was sent to your email."):
        super().__init__(message=message, status_code=403)

class InvalidOTPException(AppException):
    def __init__(self, message: str = "Invalid verification code. Please check your email and try again."):
        super().__init__(message=message, status_code=400)

class OTPExpiredException(AppException):
    def __init__(self, message: str = "Verification code has expired. Please request a new code."):
        super().__init__(message=message, status_code=400)

class AudioGenerationException(AppException):
    def __init__(self, message: str = "Failed to generate audio"):
        super().__init__(message=message, status_code=500)
