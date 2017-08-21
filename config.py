import os

postgres_local_base = 'postgresql://postgres:ceciliacaroline20@localhost/'
database_name = 'api'


# base config
class Config(object):
    """Parent configuration class."""
    DEBUG = False
    CSRF_ENABLED = True
    SECRET = os.getenv('SECRET_KEY', 'cecilia')
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL')
    SQLALCHEMY_TRACK_MODIFICATIONS = False


# development config
class DevelopmentConfig(Config):
    """Configurations for Development."""
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = postgres_local_base + database_name

# configurations
app_config = {
    'development': DevelopmentConfig

}