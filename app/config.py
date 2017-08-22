import os

base_dir = os.path.abspath(os.path.dirname(__file__))
postgres_local_base = 'postgresql://postgres:ceciliacaroline20@localhost/'
database_name = 'shop_list'


class BaseConfig:
    """
    Base application configuration
    """
    SECRET_KEY = os.getenv('SECRET_KEY', 'my_strong_key')
    DEBUG = False
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    BCRYPT_HASH_PREFIX = 13


class DevelopmentConfig(BaseConfig):
    """
    Development application configuration
    """
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = postgres_local_base + database_name
    BCRYPT_HASH_PREFIX = 4


class TestingConfig(BaseConfig):
    """
    Testing application configuration
    """
    DEBUG = True
    TESTING = True
    SQLALCHEMY_DATABASE_URI = postgres_local_base + "test_db"
    BCRYPT_HASH_PREFIX = 3
