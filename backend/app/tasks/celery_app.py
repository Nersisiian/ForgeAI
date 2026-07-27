from celery import Celery
from app.core.config import settings

celery_app = Celery(
    "pythonauto",
    broker=settings.CELERY_BROKER_URL,
    backend=None,
)
celery_app.conf.task_routes = {"app.tasks.generation.*": {"queue": "generation"}}
