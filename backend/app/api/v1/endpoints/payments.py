"""
Payments endpoint - Stripe Checkout integration
Supports two tiers: Pro ($9.99/mo) and Pro+ ($29.99/mo)
"""
from typing import Optional

import stripe
from fastapi import APIRouter, Depends, HTTPException, Request
from pydantic import BaseModel
from sqlalchemy.orm import Session

from app.core.config import settings
from app.core.database import get_db
from app.core.auth import get_optional_user, get_current_user
from app.models.subscriber import Subscriber
from app.models.user import User

router = APIRouter()

# Map Stripe price IDs to tier names (populated at runtime from settings)
def _price_to_tier() -> dict:
    mapping = {}
    if settings.STRIPE_PRICE_ID:
        mapping[settings.STRIPE_PRICE_ID] = "pro"
    if settings.STRIPE_PRICE_ID_PRO_PLUS:
        mapping[settings.STRIPE_PRICE_ID_PRO_PLUS] = "pro_plus"
    return mapping


class CheckoutRequest(BaseModel):
    email: str
    tier: str = "pro"  # "pro" or "pro_plus"


class PortalRequest(BaseModel):
    email: str


def _configure_stripe():
    if not settings.STRIPE_SECRET_KEY:
        raise HTTPException(status_code=503, detail="Stripe is not configured")
    stripe.api_key = settings.STRIPE_SECRET_KEY


def _get_price_id(tier: str) -> str:
    """Get the Stripe price ID for a given tier."""
    if tier == "pro_plus":
        price_id = settings.STRIPE_PRICE_ID_PRO_PLUS
        if not price_id:
            raise HTTPException(status_code=503, detail="Pro+ price not configured in Stripe")
        return price_id
    price_id = settings.STRIPE_PRICE_ID
    if not price_id:
        raise HTTPException(status_code=503, detail="Stripe price not configured")
    return price_id


@router.post("/create-checkout")
async def create_checkout(
    req: CheckoutRequest,
    db: Session = Depends(get_db),
    user: Optional[User] = Depends(get_optional_user),
):
    """Create a Stripe Checkout session for Pro or Pro+ subscription."""
    _configure_stripe()

    if req.tier not in ("pro", "pro_plus"):
        raise HTTPException(status_code=400, detail="Invalid tier. Must be 'pro' or 'pro_plus'")

    price_id = _get_price_id(req.tier)

    # Prefer authenticated email over body email
    email = user.email if user else req.email

    # Check if already on this tier or higher
    subscriber = db.query(Subscriber).filter(Subscriber.email == email).first()
    if subscriber and subscriber.status == "active":
        if subscriber.tier == req.tier:
            return {"already_premium": True, "message": f"You're already a {req.tier.replace('_', ' ').title()} subscriber!"}
        if subscriber.tier == "pro_plus" and req.tier == "pro":
            return {"already_premium": True, "message": "You're already on Pro+ which includes everything in Pro!"}
        # Pro user upgrading to Pro+ — use Stripe portal for subscription change
        if subscriber.tier == "pro" and req.tier == "pro_plus" and subscriber.stripe_customer_id:
            session = stripe.billing_portal.Session.create(
                customer=subscriber.stripe_customer_id,
                return_url=f"{settings.FRONTEND_URL}?upgrade=success",
            )
            return {"checkout_url": session.url, "is_upgrade": True}

    session = stripe.checkout.Session.create(
        mode="subscription",
        line_items=[{"price": price_id, "quantity": 1}],
        customer_email=email,
        success_url=f"{settings.FRONTEND_URL}?checkout=success",
        cancel_url=f"{settings.FRONTEND_URL}?checkout=cancel",
        metadata={"tier": req.tier},
    )

    return {"checkout_url": session.url}


@router.post("/webhook")
async def stripe_webhook(request: Request, db: Session = Depends(get_db)):
    """Handle Stripe webhook events."""
    payload = await request.body()
    sig_header = request.headers.get("stripe-signature")

    if not settings.STRIPE_WEBHOOK_SECRET:
        raise HTTPException(status_code=503, detail="Webhook secret not configured")

    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, settings.STRIPE_WEBHOOK_SECRET
        )
    except (ValueError, stripe.error.SignatureVerificationError):
        raise HTTPException(status_code=400, detail="Invalid webhook signature")

    event_type = event.get("type") if isinstance(event, dict) else event["type"]
    data = event.get("data", {}).get("object", {}) if isinstance(event, dict) else event["data"]["object"]

    if event_type == "checkout.session.completed":
        email = data.get("customer_email")
        customer_id = data.get("customer")
        subscription_id = data.get("subscription")
        metadata = data.get("metadata", {})
        tier = metadata.get("tier", "pro")

        if email:
            subscriber = db.query(Subscriber).filter(Subscriber.email == email).first()
            if subscriber:
                subscriber.stripe_customer_id = customer_id
                subscriber.stripe_subscription_id = subscription_id
                subscriber.status = "active"
                subscriber.tier = tier
            else:
                subscriber = Subscriber(
                    email=email,
                    stripe_customer_id=customer_id,
                    stripe_subscription_id=subscription_id,
                    status="active",
                    tier=tier,
                )
                db.add(subscriber)
            db.commit()

    elif event_type == "customer.subscription.updated":
        sub_id = data.get("id")
        status = data.get("status")  # active, past_due, canceled, etc.
        subscriber = db.query(Subscriber).filter(
            Subscriber.stripe_subscription_id == sub_id
        ).first()
        if subscriber:
            subscriber.status = status if status in ("active", "past_due") else "canceled"
            # Check if the price changed (upgrade/downgrade)
            items = data.get("items", {}).get("data", [])
            if items:
                price_id = items[0].get("price", {}).get("id")
                price_tier_map = _price_to_tier()
                if price_id in price_tier_map:
                    subscriber.tier = price_tier_map[price_id]
            db.commit()

    elif event_type == "customer.subscription.deleted":
        sub_id = data.get("id")
        subscriber = db.query(Subscriber).filter(
            Subscriber.stripe_subscription_id == sub_id
        ).first()
        if subscriber:
            subscriber.status = "canceled"
            db.commit()

    return {"status": "ok"}


@router.get("/status")
async def subscription_status(
    email: Optional[str] = None,
    db: Session = Depends(get_db),
    user: Optional[User] = Depends(get_optional_user),
):
    """Check if an email has an active premium subscription."""
    resolved_email = user.email if user else email
    if not resolved_email:
        return {"is_premium": False, "tier": "free", "email": None}
    subscriber = db.query(Subscriber).filter(Subscriber.email == resolved_email).first()
    if subscriber and subscriber.status == "active":
        return {
            "is_premium": True,
            "tier": subscriber.tier or "pro",
            "email": resolved_email,
        }
    return {"is_premium": False, "tier": "free", "email": resolved_email}


@router.post("/portal")
async def customer_portal(
    req: Optional[PortalRequest] = None,
    db: Session = Depends(get_db),
    user: Optional[User] = Depends(get_optional_user),
):
    """Create a Stripe Customer Portal session for managing subscription."""
    _configure_stripe()

    email = user.email if user else (req.email if req else None)
    if not email:
        raise HTTPException(status_code=401, detail="Authentication required")

    subscriber = db.query(Subscriber).filter(Subscriber.email == email).first()
    if not subscriber or not subscriber.stripe_customer_id:
        raise HTTPException(status_code=404, detail="No subscription found for this email")

    session = stripe.billing_portal.Session.create(
        customer=subscriber.stripe_customer_id,
        return_url=settings.FRONTEND_URL,
    )

    return {"portal_url": session.url}
