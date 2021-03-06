import datetime
from app import app, db, bcrypt
import jwt



class User(db.Model):
    """
    Users table
    """

    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    email = db.Column(db.String(250), unique=True, nullable=False)
    password = db.Column(db.String(250), nullable=False)
    registered_on = db.Column(db.DateTime, nullable=False)
    shoppinglists = db.relationship(
        'ShoppingList', order_by='ShoppingList.id', lazy='dynamic')

    def __init__(self, email, password):
        self.email = email
        self.password = bcrypt.generate_password_hash(password, app.config.get('BCRYPT_LOG_ROUNDS')) \
            .decode('utf-8')
        self.registered_on = datetime.datetime.now()

    def encode_auth_token(self, user_id):
        """
        Encode the Auth token
        :param user_id: User's Id
        :return:
        """
        try:
            payload = {
                'exp': datetime.datetime.utcnow() + datetime.timedelta(days=1, seconds=10),
                'iat': datetime.datetime.now(),
                'sub': user_id
            }
            return jwt.encode(
                payload,
                app.config['SECRET_KEY'],
                algorithm='HS256'
            )
        except Exception as e:
            return e

    @staticmethod
    def decode_auth_token(token):
        """
        Decoding the token to get the payload and then return the user Id in 'sub'
        :param token: Auth Token
        :return:
        """
        try:
            payload = jwt.decode(token, app.config['SECRET_KEY'], algorithms='HS256')
            is_token_blacklisted = BlackListToken.check_blacklist(token)
            if is_token_blacklisted:
                return 'Token was Blacklisted, Please login In'
            return payload['sub']
        except jwt.ExpiredSignatureError:
            return 'Signature expired, Please sign in again'
        except jwt.InvalidTokenError:
            return 'Invalid token. Please sign in again'


class BlackListToken(db.Model):
    """
    Table to store blacklisted/invalid auth tokens
    """
    __tablename__ = 'blacklist_token'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    token = db.Column(db.String(255), unique=True, nullable=False)
    blacklisted_on = db.Column(db.DateTime, nullable=False)

    def __init__(self, token):
        self.token = token
        self.blacklisted_on = datetime.datetime.now()

    @staticmethod
    def check_blacklist(token):
        """
        Check to find out whether a token has already been blacklisted.
        :param token: Authorization token
        :return:
        """
        response = BlackListToken.query.filter_by(token=token).first()
        if response:
            return True
        return False


class ShoppingList(db.Model):
    """This class defines the shoppinglist table."""

    __tablename__ = 'shoppinglists'

    # define the columns of the table, starting with its primary key
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250))
    description = db.Column(db.String(250))
    user_id = db.Column(db.Integer, db.ForeignKey(User.id))
    items = db.relationship('Items', order_by='Items.item_id', lazy='dynamic')

    def __init__(self, name, description, user_id):
        """Initialize the shoppinglist with a name and description."""
        self.name = name
        self.description = description
        self.user_id = user_id

    def json(self):
        """"
        Get Json representation of the model
        """
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description
        }


class Items(db.Model):
    """This class defines the shoppinglist table."""

    __tablename__ = 'items'

    # define the columns of the table, starting with its primary key
    item_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250))
    price = db.Column(db.String(250))
    list_id = db.Column(db.Integer, db.ForeignKey(ShoppingList.id))

    def __init__(self, name, price, list_id):
        """Initialize the item with a name and description."""
        self.name = name
        self.price = price
        self.list_id = list_id

    def json(self):
        """"
        Get Json representation of the model
        """
        return {
            'id': self.item_id,
            'name': self.name,
            'price': self.price,
            'list_id': self.list_id,
            # 'status': 'success'
        }
