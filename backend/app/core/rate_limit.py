"""
Rate limiting / freemium scan counter
Tracks scans per IP (free) or email (premium) per day.
Free: 3 text/barcode scans/day, NO photo scans (Pro only).
Pro ($9.99/mo): 20 scans/day (5 photo max, uses OpenAI Vision).
Pro+ ($29.99/mo): 40 scans/day (20 photo max, uses OpenAI Vision).

Cost math (worst case, all users max out daily):
  Free users: $0 (text/barcode only, no API calls)
  Photo scan (GPT-4o-mini Vision): ~$0.03 each

  Pro: 5 photos/day x 30 days = $4.50/month per user
    Stripe fee on $9.99: $0.59
    Net revenue: $9.99 - $0.59 = $9.40
    Guaranteed profit per Pro user: $9.40 - $4.50 = $4.90/month minimum

  Pro+: 20 photos/day x 30 days = $18.00/month per user
    Stripe fee on $29.99: $1.17
    Net revenue: $29.99 - $1.17 = $28.82
    Guaranteed profit per Pro+ user: $28.82 - $18.00 = $10.82/month minimum
"""
import time
from collections import defaultdict
from typing import Tuple

# In-memory store (fine for MVP on single server; swap to Redis later)
_scan_counts: dict = defaultdict(list)  # key -> [timestamp, ...]
_photo_counts: dict = defaultdict(list)  # key -> [timestamp, ...] (photo scans only)

FREE_SCANS_PER_DAY = 3
FREE_PHOTO_SCANS_PER_DAY = 0  # Free users cannot do photo scans

# Tier limits: (total_scans, photo_scans)
TIER_LIMITS = {
    "free": (3, 0),
    "pro": (20, 5),
    "pro_plus": (40, 20),
}

DAY_SECONDS = 86400


def _clean_counts(key: str) -> Tuple[int, int]:
    """Clean expired entries and return (total_scans, photo_scans) for today."""
    now = time.time()
    cutoff = now - DAY_SECONDS
    _scan_counts[key] = [ts for ts in _scan_counts[key] if ts > cutoff]
    _photo_counts[key] = [ts for ts in _photo_counts[key] if ts > cutoff]
    return len(_scan_counts[key]), len(_photo_counts[key])


def check_scan_limit(
    ip: str,
    tier: str = "free",
    email: str = None,
    is_photo: bool = False,
) -> Tuple[bool, int, int]:
    """
    Check if a user has remaining scans.

    Premium users (pro/pro_plus) are tracked by email (not IP) so limits
    follow them across devices. Free users are tracked by IP.

    Returns:
        (allowed, remaining, total_today)
    """
    is_premium = tier != "free"
    key = f"premium:{email}" if is_premium and email else ip
    total_today, photo_today = _clean_counts(key)

    scan_limit, photo_limit = TIER_LIMITS.get(tier, TIER_LIMITS["free"])

    if is_premium:
        remaining = max(0, scan_limit - total_today)
        allowed = total_today < scan_limit

        # Additional photo cap check
        if is_photo and photo_today >= photo_limit:
            allowed = False
            remaining = 0

        return allowed, remaining, total_today

    # Free users: no photo scans allowed
    if is_photo:
        return False, 0, total_today

    remaining = max(0, scan_limit - total_today)
    allowed = total_today < scan_limit
    return allowed, remaining, total_today


def record_scan(ip: str, tier: str = "free", email: str = None, is_photo: bool = False):
    """Record a scan for the given user."""
    is_premium = tier != "free"
    key = f"premium:{email}" if is_premium and email else ip
    _scan_counts[key].append(time.time())
    if is_photo:
        _photo_counts[key].append(time.time())


def get_scan_info(ip: str, tier: str = "free", email: str = None) -> dict:
    """Get scan usage info for display."""
    is_premium = tier != "free"
    key = f"premium:{email}" if is_premium and email else ip
    total_today, photo_today = _clean_counts(key)

    scan_limit, photo_limit = TIER_LIMITS.get(tier, TIER_LIMITS["free"])

    remaining = max(0, scan_limit - total_today)
    photo_remaining = max(0, photo_limit - photo_today)

    return {
        "scans_today": total_today,
        "scans_remaining": remaining,
        "limit": scan_limit,
        "photo_scans_today": photo_today,
        "photo_scans_remaining": photo_remaining,
        "photo_limit": photo_limit,
        "is_premium": is_premium,
        "tier": tier,
    }
