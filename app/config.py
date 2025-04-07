import os

class Config:
   
    SQLALCHEMY_DATABASE_URI = os.getenv(
        "DATABASE_URL", 
        "postgresql://postgres:root@localhost:5432/flask_task_db"
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False

   
    CELERY_BROKER_URL = os.getenv(
        "CELERY_BROKER_URL", 
        "redis://localhost:6379/0"
    )
    CELERY_RESULT_BACKEND = os.getenv(
        "CELERY_RESULT_BACKEND", 
        "redis://localhost:6379/0"
    )

  
    RATELIMIT_STORAGE_URL = os.getenv(
        "RATELIMIT_STORAGE_URL", 
        "redis://localhost:6379"
    )
