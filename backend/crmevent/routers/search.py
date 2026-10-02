from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from crmevent.core.security import get_current_user
from crmevent.db.base import get_db
from crmevent.schemas.search import GlobalSearchResponse
from crmevent.services.search import global_search


router = APIRouter(prefix="/search", tags=["search"])


@router.get("/", response_model=GlobalSearchResponse)
def search(
    q: str = Query(..., min_length=2, max_length=100),
    limit: int = Query(default=5, ge=1, le=10),
    db: Session = Depends(get_db),
    _current_user=Depends(get_current_user),
):
    return GlobalSearchResponse(results=global_search(db, q, limit))

