import secrets
from datetime import datetime, timedelta, timezone
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.user import User
from app.schemas.user import (
    UserRegister,
    UserLogin,
    Token,
    UserResponse,
    VerifyEmailRequest,
    ResendVerificationRequest,
    RegisterResponse,
)
from app.core.security import get_password_hash, verify_password, create_access_token
from app.core.config import settings
from app.tasks.email import send_verification_email_task

router = APIRouter()

def generate_otp_code() -> str:
    """Generate a secure 6-digit numeric OTP code"""
    return f"{secrets.randbelow(900000) + 100000}"

@router.post("/register", response_model=RegisterResponse)
def register(
    user_in: UserRegister,
    db: Session = Depends(get_db)
):
    """
    Register a new user, generate 6-digit OTP, and trigger Celery task to send verification email.
    """
    # Check if email exists
    existing_user = db.query(User).filter(User.email == user_in.email.lower()).first()
    if existing_user:
        if not existing_user.is_verified:
            # If exists but not verified, refresh code and resend email
            code = generate_otp_code()
            existing_user.verification_code = code
            existing_user.verification_code_expires_at = datetime.now(timezone.utc) + timedelta(
                minutes=settings.EMAIL_VERIFICATION_EXPIRE_MINUTES
            )
            db.commit()

            # Trigger Celery background task via Redis broker
            send_verification_email_task.delay(
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

        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email is already registered and verified. Please login instead."
        )

    # Generate 6-digit OTP code & expiration
    code = generate_otp_code()
    expires_at = datetime.now(timezone.utc) + timedelta(minutes=settings.EMAIL_VERIFICATION_EXPIRE_MINUTES)

    # Create new user with is_verified = False
    db_user = User(
        email=user_in.email.lower(),
        hashed_password=get_password_hash(user_in.password),
        parent_name=user_in.parent_name or "",
        child_name=user_in.child_name,
        child_age=user_in.child_age,
        avatar=user_in.avatar or "🦁",
        is_verified=False,
        verification_code=code,
        verification_code_expires_at=expires_at,
        stars=10,
        streak_days=1,
        mastered_words=[],
        completed_categories=[],
        quiz_high_score=0,
        total_study_minutes=0,
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)

    # Dispatch asynchronous email task to Celery via Redis
    send_verification_email_task.delay(
        to_email=db_user.email,
        child_name=db_user.child_name,
        verification_code=code,
    )

    return RegisterResponse(
        message=f"Registration successful! Please check {db_user.email} for your 6-digit verification code.",
        email=db_user.email,
        child_name=db_user.child_name,
        is_verified=False,
    )


@router.post("/verify-email", response_model=Token)
def verify_email(
    verify_in: VerifyEmailRequest,
    db: Session = Depends(get_db)
):
    """
    Verify user email with 6-digit OTP code and return active JWT access token.
    """
    user = db.query(User).filter(User.email == verify_in.email.lower()).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User account not found."
        )

    if user.is_verified:
        # Already verified, generate login token
        access_token = create_access_token(subject=user.id)
        return {
            "access_token": access_token,
            "token_type": "bearer",
            "user": user
        }

    # Validate OTP code
    if not user.verification_code or user.verification_code != verify_in.code.strip():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid verification code. Please check your email and try again."
        )

    # Check expiration
    now = datetime.now(timezone.utc)
    if user.verification_code_expires_at:
        # Handle timezone-aware or naive datetime comparison
        expires_at = user.verification_code_expires_at
        if expires_at.tzinfo is None:
            expires_at = expires_at.replace(tzinfo=timezone.utc)
        if now > expires_at:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Verification code has expired. Please request a new code."
            )

    # Mark user as verified & clear OTP
    user.is_verified = True
    user.verification_code = None
    user.verification_code_expires_at = None
    db.add(user)
    db.commit()
    db.refresh(user)

    access_token = create_access_token(subject=user.id)
    return {
        "access_token": access_token,
        "token_type": "bearer",
        "user": user
    }


@router.post("/resend-verification")
def resend_verification(
    resend_in: ResendVerificationRequest,
    db: Session = Depends(get_db)
):
    """
    Generate new OTP code and dispatch Celery email task.
    """
    user = db.query(User).filter(User.email == resend_in.email.lower()).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Account with this email not found."
        )

    if user.is_verified:
        return {
            "success": True,
            "message": "Email is already verified. You can log in directly."
        }

    code = generate_otp_code()
    user.verification_code = code
    user.verification_code_expires_at = datetime.now(timezone.utc) + timedelta(
        minutes=settings.EMAIL_VERIFICATION_EXPIRE_MINUTES
    )
    db.add(user)
    db.commit()

    # Dispatch Celery background task
    send_verification_email_task.delay(
        to_email=user.email,
        child_name=user.child_name,
        verification_code=code,
    )

    return {
        "success": True,
        "message": f"A new 6-digit verification code has been sent to {user.email}."
    }


@router.post("/login", response_model=Token)
def login(
    user_in: UserLogin,
    db: Session = Depends(get_db)
):
    """
    Authenticate user. Requires verified email address.
    """
    user = db.query(User).filter(User.email == user_in.email.lower()).first()
    if not user or not verify_password(user_in.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    if not user.is_verified:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Please verify your email before logging in. A verification code was sent to your email."
        )

    access_token = create_access_token(subject=user.id)
    return {
        "access_token": access_token,
        "token_type": "bearer",
        "user": user
    }
