from flask_testing import TestCase
from app import app
from flask import current_app
import unittest
import os


class TestDevelopmentConfig(TestCase):
    def create_app(self):
        """
        Create an app with the development configuration
        :return:
        """
        app.config.from_object('app.config.DevelopmentConfig')
        return app

    def test_app_in_development(self):
        self.assertFalse(app.config['SECRET_KEY'] is 'caroline')
        self.assertTrue(app.config['DEBUG'], True)
        self.assertTrue(app.config['BCRYPT_HASH_PREFIX'] == 4)
        self.assertFalse(current_app is None)
        self.assertTrue(
            app.config['SQLALCHEMY_DATABASE_URI'] == "postgresql://ceciliacaroline:ceciliacaroline20@localhost/shop_list")
        self.assertEqual(app.config['AUTH_TOKEN_EXPIRY_DAYS'], 1)
        self.assertEqual(app.config['AUTH_TOKEN_EXPIRY_SECONDS'], 18)


class TestTestingConfig(TestCase):
    def create_app(self):
        """
                Create an instance of the app with the testing configuration
                :return:
                """
        app.config.from_object('app.config.TestingConfig')
        return app

    def test_app_in_testing(self):
        self.assertFalse(app.config['SECRET_KEY'] is 'caroline')
        self.assertTrue(app.config['DEBUG'], True)
        self.assertTrue(app.config['TESTING'] is True)
        self.assertTrue(app.config['BCRYPT_HASH_PREFIX'] == 3)
        self.assertFalse(current_app is None)
        self.assertTrue(
            app.config['SQLALCHEMY_DATABASE_URI'] == os.getenv('DATABASE_URL_TEST',
                                                               "postgresql://ceciliacaroline:ceciliacaroline20@localhost/test_api"))

        self.assertEqual(app.config['AUTH_TOKEN_EXPIRY_SECONDS'], 2)
        self.assertEqual(app.config['AUTH_TOKEN_EXPIRATION_TIME_DURING_TESTS'], 4)
        self.assertEqual(app.config['AUTH_TOKEN_EXPIRY_DAYS'], 0)


if __name__ == '__main__':
    unittest.main()
