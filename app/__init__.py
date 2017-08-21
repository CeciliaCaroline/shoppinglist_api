from flask_sqlalchemy import SQLAlchemy
from flask_api import FlaskAPI

# local import
from config import app_config

# initialize sql-alchemy
db = SQLAlchemy()


# initialize application
def app_init(config_name):
    app = FlaskAPI(__name__, instance_relative_config=True)
    app.config.from_object(app_config[config_name])
    app.config.from_pyfile('config.py')
    db.init_app(app)
