from tests.base_test import BaseTestCase
from app.models import Shoppinglist
from app import db
import unittest
import json
import time


class TestShoppingList(BaseTestCase):
    def register_user(self, email, password):
        """
        Helper method for registering a user with dummy data
        :return:
        """
        return self.client.post(
            '/auth/register',
            content_type='application/json',
            data=json.dumps(dict(email=email, password=password)))

    def login_user(self, email, password):
        """
        Helper method to login a user
        :param email: Email
        :param password: Password
        :return:
        """
        return self.client.post(
            '/auth/login',
            content_type='application/json',
            data=json.dumps(dict(email=email, password=password)))

    def test_create_shoppinglist(self):
        """Test API can create a shoppinglist """

        with self.client:
            result = self.register_user('example@gmail.com', '123456')
            auth_token = json.loads(result.data.decode())['auth_token']

            # create a shoppinglist by making a POST request
            res = self.client.post(
                '/shoppinglist',
                headers=dict(Authorization='Bearer ' + auth_token),
                content_type='application/json',
                data=json.dumps(dict(name='travel', description='Go to Kenya')))
            self.assertEqual(res.status_code, 201)
            self.assertIn('Go to Kenya', str(res.data))

    def create_list(self, name, description):
        """
        Helper method for creating a list with dummy data
        :return:
        """
        return self.client.post(
            '/shoppinglist',
            content_type='application/json',
            data=json.dumps(dict(name=name, description=description)))


if __name__ == '__main__':
    unittest.main()
