import json
# from app.shoppinglists import shop_list
import unittest

from tests.base_test import BaseTestCase


class TestShoppingList(BaseTestCase):
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

    def create_list_with_wrong_request_content_type(self, name, description):
        """
        Helper method to create a list using a wrong content-type
        :param name
        :param description
        :return:
        """
        return self.client.post(
            '/v1/shoppinglist/',
            content_type='application/javascript',
            data=json.dumps(dict(name=name, description=description)))

    def test_create_shoppinglist(self):
        """Test API can create a shoppinglist """

        with self.client:
            res = self.create_list('travel', 'Go to Kenya', self.token())
            data = json.loads(res.data.decode())
            self.assertTrue(data['name'], 'travel')
            self.assertTrue(data['description'], 'Go to Kenya')
            self.assertTrue(data['message'], 'Shopping list has been created')
            self.assertEqual(res.status_code, 201)
            self.assertIn('Go to Kenya', str(res.data))
            # return data

    def test_create_shoppinglist_with_name_containing_special_characters(self):
        """Test API can create a shoppinglist """

        with self.client:
            res = self.create_list('travel!!!', 'Go to Kenya', self.token())
            data = json.loads(res.data.decode())
            self.assertTrue(data['message'], 'Wrong name format. Name can only contain letters and numbers')
            self.assertTrue(data['status'], 'failed')
            self.assertEqual(res.status_code, 400)

    def test_create_shoppinglist_with_name_containing_spaces(self):
        """Test API can create a shoppinglist """

        with self.client:
            res = self.create_list('travel the world', 'Go to Kenya', self.token())
            data = json.loads(res.data.decode())
            self.assertTrue(data['message'], 'Wrong name format. Name can only contain letters and numbers')
            self.assertTrue(data['status'], 'failed')
            self.assertEqual(res.status_code, 400)

    def test_create_shoppinglist_with_empty_name_or_description(self):
        """Test API can create a shoppinglist """

        with self.client:
            res = self.create_list('', '', self.token())
            data = json.loads(res.data.decode())
            self.assertTrue(data['message'], 'No name or description input. Try again')
            self.assertTrue(data['status'], 'failed')
            self.assertEqual(res.status_code, 406)

    def test_create_list_with_wrong_content_type(self):
        """"
        Test API can not create a list with a wrong content type
        """
        with self.client:
            response = self.create_list_with_wrong_request_content_type('travel', 'Go to Kenya')
            data = json.loads(response.data.decode())
            self.assertTrue(data['message'], 'Content-type must be json')
            self.assertTrue(data['status'], 'failed')
            self.assertEqual(response.status_code, 401)

    def test_get_shopping_lists(self):
        """"
        Test API can get all shopping lists
        """
        with self.client:
            token = self.token()
            self.create_list('travel', 'Go to Kenya', token)
            response = self.client.get(
                '/v1/shoppinglist/',
                content_type='application/json',
                headers=dict(Authorization="Bearer " + token),
            )
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 200)
            self.assertEqual(data['status'], 'success')
            self.assertIn('Shoppinglists', response.data.decode())

    def test_edit_list_with_wrong_content_type(self):
        """"
        Test API can get all shopping lists
        """
        with self.client:
            token = self.token()
            res = self.create_list('eat', 'eatpraylove', token)
            self.assertEqual(res.status_code, 201)
            # get the json with the shoppinglist
            results = json.loads(res.data.decode())

            # then, we edit the created shoppinglist by making a PUT request
            response = self.client.put(
                '/v1/shoppinglist/{}'.format(results['id']),
                headers=dict(Authorization="Bearer " + token),
                content_type='application/javascript',
                data=json.dumps(dict(name='traveling', description='traveling to different places')))

            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 202)
            self.assertEqual(data['status'], 'failed')
            self.assertTrue(data['message'], 'Content-type must be json')

    def test_search(self):
        """"
        test API can search lists
        """
        with self.client:
            token = self.token()

            self.create_list('Travel', 'Visit places', token)

            response = self.client.get('/v1/shoppinglist/?q=Travel',
                                       content_type='application/json',
                                       headers=dict(Authorization='Bearer ' + token))

            self.assertEqual(response.status_code, 200)
            self.assertIn('Travel', response.data.decode())

    def test_search_nonexistent_list(self):
        """"
        test API can search lists
        """
        with self.client:
            token = self.token()

            self.create_list('Travel', 'Visit places', token)

            response = self.client.get('/v1/shoppinglist/?q=Travelling',
                                       content_type='application/json',
                                       headers=dict(Authorization='Bearer ' + token))

            self.assertEqual(response.status_code, 404)
            data = json.loads(response.data.decode())
            self.assertEqual(data['status'], 'failed')
            self.assertTrue(data['message'], 'Shopping list not found')

    def test_pagination(self):
        """"
        test API can get a specific number of lists
        """
        with self.client:
            token = self.token()

            self.create_list('Travel', 'Visit places', token)
            self.create_list('Health', 'Excercises', token)

            response = self.client.get('/v1/shoppinglist/?limit=1',
                                       content_type='application/json',
                                       headers=dict(Authorization='Bearer ' + token))

            self.assertEqual(response.status_code, 200)
            self.assertIn('success', response.data.decode())

    def test_pagination_with_non_integer_input(self):
        """"
        test API can get a specific number of lists
        """
        with self.client:
            token = self.token()

            self.create_list('Travel', 'Visit places', token)
            self.create_list('Health', 'Excercises', token)

            response = self.client.get('/v1/shoppinglist/?limit=one',
                                       content_type='application/json',
                                       headers=dict(Authorization='Bearer ' + token))

            self.assertEqual(response.status_code, 400)
            self.assertIn('Limit should be an integer', response.data.decode())

    def test_get_single_shopping_list(self):
        with self.client:
            token = self.token()
            res = self.create_list('travel', 'Go to Kenya', token)
            results = json.loads(res.data.decode())

            response = self.client.get(
                '/v1/shoppinglist/{}'.format(results['id']),
                content_type='application/json',
                headers=dict(Authorization="Bearer " + token)
            )
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 200)
            self.assertEqual(data['status'], 'success')

    def test_get_single_shopping_list_with_wrong_content_type(self):
        with self.client:
            token = self.token()
            res = self.create_list('travel', 'Go to Kenya', token)
            results = json.loads(res.data.decode())

            response = self.client.get(
                '/v1/shoppinglist/{}'.format(results['id']),
                content_type='application/java',
                headers=dict(Authorization="Bearer " + token)
            )
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 202)
            self.assertEqual(data['message'], 'Content-type must be json')
            self.assertEqual(data['status'], 'failed')

    def test_get_list_doesnt_exist(self):
        with self.client:
            token = self.token()
            response = self.client.get(
                '/v1/shoppinglist/32',
                content_type='application/json',
                headers=dict(Authorization="Bearer " + token)
            )
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 404)
            self.assertEqual(data['status'], 'failed')
            self.assertEqual(data['message'], 'Shopping list not found')

    def test_get_list_with_invalid_id(self):
        with self.client:
            token = self.token()
            response = self.client.get(
                '/v1/shoppinglist/32a',
                content_type='application/json',
                headers=dict(Authorization="Bearer " + token)
            )
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 400)
            self.assertEqual(data['status'], 'failed')
            self.assertEqual(data['message'], 'Please provide a valid ShoppingList Id')

    def test_edit_list_with_invalid_id(self):
        with self.client:
            token = self.token()
            response = self.client.put(
                '/v1/shoppinglist/32a',
                content_type='application/json',
                headers=dict(Authorization="Bearer " + token)
            )
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 400)
            self.assertEqual(data['status'], 'failed')
            self.assertEqual(data['message'], 'Please provide a valid ShoppingList Id')

    def test_delete_list_with_invalid_id(self):
        with self.client:
            token = self.token()
            response = self.client.delete(
                '/v1/shoppinglist/32a',
                content_type='application/json',
                headers=dict(Authorization="Bearer " + token)
            )
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 400)
            self.assertEqual(data['status'], 'failed')
            self.assertEqual(data['message'], 'Please provide a valid ShoppingList Id')

    def test_edit_list_that_doesnt_exist(self):
        with self.client:
            token = self.token()
            response = self.client.put(
                '/v1/shoppinglist/32',
                content_type='application/json',
                headers=dict(Authorization="Bearer " + token),
                data=json.dumps(dict(name='traveling', description='traveling to different places')))

            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 404)
            self.assertEqual(data['status'], 'failed')
            self.assertEqual(data['message'], 'Shopping list does not exist. Please try again')

    def test_delete_list_that_doesnt_exist(self):
        with self.client:
            token = self.token()
            rv = self.client.delete(
                '/v1/shoppinglist/25',
                headers=dict(Authorization="Bearer " + token),
                content_type='application/json')

            self.assertEqual(rv.status_code, 404)
            data = json.loads(rv.data.decode())
            self.assertEqual(data['message'], 'Shopping list not found')

    def test_shoppinglist_can_be_edited(self):
        """Test API can edit an existing shoppinglist. (PUT request)"""
        with self.client:
            token = self.token()
            res = self.create_list('eat', 'eatpraylove', token)
            self.assertEqual(res.status_code, 201)
            # get the json with the shoppinglist
            results = json.loads(res.data.decode())

            # then, we edit the created shoppinglist by making a PUT request
            rv = self.client.put(
                '/v1/shoppinglist/{}'.format(results['id']),
                headers=dict(Authorization="Bearer " + token),
                content_type='application/json',
                data=json.dumps(dict(name='traveling', description='traveling to different places')))
            # print(rv.data)
            data = json.loads(rv.data.decode())
            self.assertEqual(rv.status_code, 200)
            self.assertEqual(data['message'], 'Shopping list has been updated')

            # finally, we get the edited shoppinglist to see if it is actually edited.
            results = self.client.get(
                '/v1/shoppinglist/{}'.format(results['id']),
                content_type='application/json',
                headers=dict(Authorization="Bearer " + token))

            self.assertIn('traveling to different places', str(results.data))

    def test_edit_shoppinglist_with_no_name(self):
        """Test API can edit an existing shoppinglist. (PUT request)"""
        with self.client:
            token = self.token()
            res = self.create_list('eat', 'eatpraylove', token)
            self.assertEqual(res.status_code, 201)
            # get the json with the shoppinglist
            results = json.loads(res.data.decode())

            # then, we edit the created shoppinglist by making a PUT request
            rv = self.client.put(
                '/v1/shoppinglist/{}'.format(results['id']),
                headers=dict(Authorization="Bearer " + token),
                content_type='application/json',
                data=json.dumps(dict(name='', description='traveling to different places')))
            # print(rv.data)
            data = json.loads(rv.data.decode())
            self.assertEqual(rv.status_code, 400)
            self.assertEqual(data['message'], 'No name input. Try again')
            self.assertEqual(data['status'], 'failed')

    def test_shoppinglist_delete(self):
        """"
        Test API can delete shopping list using a DELETE request
        """
        with self.client:
            token = self.token()
            res = self.create_list('eat', 'eatpraylove', token)
            self.assertEqual(res.status_code, 201)
            # get the json with the shoppinglist
            results = json.loads(res.data.decode())

            # then, we delete the created shoppinglist by making a DELETE request
            rv = self.client.delete(
                '/v1/shoppinglist/{}'.format(results['id']),
                headers=dict(Authorization="Bearer " + token),
                content_type='application/json')
            self.assertEqual(rv.status_code, 200)
            data = json.loads(rv.data.decode())
            self.assertEqual(data['message'], 'Shopping list has been deleted')

    def test_shoppinglist_delete_with_wrong_content_type(self):
        """"
        Test API can delete shopping list using a DELETE request
        """
        with self.client:
            token = self.token()
            res = self.create_list('eat', 'eatpraylove', token)
            self.assertEqual(res.status_code, 201)
            # get the json with the shoppinglist
            results = json.loads(res.data.decode())

            # then, we delete the created shoppinglist by making a DELETE request
            rv = self.client.delete(
                '/v1/shoppinglist/{}'.format(results['id']),
                headers=dict(Authorization="Bearer " + token),
                content_type='application/javascript')
            self.assertEqual(rv.status_code, 202)
            data = json.loads(rv.data.decode())
            self.assertEqual(data['message'], 'Content-type must be json')
            self.assertEqual(data['status'], 'failed')


if __name__ == '__main__':
    unittest.main()
