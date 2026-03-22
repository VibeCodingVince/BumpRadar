"""
Payments endpoint - Stripe Checkout integration
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


class CheckoutRequest(BaseModel):
    email: str


class PortalRequest(BaseModel):
    email: str


def _configure_stripe():
    if not settings.STRIPE_SECRET_KEY:
        raise HTTPException(status_code=503, detail="Stripe is not configured")
    stripe.api_key = settings.STRIPE_SECRET_KEY


@router.post("/create-checkout")
async def create_checkout(
    req: CheckoutRequest,
    db: Session = Depends(get_db),
    user: Optional[User] = Depends(get_optional_user),
):
    """Create a Stripe Checkout session for premium subscription."""
    _configure_stripe()

    if not settings.STRIPE_PRICE_ID:
        raise HTTPException(status_code=503, detail="Stripe price not configured")

    # Prefer authenticated email over body email
    email = user.email if user else req.email

    # Check if already premium
    subscriber = db.query(Subscriber).filter(Subscriber.email == email).first()
    if subscriber and subscriber.status == "active":
        return {"already_premium": True, "message": "You're already a premium subscriber!"}

    session = stripe.checkout.Session.create(
        mode="subscription",
        line_items=[{"price": settings.STRIPE_PRICE_ID, "quantity": 1}],
        customer_email=email,
        success_url=f"{settings.FRONTEND_URL}?checkout=success",
        cancel_url=f"{settings.FRONTEND_URL}?checkout=cancel",
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

        if email:
            subscriber = db.query(Subscriber).filter(Subscriber.email == email).first()
            if subscriber:
                subscriber.stripe_customer_id = customer_id
                subscriber.stripe_subscription_id = subscription_id
                subscriber.status = "active"
            else:
                subscriber = Subscriber(
                    email=email,
                    stripe_customer_id=customer_id,
                    stripe_subscription_id=subscription_id,
                    status="active",
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
        return {"is_premium": False, "email": None}
    subscriber = db.query(Subscriber).filter(Subscriber.email == resolved_email).first()
    is_premium = subscriber is not None and subscriber.status == "active"
    return {"is_premium": is_premium, "email": resolved_email}


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
