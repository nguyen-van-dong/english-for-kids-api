from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.user import User
from app.schemas.user import UserRegister, UserLogin, Token, UserResponse
from app.core.security import get_password_hash, verify_password, create_access_token

router = APIRouter()

@router.post("/register", response_model=Token)
def register(
    user_in: UserRegister,
    db: Session = Depends(get_db)
):
    # Check if email exists
    existing_user = db.query(User).filter(User.email == user_in.email.lower()).first()
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email is already registered. Please login instead."
        )

    # Create new user
    db_user = User(
        email=user_in.email.lower(),
        hashed_password=get_password_hash(user_in.password),
        parent_name=user_in.parent_name or "",
        child_name=user_in.child_name,
        child_age=user_in.child_age,
        avatar=user_in.avatar or "🦁",
        stars=10,
        streak_days=1,
        mastered_words=[],
        completed_categories=[],
        quiz_high_score=0,
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)

    access_token = create_access_token(subject=db_user.id)
    return {
        "access_token": access_token,
        "token_type": "bearer",
        "user": db_user
    }

@router.post("/login", response_model=Token)
def login(
    user_in: UserLogin,
    db: Session = Depends(get_db)
):
    user = db.query(User).filter(User.email == user_in.email.lower()).first()
    if not user or not verify_password(user_in.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token = create_access_token(subject=user.id)
    return {
        "access_token": access_token,
        "token_type": "bearer",
        "user": user
    }
