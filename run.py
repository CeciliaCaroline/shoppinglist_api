import os

from app import app_init

config_name = os.getenv('APP_SETTINGS', 'development')
app = app_init(config_name)


if __name__ == '__main__':
    app.run()