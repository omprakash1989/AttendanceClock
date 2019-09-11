from settings import CELERY_BROKER_URL

# Celery broker.
#CELERY_RESULT_BACKEND = CELERY_BROKER_URL

CELERY_WORKER_CONFIG = {
    'broker': CELERY_BROKER_URL,
    'loglevel': 'INFO',
    'traceback': True,
    'worker_max_tasks_per_child': 25
}

CELERY_BEAT_CONFIG = {
    'broker': CELERY_BROKER_URL,
    'loglevel': 'INFO',
    'traceback': True,
    'schedule': '/var/lib/celerybeat/schedule.db'
}

CELERY_DEFAULT_QUEUE = 'default'

CELERY_QUEUES = {
    'default': {
        "exchange": "default",
        "binding_key": "default",
    },
}

CELERY_ROUTES = {
    'api.punching_clock.tasks.test_task': {'queue': 'error_email_queue'},
}

CELERYD_TASK_SOFT_TIME_LIMIT = 120
