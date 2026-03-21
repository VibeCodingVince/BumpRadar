"""
Scan endpoint - Core feature
Analyzes products/ingredients for pregnancy safety
"""
from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy.orm import Session
from typing import Optional

from app.core.database import get_db
from app.core.rate_limit import check_scan_limit, record_scan, get_scan_info
from app.schemas.scan import ScanRequest, ScanResponse
from app.agents.orchestrator import OrchestratorAgent
from app.models.subscriber import Subscriber

router = APIRouter()


def _get_client_ip(request: Request) -> str:
    """Extract real client IP (behind nginx proxy)."""
    forwarded = request.headers.get("X-Forwarded-For")
    if forwarded:
        return forwarded.split(",")[0].strip()
    return request.client.host


def _check_premium(email: Optional[str], db: Session) -> bool:
    """Check if an email has an active premium subscription."""
    if not email:
        return False
    subscriber = db.query(Subscriber).filter(Subscriber.email == email).first()
    return subscriber is not None and subscriber.status == "active"


@router.post("/", response_model=ScanResponse)
async def scan_product(
    request: ScanRequest,
    raw_request: Request,
    db: Session = Depends(get_db),
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

    # Check premium status via email header
    email = raw_request.headers.get("X-User-Email")
    is_premium = _check_premium(email, db)

    # Check rate limit
    ip = _get_client_ip(raw_request)
    allowed, remaining, total = check_scan_limit(ip, is_premium=is_premium)

    if not allowed:
        raise HTTPException(
            status_code=429,
            detail={
                "message": "Daily scan limit reached! Upgrade to BumpRadar Premium for unlimited scans.",
                "scans_today": total,
                "limit": 3,
                "upgrade_url": "/premium",
            },
        )

    # Run scan
    orchestrator = OrchestratorAgent(db)
    result = orchestrator.execute(request)

    # Record successful scan
    record_scan(ip)

    return result


@router.get("/usage")
async def scan_usage(request: Request, email: Optional[str] = None, db: Session = Depends(get_db)):
    """Get current scan usage for this user."""
    ip = _get_client_ip(request)
    is_premium = _check_premium(email, db)
    return get_scan_info(ip, is_premium=is_premium)
