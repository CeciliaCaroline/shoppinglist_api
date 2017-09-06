from tests.base_test import BaseTestCase
from app.models import Items
from app import db
import unittest
import json


class ItemsTestCase(BaseTestCase):
    # def create_list(self, name, description, token):
    #     """
    #     Helper method for creating a list with dummy data
    #     :return:
    #     """
    #     return self.client.post(
    #         '/shoppinglist',
    #         headers=dict(Authorization='Bearer ' + token),
    #         content_type='application/json',
    #         data=json.dumps(dict(name=name, description=description)))
    #
    # def create_item(self, name, price, token):
    #     """"
    #     Helper method to create a shopping list item with dummy data
    #     :return:
    #     """
    #     token = self.token()
    #     res = self.create_list('travel', 'Go to Kenya', token)
    #     results = json.loads(res.data.decode())
    #     response = self.client.get(
    #         '/shoppinglist/{}'.format(results['id']),
    #         content_type='application/json',
    #         headers=dict(Authorization="Bearer " + token)
    #     )
    #     return self.client.post('/shoppinglist/{}/items'.format(results['id']),
    #                             content_type='application/json',
    #                             headers=dict(Authorization='Bearer ' + token),
    #                             data=(dict(name=name, price=price)),
    #                             )

    def test_create_item(self):
        with self.client:
            token = self.token()

            shop = json.dumps({
                'name': 'Travel',
                'description': 'Visit places'
            })
            self.client.post('/shoppinglist', data=shop, content_type='application/json',
                             headers=dict(Authorization='Bearer ' + token))

            item = json.dumps({'name': 'Go to Nairobi', 'price': '5000kshs'})
            response = self.client.post('/shoppinglist/1/items', data=item,
                                        content_type='application/json',
                                        headers=dict(Authorization='Bearer ' + token))
            print(response.data)
            self.assertEqual(response.status_code, 201)
            self.assertIn('Go to Nairobi', response.data.decode())

    def test_delete_item_that_doesnt_exist(self):
        """Should return 404 for missing item"""
        with self.client:
            token = self.token()
            response = self.client.delete('/shoppinglist/1/items/47',
                                          content_type='application/json',
                                          headers=dict(Authorization='Bearer ' + token))
            self.assertEqual(response.status_code, 404)
            self.assertIn('Item not found', response.data.decode())

    def test_delete_item_(self):
        """Should return 200 for success"""
        with self.client:
            token = self.token()
            shop = json.dumps({
                'name': 'Travel',
                'description': 'Visit places'
            })
            self.client.post('/shoppinglist', data=shop, content_type='application/json',
                             headers=dict(Authorization='Bearer ' + token))

            item = json.dumps({'name': 'Go to Nairobi', 'price': '5000kshs'})
            self.client.post('/shoppinglist/1/items', data=item,
                             content_type='application/json',
                             headers=dict(Authorization='Bearer ' + token))

            response = self.client.delete('/shoppinglist/1/items/1',
                                          content_type='application/json',
                                          headers=dict(Authorization='Bearer ' + token))
            print(response.data)
            self.assertEqual(response.status_code, 200)
            self.assertIn('Shopping list item has been deleted', response.data.decode())

    def test_edit_item_(self):
        """Should return 200 for success"""
        with self.client:
            token = self.token()
            shop = json.dumps({
                'name': 'Travel',
                'description': 'Visit places'
            })
            self.client.post('/shoppinglist', data=shop, content_type='application/json',
                             headers=dict(Authorization='Bearer ' + token))

            item = json.dumps({'name': 'Go to Nairobi', 'price': '5000kshs'})
            self.client.post('/shoppinglist/1/items', data=item,
                             content_type='application/json',
                             headers=dict(Authorization='Bearer ' + token))
            new_item = json.dumps({
                'name': 'Travelling bag',
                'price': '5000ugx'
            })

            response = self.client.put('/shoppinglist/1/items/1', data=new_item,
                                       content_type='application/json',
                                       headers=dict(Authorization='Bearer ' + token))

            print(response.data)
            self.assertEqual(response.status_code, 200)
            self.assertIn('Shopping list item has been updated', response.data.decode())


if __name__ == '__main__':
    unittest.main()

