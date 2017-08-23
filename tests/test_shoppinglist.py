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
            data = json.loads(res.data.decode())
            self.assertTrue(data['name'], 'travel')
            self.assertTrue(data['description'], 'Go to Kenya')
            self.assertEqual(res.status_code, 201)
            self.assertIn('Go to Kenya', str(res.data))
            return data

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
            self.assertEqual(response.status_code, 202)

    def test_get_shopping_list(self):
        """"
        Test API can get all shopping lists
        """
        with self.client:
            response = self.client.get(
                '/shoppinglist',
                headers=dict(Authorization="Bearer " + self.token()),
            )
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 200)
            self.assertEqual(data['status'], 'success')

    def test_get_single_shopping_list(self):
        with self.client:
            res = self.create_list('travel', 'Go to Kenya')
            results = json.loads(res.data.decode())
            print(res.data)

            response = self.client.get(
                '/shoppinglist/{}'.format(results['id']),
                headers=dict(Authorization="Bearer " + self.token())
            )
            print(response.data)
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 200)
            self.assertEqual(data['status'], 'success')

    def test_shoppinglist_can_be_edited(self):
        """Test API can edit an existing shoppinglist. (PUT request)"""
        with self.client:
            res = self.create_list('eat', 'eat, pray, love')
            self.assertEqual(res.status_code, 201)
            # get the json with the shoppinglist
            results = json.loads(res.data.decode())

            # then, we edit the created shoppinglist by making a PUT request
            rv = self.client.put(
                '/shoppinglist/{}'.format(results['id']),
                headers=dict(Authorization="Bearer " + self.token()),
                data={
                    "name": "Dont just eat, but also pray and love :-)", "description": "adsfghjk"
                })
            self.assertEqual(rv.status_code, 200)

            # finally, we get the edited shoppinglist to see if it is actually edited.
            results = self.client.get(
                '/shoppinglist/{}'.format(results['id']),
                headers=dict(Authorization="Bearer " + self.token()))
            self.assertIn('Dont just eat', str(results.data))


if __name__ == '__main__':
    unittest.main()
