import os
from flask import Flask
from flask_bcrypt import Bcrypt
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_mail import Mail, Message

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

# Inirialize Flask Bcrypt
bcrypt = Bcrypt(app)

mail = Mail(app)

# Register blue prints
from app.authenticate.views import auth
from app.shoppinglists.shop_list import shop_list
from app.shoppinglists.v2_shop_list import v2_shop_list
from app.items.items import items
from app.items.v2_items import v2_items
from app.apiary.views import apiary

app.register_blueprint(auth)
app.register_blueprint(shop_list)
app.register_blueprint(v2_shop_list)
app.register_blueprint(items)
app.register_blueprint(v2_items)
app.register_blueprint(apiary)
