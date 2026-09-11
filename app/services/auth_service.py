import secrets
import logging
from datetime import datetime, timedelta, timezone
from typing import Dict, Any

from app.core.config import settings
from app.core.security import get_password_hash, verify_password, create_access_token
from app.core.exceptions import (
    UserAlreadyExistsException,
    UserNotFoundException,
    InvalidCredentialsException,
    EmailNotVerifiedException,
    InvalidOTPException,
    OTPExpiredException,
)
from app.repositories.user_repository import UserRepository
from app.schemas.user import (
    UserRegister,
    UserLogin,
    VerifyEmailRequest,
    ResendVerificationRequest,
    RegisterResponse,
)
from app.tasks.email import send_verification_email_task

logger = logging.getLogger(__name__)

class AuthService:
    def __init__(self, user_repo: UserRepository):
        self.user_repo = user_repo

    @staticmethod
    def generate_otp_code() -> str:
        """Generate a secure 6-digit numeric OTP code"""
        return f"{secrets.randbelow(900000) + 100000}"

    def _dispatch_verification_email(self, to_email: str, child_name: str, verification_code: str):
        """Safely dispatch Celery task, falling back to direct invocation if broker is offline."""
        try:
            send_verification_email_task.delay(
                to_email=to_email,
                child_name=child_name,
                verification_code=verification_code,
            )
        except Exception as e:
            logger.warning(f"Celery broker unavailable, running email task directly: {e}")
            try:
                # Direct call fallback
                send_verification_email_task(
                    to_email=to_email,
                    child_name=child_name,
                    verification_code=verification_code,
                )
            except Exception as direct_err:
                logger.error(f"Failed to execute email task directly: {direct_err}")

    def register(self, user_in: UserRegister) -> RegisterResponse:
        """
        Register a new user or refresh unverified account OTP, dispatching Celery email task.
        """
        normalized_email = user_in.email.strip().lower()
        existing_user = self.user_repo.get_by_email(normalized_email)

        if existing_user:
            if not existing_user.is_verified:
                code = self.generate_otp_code()
                expires_at = datetime.now(timezone.utc) + timedelta(
                    minutes=settings.EMAIL_VERIFICATION_EXPIRE_MINUTES
                )
                self.user_repo.update_verification_code(existing_user, code, expires_at)

                # Dispatch email task
                self._dispatch_verification_email(
                    to_email=existing_user.email,
                    child_name=existing_user.child_name,
                    verification_code=code,
                )

                return RegisterResponse(
                    message="Account already registered but unverified. A new verification code has been sent to your email.",
                    email=existing_user.email,
                    child_name=existing_user.child_name,
                    is_verified=False,
                )

            raise UserAlreadyExistsException()

        # Generate OTP
        code = self.generate_otp_code()
        expires_at = datetime.now(timezone.utc) + timedelta(
            minutes=settings.EMAIL_VERIFICATION_EXPIRE_MINUTES
        )

        # Create user
        new_user = self.user_repo.create_user(
            email=normalized_email,
            hashed_password=get_password_hash(user_in.password),
            parent_name=user_in.parent_name or "",
            child_name=user_in.child_name,
            child_age=user_in.child_age,
            avatar=user_in.avatar or "🦁",
            verification_code=code,
            verification_code_expires_at=expires_at,
        )

        # Dispatch email task
        self._dispatch_verification_email(
            to_email=new_user.email,
            child_name=new_user.child_name,
            verification_code=code,
        )

        return RegisterResponse(
            message=f"Registration successful! Please check {new_user.email} for your 6-digit verification code.",
            email=new_user.email,
            child_name=new_user.child_name,
            is_verified=False,
        )

    def verify_email(self, verify_in: VerifyEmailRequest) -> Dict[str, Any]:
        """
        Validate OTP, mark user as verified, and issue access token.
        """
        normalized_email = verify_in.email.strip().lower()
        user = self.user_repo.get_by_email(normalized_email)
        if not user:
            raise UserNotFoundException()

        if user.is_verified:
            access_token = create_access_token(subject=user.id)
            return {
                "access_token": access_token,
                "token_type": "bearer",
                "user": user
            }

        # Check OTP match
        if not user.verification_code or user.verification_code != verify_in.code.strip():
            raise InvalidOTPException()

        # Check expiration
        now = datetime.now(timezone.utc)
        if user.verification_code_expires_at:
            expires_at = user.verification_code_expires_at
            if expires_at.tzinfo is None:
                expires_at = expires_at.replace(tzinfo=timezone.utc)
            if now > expires_at:
                raise OTPExpiredException()

        # Mark verified
        user = self.user_repo.mark_email_verified(user)
        access_token = create_access_token(subject=user.id)
        return {
            "access_token": access_token,
            "token_type": "bearer",
            "user": user
        }

    def resend_verification(self, resend_in: ResendVerificationRequest) -> Dict[str, Any]:
        """
        Generate a fresh OTP code and dispatch email task.
        """
        normalized_email = resend_in.email.strip().lower()
        user = self.user_repo.get_by_email(normalized_email)
        if not user:
            raise UserNotFoundException()

        if user.is_verified:
            return {
                "success": True,
                "message": "Email is already verified. You can log in directly."
            }

        code = self.generate_otp_code()
        expires_at = datetime.now(timezone.utc) + timedelta(
            minutes=settings.EMAIL_VERIFICATION_EXPIRE_MINUTES
        )
        self.user_repo.update_verification_code(user, code, expires_at)

        self._dispatch_verification_email(
            to_email=user.email,
            child_name=user.child_name,
            verification_code=code,
        )

        return {
            "success": True,
            "message": f"A new 6-digit verification code has been sent to {user.email}."
        }

    def login(self, user_in: UserLogin) -> Dict[str, Any]:
        """
        Authenticate credentials and verify email status.
        """
        normalized_email = user_in.email.strip().lower()
        user = self.user_repo.get_by_email(normalized_email)
        if not user or not verify_password(user_in.password, user.hashed_password):
            raise InvalidCredentialsException()

        if not user.is_verified:
            raise EmailNotVerifiedException()

        access_token = create_access_token(subject=user.id)
        return {
            "access_token": access_token,
            "token_type": "bearer",
            "user": user
        }
