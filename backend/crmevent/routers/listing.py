from typing import Annotated

from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from crmevent.core.security import get_current_user
from crmevent.db.base import get_db
from crmevent.models.company import Company
from crmevent.models.users import Users
from crmevent.schemas.listing import ExportParams, ListParams
from crmevent.services import listing as service


router = APIRouter(prefix="/lists", tags=["lists"])


@router.get("/options")
def options(db: Session = Depends(get_db), user=Depends(get_current_user)):
    return {
        "companies": [{"value": row.id, "title": row.name} for row in db.query(Company.id, Company.name).order_by(Company.name, Company.id)],
        "commercials": [{"value": row.id, "title": row.email} for row in db.query(Users.id, Users.email).order_by(Users.email, Users.id)],
    }


@router.get("/{resource}/meta")
def metadata(resource: str, user=Depends(get_current_user)):
    return service.metadata(resource, user)


@router.get("/{resource}/export")
def export(resource: str, params: Annotated[ExportParams, Query()],
           db: Session = Depends(get_db), user=Depends(get_current_user)):
    return service.export_list(db, resource, params, user, params.format)


@router.get("/{resource}/")
def list_page(resource: str, params: Annotated[ListParams, Query()],
              db: Session = Depends(get_db), user=Depends(get_current_user)):
    return service.list_page(db, resource, params, user)
