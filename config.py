class Config:
    # Змінюємо URL для локального запуску
    CELERY = {
        'broker_url': 'redis://localhost:6379/0',
        'result_backend': 'redis://localhost:6379/0'
    }

    REDIS_HOST = 'localhost'  # змінено з 'redis' на 'localhost'
    REDIS_PORT = 6379

    SECRET_KEY = 'your-secret-key-here'
    DEBUG = True