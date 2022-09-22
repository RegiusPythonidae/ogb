# -*- coding: utf-8 -*-
"""Application configuration.

Most configuration is set via environment variables.

For local development, use a .env file to set
environment variables.
"""
from environs import Env

env = Env()
env.read_env()


class BaseConfig(object):
    ENV = env.str("FLASK_ENV", default="production")
    SECRET_KEY = env.str("SECRET_KEY")
    BCRYPT_LOG_ROUNDS = env.int("BCRYPT_LOG_ROUNDS", default=13)
    CACHE_TYPE = "simple"  # Can be "memcached", "redis", etc.

    UPLOAD_FOLDER = env.str("UPLOAD_FOLDER", default="uploads")
    SEND_FILE_MAX_AGE_DEFAULT = env.int("SEND_FILE_MAX_AGE_DEFAULT")

    SQLALCHEMY_TRACK_MODIFICATIONS = False


class DevelopmentConfig(BaseConfig):
    DEBUG = True
    ENV = env.str("FLASK_ENV", default="development")
    SQLALCHEMY_DATABASE_URI = env.str("DATABASE_URL")


class ProductionConfig(BaseConfig):
    DEBUG = False
    db_user = env.str("DATABASE_USERNAME", default="postgres")
    db_pass = env.str("DATABASE_PASSWORD", default="postgres")
    db_host = env.str("DATABASE_HOST", default="localhost")
    db_port = env.str("DATABASE_PORT", default="5432")
    db_name = env.str("DATABASE_NAME", default="postgres")

    SQLALCHEMY_DATABASE_URI = f'postgresql+psycopg2://' \
                              f'{db_user}:{db_pass}@' \
                              f'{db_host}:{db_port}/{db_name}'

    SQLALCHEMY_ENGINE_OPTIONS = {
        "pool_pre_ping": True,
        "pool_reset_on_return": 'commit',  # looks like postgres likes this more than rollback
        'pool_size': env.int("SQLALCHEMY_POOL_SIZE", default=20),
        'pool_recycle': env.int("SQLALCHEMY_POOL_RECYCLE", default=1200),
        'pool_timeout': env.int("SQLALCHEMY_POOL_TIMEOUT", default=5),
        'max_overflow': env.int("SQLALCHEMY_MAX_OVERFLOW", default=10),
    }
