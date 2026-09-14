from fastapi import APIRouter, Depends, Query, Response, status
from sqlalchemy.orm import Session

from crmevent.core.security import get_current_user
from crmevent.db.base import get_db
from crmevent.schemas.notification import NotificationCount, NotificationRead
from crmevent.services import notification as service


router = APIRouter(prefix="/notifications", tags=["notifications"])


@router.get("/", response_model=list[NotificationRead])
def list_notifications(db: Session = Depends(get_db), current_user=Depends(get_current_user), is_read: bool | None = Query(default=None), skip: int = Query(default=0, ge=0), limit: int = Query(default=50, ge=1, le=100)):
    return service.get_notifications(db, current_user.id, is_read, skip, limit)


@router.get("/count", response_model=NotificationCount)
def count_unread_notifications(db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    return service.count_unread_notifications(db, current_user.id)


@router.get("/count-by-type", response_model=dict[str, int])
def count_by_type(db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    return service.count_notifications_by_type(db, current_user.id)


@router.post("/sync", response_model=NotificationCount)
def synchronize_notifications(db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    return service.synchronize_notifications(db, current_user.id)


@router.patch("/read-all", response_model=NotificationCount)
def mark_all_as_read(db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    service.mark_all_notifications_as_read(db, current_user.id)
    return service.count_unread_notifications(db, current_user.id)


@router.get("/{notification_id}", response_model=NotificationRead)
def get_notification(notification_id: int, db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    return service.get_notification(db, notification_id, current_user.id)


@router.patch("/{notification_id}/read", response_model=NotificationRead)
def mark_as_read(notification_id: int, db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    return service.mark_notification_as_read(db, notification_id, current_user.id)


@router.patch("/{notification_id}/unread", response_model=NotificationRead)
def mark_as_unread(notification_id: int, db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    return service.mark_notification_as_unread(db, notification_id, current_user.id)


@router.delete("/{notification_id}", status_code=status.HTTP_204_NO_CONTENT)
def archive_notification(notification_id: int, db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    service.archive_notification(db, notification_id, current_user.id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)
