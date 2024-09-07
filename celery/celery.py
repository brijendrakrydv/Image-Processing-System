from celery import Celery
from config import Config

celery_app = Celery('tasks', broker=Config.CELERY_BROKER_URL)
celery_app.conf.update(result_backend=Config.CELERY_RESULT_BACKEND)
