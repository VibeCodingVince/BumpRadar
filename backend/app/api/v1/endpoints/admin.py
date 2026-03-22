"""
Admin endpoints
Research agent, QA checks, database management
Requires authenticated admin user.
"""
from fastapi import APIRouter, Depends, Query, HTTPException, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.auth import get_current_user
from app.models.user import User
from app.agents.research_agent import ResearchAgent
from app.agents.qa_agent import QAAgent

router = APIRouter()

# Admin emails — add yours here or move to env/config
ADMIN_EMAILS: set = set()


def _require_admin(user: User = Depends(get_current_user)) -> User:
    """Dependency that requires an authenticated admin user."""
    if ADMIN_EMAILS and user.email not in ADMIN_EMAILS:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Admin access required",
        )
    return user


@router.post("/research")
async def run_research(
    mode: str = Query("fill_gaps", pattern="^(fill_gaps|expand)$"),
    limit: int = Query(50, ge=1, le=200),
    db: Session = Depends(get_db),
    admin: User = Depends(_require_admin),
):
    """
    Run the Research Agent to expand/improve the ingredient database.

    - fill_gaps: Improve unknown or low-confidence ingredients
    - expand: Add common ingredients not yet in DB
    """
    agent = ResearchAgent(db)
    return agent.execute(mode=mode, limit=limit)


@router.get("/qa")
async def run_qa(
    check: str = Query("all", pattern="^(all|ground_truth|duplicates|consistency|stats)$"),
    db: Session = Depends(get_db),
    admin: User = Depends(_require_admin),
):
    """
    Run QA checks on the ingredient database.

    - all: Run all checks
    - ground_truth: Verify known ingredient classifications
    - duplicates: Find duplicate entries
    - consistency: Check data completeness
    - stats: Database statistics
    """
    agent = QAAgent(db)
    return agent.execute(check=check)


@router.get("/stats")
async def db_stats(
    db: Session = Depends(get_db),
    admin: User = Depends(_require_admin),
):
    """Quick database statistics."""
    agent = QAAgent(db)
    return agent.execute(check="stats")
