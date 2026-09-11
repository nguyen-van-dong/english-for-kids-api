from fastapi import APIRouter, Depends
from typing import Dict, Any

from app.api.deps import get_auth_service
from app.services.auth_service import AuthService
from app.schemas.user import (
    UserRegister,
    UserLogin,
    Token,
    VerifyEmailRequest,
    ResendVerificationRequest,
    RegisterResponse,
)

router = APIRouter()

@router.post("/register", response_model=RegisterResponse)
def register(
    user_in: UserRegister,
    auth_service: AuthService = Depends(get_auth_service)
):
    """
    Register a new user, generate 6-digit OTP, and trigger Celery task to send verification email.
    """
    return auth_service.register(user_in)

@router.post("/verify-email", response_model=Token)
def verify_email(
    verify_in: VerifyEmailRequest,
    auth_service: AuthService = Depends(get_auth_service)
):
    """
    Verify user email with 6-digit OTP code and return active JWT access token.
    """
    return auth_service.verify_email(verify_in)

@router.post("/resend-verification")
def resend_verification(
    resend_in: ResendVerificationRequest,
    auth_service: AuthService = Depends(get_auth_service)
):
    """
    Generate new OTP code and dispatch Celery email task.
    """
    return auth_service.resend_verification(resend_in)

@router.post("/login", response_model=Token)
def login(
    user_in: UserLogin,
    auth_service: AuthService = Depends(get_auth_service)
):
    """
    Authenticate user. Requires verified email address.
    """
    return auth_service.login(user_in)
