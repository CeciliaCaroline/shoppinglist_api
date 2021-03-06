import json
import unittest

from tests.base_test import BaseTestCase


class ItemsTestCase(BaseTestCase):
    def create_list(self, name, description, token):
        """
        Helper method for creating a list with dummy data
        :return:
        """
        return self.client.post(
            '/v1/shoppinglist/',
            headers=dict(Authorization='Bearer ' + token),
            content_type='application/json',
            data=json.dumps(dict(name=name, description=description)))

    def create_item(self, name, price, token):
        """
        Helper method for creating an item with dummy data
        :return:
        """
        return self.client.post(
            '/v1/shoppinglist/1/items/',
            headers=dict(Authorization='Bearer ' + token),
            content_type='application/json',
            data=json.dumps(dict(name=name, price=price)))

    def create_item_with_wrong_content_type(self, name, price, token):
        """
        Helper method for creating an item with wrong content type with dummy data
        :return:
        """
        return self.client.post(
            '/v1/shoppinglist/1/items/',
            headers=dict(Authorization='Bearer ' + token),
            content_type='application/javascript',
            data=json.dumps(dict(name=name, price=price)))

    def edit_item(self, name, price, token):
        """
        Helper method for creating an item with dummy data
        :return:
        """
        return self.client.put(
            '/v1/shoppinglist/1/items/1',
            headers=dict(Authorization='Bearer ' + token),
            content_type='application/json',
            data=json.dumps(dict(name=name, price=price)))

    def test_create_item(self):
        """"
        test item can be created
        """
        with self.client:
            token = self.token()
            self.create_list('Travel', 'Visit places', token)
            response = self.create_item('Go_to_Nairobi', '5000', token)
            data = json.loads(response.data.decode())
            self.assertTrue(data['message'], 'Shopping list item has been created')
            self.assertEqual(response.status_code, 201)
            self.assertIn('Go_to_Nairobi', response.data.decode())

    def test_create_item_with_wrong_content_type(self):
        """"
        test item can not be created with wrong content type
        """
        with self.client:
            token = self.token()

            self.create_list('Travel', 'Visit places', token)
            self.create_item('Go_to_Nairobi', '5000', token)
            response = self.create_item_with_wrong_content_type('Go_to_Nairobi', '5000', token)
            data = json.loads(response.data.decode())
            self.assertTrue(data['message'], 'Content-type must be json')
            self.assertEqual(response.status_code, 202)
            self.assertIn('Content-type must be json', response.data.decode())

    def test_create_item_with_empty_name(self):
        """"
        test item can not be created with empty item name
        """
        with self.client:
            token = self.token()

            self.create_list('Travel', 'Visit places', token)
            response = self.create_item('', '5000', token)
            data = json.loads(response.data.decode())
            self.assertTrue(data['message'], 'No name has been input')
            self.assertEqual(response.status_code, 400)
            self.assertIn('No name has been input', response.data.decode())

    def test_create_item_with_name_containing_spaces(self):
        """"
        test item cant be created with invalid item name format
        """
        with self.client:
            token = self.token()

            self.create_list('Travel', 'Visit places', token)
            response = self.create_item('Go to Nairobi', '5000', token)
            data = json.loads(response.data.decode())
            self.assertTrue(data['message'], 'Wrong name format. Name can only contain letters and number')
            self.assertEqual(response.status_code, 406)
            self.assertIn('Wrong name format. Name can only contain letters and numbers', response.data.decode())

    def test_create_item_with_name_containing_special_characters(self):
        """"
        test item cant be created with invalid item name format
        """
        with self.client:
            token = self.token()

            self.create_list('Travel', 'Visit places', token)
            response = self.create_item('Nairobi!!!', '5000', token)
            data = json.loads(response.data.decode())
            self.assertTrue(data['message'], 'Wrong name format. Name can only contain letters and number')
            self.assertEqual(response.status_code, 406)
            self.assertIn('Wrong name format. Name can only contain letters and numbers', response.data.decode())

    def test_create_item_with_string_price(self):
        """"
        test item cant be created if input price is a string
        """
        with self.client:
            token = self.token()

            self.create_list('Travel', 'Visit places', token)
            response = self.create_item('Go_to_Nairobi', '5000ugx', token)
            data = json.loads(response.data.decode())
            self.assertTrue(data['message'], 'Item price should be an integer')
            self.assertEqual(response.status_code, 400)
            self.assertIn('Item price should be an integer', response.data.decode())

    def test_get_items(self):
        """"
        test API can get items in a list
        """
        with self.client:
            token = self.token()

            self.create_list('Travel', 'Visit places', token)
            self.create_item('Go_to_Nairobi', '5000', token)

            response = self.client.get('/v1/shoppinglist/1/items/',
                                       content_type='application/json',
                                       headers=dict(Authorization='Bearer ' + token))
            data = json.loads(response.data.decode())
            self.assertTrue(data['status'], 'success')
            self.assertEqual(response.status_code, 200)

    def test_search(self):
        """"
        test API can search items
        """
        with self.client:
            token = self.token()

            self.create_list('Travel', 'Visit places', token)
            self.create_item('Go_to_Nairobi', '5000', token)

            response = self.client.get('/v1/shoppinglist/1/items/?q=Go_to_Nairobi',
                                       content_type='application/json',
                                       headers=dict(Authorization='Bearer ' + token))

            self.assertEqual(response.status_code, 200)
            self.assertIn('Go_to_Nairobi', response.data.decode())

    def test_pagination(self):
        """"
        test API can get a specific number of items
        """
        with self.client:
            token = self.token()

            self.create_list('Travel', 'Visit places', token)
            self.create_item('Go_to_Nairobi', '5000', token)
            self.create_item('Shoes', '5000', token)

            response = self.client.get('/v1/shoppinglist/1/items/?limit=1',
                                       content_type='application/json',
                                       headers=dict(Authorization='Bearer ' + token))

            self.assertEqual(response.status_code, 200)
            self.assertIn('success', response.data.decode())

    def test_pagination_with_non_integer_input(self):
        """"
        test API can get a specific number of items
        """
        with self.client:
            token = self.token()

            self.create_list('Travel', 'Visit places', token)
            self.create_item('Go_to_Nairobi', '5000', token)

            response = self.client.get('/v1/shoppinglist/1/items/?limit=one',
                                       content_type='application/json',
                                       headers=dict(Authorization='Bearer ' + token))

            self.assertEqual(response.status_code, 400)
            self.assertIn('Limit should be an integer', response.data.decode())

    def test_get_item(self):
        """"
        test API can get single item in a list
        """
        with self.client:
            token = self.token()

            self.create_list('Travel', 'Visit places', token)
            self.create_item('Go_to_Nairobi', '5000', token)

            response = self.client.get('/v1/shoppinglist/1/items/1',
                                       content_type='application/json',
                                       headers=dict(Authorization='Bearer ' + token))

            self.assertEqual(response.status_code, 200)

    def test_get_nonexistent_item(self):
        """"
        test API cant get non existent item from a list
        """
        with self.client:
            token = self.token()

            self.create_list('Travel', 'Visit places', token)
            # self.create_item('Go_to_Nairobi', '5000', token)
            response = self.client.get('/v1/shoppinglist/1/items/45',
                                       content_type='application/json',
                                       headers=dict(Authorization='Bearer ' + token))

            self.assertEqual(response.status_code, 404)
            data = json.loads(response.data.decode())
            self.assertTrue(data['message'], 'Item not found')
            self.assertIn('Item not found', response.data.decode())

    def test_get_item_with_invalid_id(self):
        """"
        test API cant get non existent item from a list
        """
        with self.client:
            token = self.token()

            self.create_list('Travel', 'Visit places', token)
            response = self.client.get('/v1/shoppinglist/1/items/45asd',
                                       content_type='application/json',
                                       headers=dict(Authorization='Bearer ' + token))

            self.assertEqual(response.status_code, 400)
            data = json.loads(response.data.decode())
            self.assertTrue(data['message'], 'Please provide a valid item or list Id')
            self.assertIn('Please provide a valid item or list Id', response.data.decode())

    def test_edit_item_with_invalid_id(self):
        """"
        test API cant get non existent item from a list
        """
        with self.client:
            token = self.token()

            self.create_list('Travel', 'Visit places', token)
            response = self.client.put('/v1/shoppinglist/1/items/45asd',
                                       content_type='application/json',
                                       headers=dict(Authorization='Bearer ' + token))

            self.assertEqual(response.status_code, 400)
            data = json.loads(response.data.decode())
            self.assertTrue(data['message'], 'Please provide a valid item Id')
            self.assertIn('Please provide a valid item or list Id', response.data.decode())

    def test_delete_item_that_doesnt_exist(self):
        """Should return 404 for missing item"""
        with self.client:
            token = self.token()
            response = self.client.delete('/v1/shoppinglist/1/items/47',
                                          content_type='application/json',
                                          headers=dict(Authorization='Bearer ' + token))
            self.assertEqual(response.status_code, 404)
            data = json.loads(response.data.decode())
            self.assertTrue(data['message'], 'Item not found')
            self.assertTrue(data['status'], 'failed')
            self.assertIn('Item not found', response.data.decode())

    def test_delete_item(self):
        """Should return 200 for success"""
        with self.client:
            token = self.token()
            self.create_list('Travel', 'Visit places', token)
            self.create_item('Go_to_Nairobi', '5000', token)

            response = self.client.delete('/v1/shoppinglist/1/items/1',
                                          content_type='application/json',
                                          headers=dict(Authorization='Bearer ' + token))

            self.assertEqual(response.status_code, 200)
            data = json.loads(response.data.decode())
            self.assertTrue(data['message'], 'Shopping list item has been deleted')
            self.assertTrue(data['status'], 'success')
            self.assertIn('Shopping list item has been deleted', response.data.decode())

    def test_delete_item_with_invalid_id(self):
        """Should return 200 for success"""
        with self.client:
            token = self.token()
            self.create_list('Travel', 'Visit places', token)
            self.create_item('Go_to_Nairobi', '5000', token)

            response = self.client.delete('/v1/shoppinglist/1/items/sadf',
                                          content_type='application/json',
                                          headers=dict(Authorization='Bearer ' + token))

            self.assertEqual(response.status_code, 400)
            data = json.loads(response.data.decode())
            self.assertTrue(data['message'], 'Please provide a valid item Id')
            self.assertTrue(data['status'], 'failed')
            self.assertIn('Please provide a valid item or list Id', response.data.decode())

    def test_delete_item_with_wrong_content_type(self):
        """Should return 200 for success"""
        with self.client:
            token = self.token()
            self.create_list('Travel', 'Visit places', token)
            self.create_item('Go_to_Nairobi', '5000', token)

            response = self.client.delete('/v1/shoppinglist/1/items/1',
                                          content_type='application/javascript',
                                          headers=dict(Authorization='Bearer ' + token))

            self.assertEqual(response.status_code, 202)
            data = json.loads(response.data.decode())
            self.assertTrue(data['status'], 'failed')
            self.assertIn('Content-type must be json', response.data.decode())

    def test_edit_item_(self):
        """Should return 200 for success"""
        with self.client:
            token = self.token()
            self.create_list('Travel', 'Visit places', token)
            self.create_item('Go_to_Nairobi', '5000', token)
            response = self.edit_item('Travelling_bag', '5000', token)

            self.assertEqual(response.status_code, 200)
            data = json.loads(response.data.decode())
            self.assertTrue(data['status'], 'success')
            self.assertIn('Shopping list item has been edited', response.data.decode())

    def test_edit_non_existent_item(self):
        """Should return 200 for success"""
        with self.client:
            token = self.token()
            self.create_list('Travel', 'Visit places', token)
            self.create_item('Go_to_Nairobi', '5000', token)
            new_item = json.dumps({
                'name': 'Travelling_bag',
                'price': '5000'
            })

            response = self.client.put('/v1/shoppinglist/1/items/56', data=new_item,
                                       content_type='application/json',
                                       headers=dict(Authorization='Bearer ' + token))

            self.assertEqual(response.status_code, 404)
            data = json.loads(response.data.decode())
            self.assertTrue(data['status'], 'failed')
            self.assertIn('Shopping list item does not exist. Please try again', response.data.decode())

    def test_edit_item_with_wrong_content_type(self):
        """Should return 200 for success"""
        with self.client:
            token = self.token()
            self.create_list('Travel', 'Visit places', token)
            self.create_item('Go_to_Nairobi', '5000', token)
            new_item = json.dumps({
                'name': 'Travelling_bag',
                'price': '5000'
            })

            response = self.client.put('/v1/shoppinglist/1/items/1', data=new_item,
                                       content_type='application/javascript',
                                       headers=dict(Authorization='Bearer ' + token))

            self.assertEqual(response.status_code, 202)
            data = json.loads(response.data.decode())
            self.assertTrue(data['status'], 'failed')
            self.assertIn('Content-type must be json', response.data.decode())

    def test_edit_item_with_empty_name(self):
        """Should return 200 for success"""
        with self.client:
            token = self.token()
            self.create_list('Travel', 'Visit places', token)
            self.create_item('Go_to_Nairobi', '5000', token)
            response = self.edit_item('', '5000', token)
            self.assertEqual(response.status_code, 400)
            data = json.loads(response.data.decode())
            self.assertTrue(data['status'], 'failed')
            self.assertIn('No name input. Try again', response.data.decode())

    def test_edit_item_with_name_containing_spaces(self):
        """Should return 200 for success"""
        with self.client:
            token = self.token()
            self.create_list('Travel', 'Visit places', token)
            self.create_item('Go_to_Nairobi', '5000', token)
            response = self.edit_item('Going to Mombasa', '5000', token)
            self.assertEqual(response.status_code, 406)
            data = json.loads(response.data.decode())
            self.assertTrue(data['status'], 'failed')
            self.assertIn('Wrong name format. Name can only contain letters and numbers', response.data.decode())

    def test_edit_item_with_string_price(self):
        """Should return 200 for success"""
        with self.client:
            token = self.token()
            self.create_list('Travel', 'Visit places', token)
            self.create_item('Go_to_Nairobi', '5000', token)
            response = self.edit_item('Travelling_bag', '5000ugx', token)
            self.assertEqual(response.status_code, 400)
            data = json.loads(response.data.decode())
            self.assertTrue(data['status'], 'failed')
            self.assertIn('Item price should be an integer', response.data.decode())


if __name__ == '__main__':
    unittest.main()
