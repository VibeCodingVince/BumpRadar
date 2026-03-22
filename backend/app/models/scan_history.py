"""
Scan history model - stores user scan results for the account page
"""
from sqlalchemy import Column, Integer, String, Float, Text, DateTime, ForeignKey
from sqlalchemy.sql import func
from app.core.database import Base


class ScanHistory(Base):
    """Record of a user's scan for their history page"""
    __tablename__ = "scan_history"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    scan_type = Column(String(20), nullable=False)  # text, barcode, photo
    input_summary = Column(String(255), nullable=True)  # first ~100 chars of input or product name
    overall_safety = Column(String(20), nullable=False)  # safe, caution, avoid
    verdict_message = Column(Text, nullable=True)
    flagged_count = Column(Integer, default=0)
    total_ingredients = Column(Integer, default=0)
    product_name = Column(String(255), nullable=True)
    product_brand = Column(String(255), nullable=True)
    created_at = Column(DateTime, default=func.now())

    def __repr__(self):
        return f"<ScanHistory(user={self.user_id}, safety={self.overall_safety}, at={self.created_at})>"
