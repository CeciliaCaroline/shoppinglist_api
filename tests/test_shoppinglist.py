from tests.base_test import BaseTestCase
from app.models import Shoppinglist
from app import db
import unittest
import json


class TestShoppingList(BaseTestCase):
    def create_list(self, name, description):
        """
        Helper method for creating a list with dummy data
        :return:
        """
        return self.client.post(
            '/shoppinglist',
            headers=dict(Authorization='Bearer ' + self.token()),
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


if __name__ == '__main__':
    unittest.main()
