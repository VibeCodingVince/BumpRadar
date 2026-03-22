"""
Scan endpoint - Core feature
Analyzes products/ingredients for pregnancy safety
"""
from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy.orm import Session
from typing import Optional

from app.core.database import get_db
from app.core.rate_limit import check_scan_limit, record_scan, get_scan_info, TIER_LIMITS
from app.core.auth import get_optional_user
from app.schemas.scan import ScanRequest, ScanResponse
from app.agents.orchestrator import OrchestratorAgent
from app.models.subscriber import Subscriber
from app.models.user import User

router = APIRouter()


def _get_client_ip(request: Request) -> str:
    """Extract real client IP (behind nginx proxy)."""
    forwarded = request.headers.get("X-Forwarded-For")
    if forwarded:
        return forwarded.split(",")[0].strip()
    return request.client.host


def _get_tier(email: Optional[str], db: Session) -> str:
    """Get the subscription tier for a user. Returns 'free', 'pro', or 'pro_plus'."""
    if not email:
        return "free"
    subscriber = db.query(Subscriber).filter(Subscriber.email == email).first()
    if subscriber and subscriber.status == "active":
        return subscriber.tier or "pro"
    return "free"


@router.post("/", response_model=ScanResponse)
async def scan_product(
    request: ScanRequest,
    raw_request: Request,
    db: Session = Depends(get_db),
    user: Optional[User] = Depends(get_optional_user),
):
    """
    Scan a product for pregnancy safety.

    Accepts:
    - barcode: Product barcode for database lookup
    - ingredient_text: Comma-separated ingredient list
    - image_base64: Base64-encoded photo for OCR

    Returns traffic-light safety verdict with flagged ingredients.
    Free tier: 3 scans/day.
    """
    # Validate input
    if not request.barcode and not request.ingredient_text and not request.image_base64:
        raise HTTPException(
            status_code=400,
            detail="Must provide either barcode, ingredient_text, or image_base64",
        )

    # Check premium status — JWT auth only (header spoofing removed)
    email = user.email if user else None
    tier = _get_tier(email, db)

    # Determine scan type (photo scans cost more due to Vision API)
    is_photo = bool(request.image_base64)

    # Check rate limit
    ip = _get_client_ip(raw_request)
    allowed, remaining, total = check_scan_limit(
        ip, tier=tier, email=email, is_photo=is_photo
    )

    if not allowed:
        scan_limit, photo_limit = TIER_LIMITS.get(tier, TIER_LIMITS["free"])
        if is_photo:
            if tier == "pro_plus":
                message = f"Daily photo scan limit reached ({photo_limit}/day). Try pasting ingredients as text instead!"
            elif tier == "pro":
                message = f"Daily photo scan limit reached ({photo_limit}/day). Upgrade to Pro+ for 20 photo scans/day!"
            else:
                message = "Photo scanning is a Pro feature. Upgrade to unlock!"
        elif tier != "free":
            message = f"Daily scan limit reached ({scan_limit}/day). Your limit resets tomorrow!"
        else:
            message = "Daily scan limit reached. Try again tomorrow!"
        raise HTTPException(
            status_code=429,
            detail={
                "message": message,
                "scans_today": total,
                "limit": scan_limit,
                "tier": tier,
                "is_premium": tier != "free",
            },
        )

    # Free photo scans use local Tesseract OCR ($0 cost)
    use_local_ocr = is_photo and tier == "free"

    # Run scan
    orchestrator = OrchestratorAgent(db)
    result = orchestrator.execute(request, use_local_ocr=use_local_ocr)

    # Record successful scan
    record_scan(ip, tier=tier, email=email, is_photo=is_photo)

    return result


@router.get("/usage")
async def scan_usage(
    request: Request,
    email: Optional[str] = None,
    db: Session = Depends(get_db),
    user: Optional[User] = Depends(get_optional_user),
):
    """Get current scan usage for this user."""
    ip = _get_client_ip(request)
    resolved_email = user.email if user else email
    tier = _get_tier(resolved_email, db)
    return get_scan_info(ip, tier=tier, email=resolved_email)
