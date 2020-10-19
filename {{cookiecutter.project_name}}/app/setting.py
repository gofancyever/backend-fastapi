from pydantic import BaseSettings
import os

class Settings:
    SQLALCHEMY_DATABASE_URL = "sqlite:///./sql_app.db"
    docs_url = '/docs'
    redoc_url = '/redoc'
    celery_backend = "redis://:password123@localhost:6379/0",
    celery_broker = "amqp://user:bitnami@localhost:5672//"


class DevelopmentSetting(Settings):
    SQLALCHEMY_DATABASE_URL = "sqlite:///./sql_app.db"
    docs_url = '/docs'
    redoc_url = '/redoc'

    # SQLALCHEMY_DATABASE_URL = "postgresql://user:password@postgresserver/db"

class ProductionSetting(Settings):
    SQLALCHEMY_DATABASE_URL = "sqlite:///./sql_app.db"
    docs_url = None
    redoc_url = None

class TestingConfigSetting(Settings):
    SQLALCHEMY_DATABASE_URL = "sqlite:///./sql_app.db"
    docs_url = '/docs'
    redoc_url = '/redoc'

config = {
    'development': DevelopmentSetting,
    'production': ProductionSetting,
    'testing': TestingConfigSetting,
    'default': DevelopmentSetting
}
settings = config[os.getenv('PYTHON_ENV') or 'default']
