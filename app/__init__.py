from flask import Flask
from flask_bcrypt import Bcrypt
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import os

# Initialize application
app = Flask(__name__, static_folder=None)

# app configuration
app_settings = os.getenv(
    'APP_SETTINGS',
    'app.config.DevelopmentConfig'
)
app.config.from_object(app_settings)

# Initialize Flask Sql Alchemy
db = SQLAlchemy(app)

# Initialize Flask Migrate
migrate = Migrate(app, db)

# Initialize Flask Bcrypt
bcrypt = Bcrypt(app)

# Register blue prints
from app.authenticate.views import auth
from app.shoppinglists.shop_list import shop_list
from app.items.items import items
from app.apiary.views import apiary

app.register_blueprint(auth)
app.register_blueprint(shop_list)
app.register_blueprint(items)
app.register_blueprint(apiary)
