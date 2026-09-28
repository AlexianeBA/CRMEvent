import asyncio
import logging
import os

from crmevent.db.session import SessionLocal
from crmevent.models.users import Users
from crmevent.services.notification import synchronize_notifications


logger = logging.getLogger(__name__)


def synchronize_all_users():
    with SessionLocal() as db:
        user_ids = [row[0] for row in db.query(Users.id).filter(Users.is_active == 1).all()]
    for user_id in user_ids:
        with SessionLocal() as db:
            try:
                synchronize_notifications(db, user_id)
            except Exception:
                db.rollback()
                logger.exception("Échec de synchronisation des notifications pour l'utilisateur %s", user_id)


async def notification_scheduler():
    interval = max(60, int(os.getenv("NOTIFICATION_SYNC_INTERVAL_SECONDS", "900")))
    while True:
        try:
            await asyncio.to_thread(synchronize_all_users)
        except Exception:
            logger.exception("Échec du planificateur de notifications")
        await asyncio.sleep(interval)
