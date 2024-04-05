import os
from celery import Celery
from uwords_api.settings import CELERY_BROKER_URL


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'uwords_api.settings')

app = Celery('uwords_api', broker=CELERY_BROKER_URL)
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()


@app.task(bind=True)
def debug_task(self):
    print(f'Request: {self.request!r}')
