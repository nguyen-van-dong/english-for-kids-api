import logging
from app.core.config import settings

logger = logging.getLogger(__name__)

try:
    from celery import Celery

    celery_app = Celery(
        "english_kids_worker",
        broker=settings.CELERY_BROKER_URL,
        backend=settings.CELERY_RESULT_BACKEND,
        include=["app.tasks.email"]
    )

    celery_app.conf.update(
        task_serializer="json",
        accept_content=["json"],
        result_serializer="json",
        timezone="UTC",
        enable_utc=True,
        task_track_started=True,
        task_time_limit=300,  # 5 minutes max
    )
    HAS_CELERY = True
except ImportError:
    logger.warning("Celery is not installed in this environment. Background tasks will fall back gracefully.")
    HAS_CELERY = False

    class DummyCelery:
        def task(self, *args, **kwargs):
            def decorator(func):
                def delay(*f_args, **f_kwargs):
                    return func(None, *f_args, **f_kwargs)
                func.delay = delay
                return func
            return decorator

    celery_app = DummyCelery()
