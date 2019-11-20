import os
from celery import Celery
from celery.schedules import crontab

# set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')
app = Celery('kops')

# Using a string here means the worker don't have to serialize
# the configuration object to child processes.
# - namespace='CELERY' means all celery-related configuration keys
#   should have a `CELERY_` prefix.
app.config_from_object('django.conf:settings', namespace='CELERY')
REDIS_URL = 'redis://127.0.0.1:6379/3'
# celery 结果存储
RESULT_BACKEND = 'redis://127.0.0.1:6379/4'
app.conf.broker_url = REDIS_URL
app.conf.result_backend = RESULT_BACKEND

app.conf.update(
    task_serializer='json',
    accept_content=['json'],  # Ignore other content
    result_serializer='json',
    timezone='Asia/Shanghai',
    enable_utc=True,
)

# Load task modules from all registered Django app configs.
app.autodiscover_tasks()
app.conf.imports = ('kops.tasks'
                    )

app.conf.beat_schedule = {
    # 每1分钟定时执行一次
    'sync_consume_monitor': {
        'task': 'kops.tasks.get_consume_monitor',
        'schedule': crontab(minute='*/1')
    },
}
