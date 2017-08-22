from app import db
from tests.base_test import BaseTestCase
from app.models import User
import unittest


class TestUserModel(BaseTestCase):
    """
    Test that the auth token is generated correctly
    """

    def created_user(self):
        """"
        Method to create a user and add them to the database
        """
        user = User(email='example@gmail.com', password='123456')
        db.session.add(user)
        db.session.commit()
        return user

    def get_auth_token(self, user):
        """"
        Method to retrieve the auth token
        """
        auth_token = user.encode_auth_token(user.id)
        return auth_token

    def test_encode_user_token(self):
        """"
        Testing that the token generated is correct
        """
        user = self.created_user()
        auth_token = self.get_auth_token(user)
        self.assertTrue(isinstance(auth_token, bytes))

    def test_decode_user_token(self):
        """"
        Testing that the encoded token is correctly decoded
        """
        user = self.created_user()
        auth_token = self.get_auth_token(user)
        self.assertTrue(isinstance(auth_token, bytes))
        self.assertTrue(user.decode_auth_token(auth_token.decode('utf-8')) == 1, msg='The user Id should be 1')


if __name__ == '__main__':
    unittest.main()
