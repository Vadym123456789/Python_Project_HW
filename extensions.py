from flask import Flask
from celery import Celery
from config import Config

app = Flask(__name__)
app.config.from_object(Config)

celery = Celery(
    app.import_name,
    broker=app.config['CELERY']['broker_url'],
    backend=app.config['CELERY']['result_backend']
)

class ContextTask(celery.Task):
    def __call__(self, *args, **kwargs):
        with app.app_context():
            return self.run(*args, **kwargs)

celery.Task = ContextTask