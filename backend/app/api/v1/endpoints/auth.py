"""
Auth endpoints - register, login, profile, change password
"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.auth import (
    hash_password,
    verify_password,
    create_access_token,
    get_current_user,
)
from app.models.user import User
from app.models.subscriber import Subscriber
from app.models.scan_history import ScanHistory
from app.schemas.auth import (
    RegisterRequest,
    LoginRequest,
    TokenResponse,
    UserResponse,
    ChangePasswordRequest,
)

router = APIRouter()


def _get_subscription_info(email: str, db: Session) -> tuple:
    """Get subscription status and tier for an email. Returns (is_premium, tier)."""
    subscriber = db.query(Subscriber).filter(Subscriber.email == email).first()
    if subscriber and subscriber.status == "active":
        return True, subscriber.tier or "pro"
    return False, "free"


@router.post("/register", response_model=TokenResponse)
async def register(req: RegisterRequest, db: Session = Depends(get_db)):
    """Create a new account."""
    existing = db.query(User).filter(User.email == req.email).first()
    if existing:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="An account with this email already exists",
        )

    user = User(
        email=req.email,
        username=req.username,
        hashed_password=hash_password(req.password),
    )
    db.add(user)
    db.commit()
    db.refresh(user)

    token = create_access_token({"sub": user.email, "user_id": user.id})
    is_premium, tier = _get_subscription_info(user.email, db)
    return TokenResponse(
        access_token=token,
        email=user.email,
        username=user.username,
        is_premium=is_premium,
        tier=tier,
    )


@router.post("/login", response_model=TokenResponse)
async def login(req: LoginRequest, db: Session = Depends(get_db)):
    """Log in with email and password."""
    user = db.query(User).filter(User.email == req.email).first()
    if not user or not verify_password(req.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password",
        )

    token = create_access_token({"sub": user.email, "user_id": user.id})
    is_premium, tier = _get_subscription_info(user.email, db)
    return TokenResponse(
        access_token=token,
        email=user.email,
        username=user.username,
        is_premium=is_premium,
        tier=tier,
    )


@router.get("/me", response_model=UserResponse)
async def get_profile(
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Get current user profile."""
    is_premium, tier = _get_subscription_info(user.email, db)
    return UserResponse(
        id=user.id,
        email=user.email,
        username=user.username,
        is_premium=is_premium,
        tier=tier,
        created_at=user.created_at,
    )


@router.put("/username")
async def update_username(
    req: dict,
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Update display name."""
    username = (req.get("username") or "").strip()[:50]
    if not username:
        raise HTTPException(status_code=400, detail="Username is required")
    user.username = username
    db.commit()
    return {"username": user.username}


@router.post("/change-password")
async def change_password(
    req: ChangePasswordRequest,
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Change password for authenticated user."""
    if not verify_password(req.current_password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Current password is incorrect",
        )

    user.hashed_password = hash_password(req.new_password)
    db.commit()
    return {"message": "Password updated successfully"}


@router.get("/history")
async def get_scan_history(
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
    limit: int = 50,
    offset: int = 0,
):
    """Get scan history for authenticated user."""
    scans = (
        db.query(ScanHistory)
        .filter(ScanHistory.user_id == user.id)
        .order_by(ScanHistory.created_at.desc())
        .offset(offset)
        .limit(min(limit, 100))
        .all()
    )
    total = db.query(ScanHistory).filter(ScanHistory.user_id == user.id).count()
    return {
        "scans": [
            {
                "id": s.id,
                "scan_type": s.scan_type,
                "input_summary": s.input_summary,
                "overall_safety": s.overall_safety,
                "verdict_message": s.verdict_message,
                "flagged_count": s.flagged_count,
                "total_ingredients": s.total_ingredients,
                "product_name": s.product_name,
                "product_brand": s.product_brand,
                "created_at": s.created_at.isoformat() if s.created_at else None,
            }
            for s in scans
        ],
        "total": total,
    }
