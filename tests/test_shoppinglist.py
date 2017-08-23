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

    def create_list(self, name, description):
        """
        Helper method for creating a list with dummy data
        :return:
        """
        result = self.register_user('example@gmail.com', '123456')
        auth_token = json.loads(result.data.decode())['auth_token']
        return self.client.post(
            '/shoppinglist',
            headers=dict(Authorization='Bearer ' + auth_token),
            content_type='application/json',
            data=json.dumps(dict(name=name, description=description)))

    def create_list_with_wrong_request_content_type(self, name, description):
        """
        Helper method to create a list using a wrong content-type
        :param name
        :param description
        :return:
        """
        return self.client.post(
            '/auth/register',
            content_type='application/javascript',
            data=json.dumps(dict(name=name, description=description)))

    def test_create_shoppinglist(self):
        """Test API can create a shoppinglist """

        with self.client:
            res = self.create_list('travel', 'Go to Kenya')
            self.assertEqual(res.status_code, 201)
            self.assertIn('Go to Kenya', str(res.data))

    def test_create_shoppinglist_with_invalid_name(self):
        """Test API can create a shoppinglist """

        with self.client:
            res = self.create_list('travel!!!', 'Go to Kenya')
            self.assertEqual(res.status_code, 400)

    def test_create_shoppinglist_with_empty_name_or_description(self):
        """Test API can create a shoppinglist """

        with self.client:
            res = self.create_list(' ', 'Go to Kenya')
            self.assertEqual(res.status_code, 400)

    def test_create_list_with_wrong_content_type(self):
        """"
        Test API can not create a list with a wrong content type
        """
        with self.client:
            response = self.create_list_with_wrong_request_content_type('travel', 'Go to Kenya')
            print(response.data)
            self.assertEqual(response.status_code, 202)

    # def test_list_cant_be_created_without_authorization_header(self):


if __name__ == '__main__':
    unittest.main()
