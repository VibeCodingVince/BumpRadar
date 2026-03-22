"""
Subscriber model for premium payment tracking
"""
from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.sql import func
from app.core.database import Base


class Subscriber(Base):
    """Tracks premium subscribers via Stripe"""
    __tablename__ = "subscribers"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(255), unique=True, nullable=False, index=True)
    stripe_customer_id = Column(String(255), unique=True, nullable=True)
    stripe_subscription_id = Column(String(255), unique=True, nullable=True)
    status = Column(String(50), nullable=False, default="inactive")  # active, canceled, past_due, inactive
    tier = Column(String(20), nullable=False, default="pro")  # pro, pro_plus
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())

    def __repr__(self):
        return f"<Subscriber(email='{self.email}', status='{self.status}', tier='{self.tier}')>"
