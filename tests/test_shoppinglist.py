from tests.base_test import BaseTestCase
import unittest
import json


class TestShoppingList(BaseTestCase):
    def create_list(self, name, description, token):
        """
        Helper method for creating a list with dummy data
        :return:
        """
        return self.client.post(
            '/shoppinglist',
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
            '/shoppinglist',
            content_type='application/javascript',
            data=json.dumps(dict(name=name, description=description)))

    def test_create_shoppinglist(self):
        """Test API can create a shoppinglist """

        with self.client:
            res = self.create_list('travel', 'Go to Kenya', self.token())
            data = json.loads(res.data.decode())
            self.assertTrue(data['name'], 'travel')
            self.assertTrue(data['description'], 'Go to Kenya')
            self.assertEqual(res.status_code, 201)
            self.assertIn('Go to Kenya', str(res.data))
            return data

    def test_create_shoppinglist_with_invalid_name(self):
        """Test API can create a shoppinglist """

        with self.client:
            res = self.create_list('travel!!!', 'Go to Kenya', self.token())
            self.assertEqual(res.status_code, 406)

    def test_create_shoppinglist_with_empty_name_or_description(self):
        """Test API can create a shoppinglist """

        with self.client:
            res = self.create_list(' ', 'Go to Kenya', self.token())
            self.assertEqual(res.status_code, 406)

    def test_create_list_with_wrong_content_type(self):
        """"
        Test API can not create a list with a wrong content type
        """
        with self.client:
            response = self.create_list_with_wrong_request_content_type('travel', 'Go to Kenya')
            self.assertEqual(response.status_code, 401)

    def test_get_shopping_list(self):
        """"
        Test API can get all shopping lists
        """
        with self.client:
            token = self.token()
            self.create_list('travel', 'Go to Kenya', token)
            response = self.client.get(
                '/shoppinglist',
                content_type='application/json',
                headers=dict(Authorization="Bearer " + token),
            )
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 200)
            self.assertEqual(data['status'], 'success')

    def test_search(self):
        """"
        test API can search lists
        """
        with self.client:
            token = self.token()

            self.create_list('Travel', 'Visit places', token)

            response = self.client.get('/shoppinglist?q=Travel',
                                       content_type='application/json',
                                       headers=dict(Authorization='Bearer ' + token))

            self.assertEqual(response.status_code, 200)
            self.assertIn('Travel', response.data.decode())

    def test_pagination(self):
        """"
        test API can get a specific number of lists
        """
        with self.client:
            token = self.token()

            self.create_list('Travel', 'Visit places', token)
            self.create_list('Health', 'Excercises', token)

            response = self.client.get('/shoppinglist?limit=1',
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

            response = self.client.get('/shoppinglist?limit=one',
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
                '/shoppinglist/{}'.format(results['id']),
                content_type='application/json',
                headers=dict(Authorization="Bearer " + token)
            )
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 200)
            self.assertEqual(data['status'], 'success')

    def test_get_list_doesnt_exist(self):
        with self.client:
            token = self.token()
            response = self.client.get(
                '/shoppinglist/32',
                content_type='application/json',
                headers=dict(Authorization="Bearer " + token)
            )
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 404)
            self.assertEqual(data['status'], 'failed')
            self.assertEqual(data['message'], 'Shopping list not found')

    def test_edit_list_that_doesnt_exist(self):
        with self.client:
            token = self.token()
            response = self.client.put(
                '/shoppinglist/32',
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
                '/shoppinglist/25',
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
                '/shoppinglist/{}'.format(results['id']),
                headers=dict(Authorization="Bearer " + token),
                content_type='application/json',
                data=json.dumps(dict(name='traveling', description='traveling to different places')))
            # print(rv.data)
            self.assertEqual(rv.status_code, 200)

            # finally, we get the edited shoppinglist to see if it is actually edited.
            results = self.client.get(
                '/shoppinglist/{}'.format(results['id']),
                content_type='application/json',
                headers=dict(Authorization="Bearer " + token))
            self.assertIn('traveling to different places', str(results.data))

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
                '/shoppinglist/{}'.format(results['id']),
                headers=dict(Authorization="Bearer " + token),
                content_type='application/json')
            self.assertEqual(rv.status_code, 200)


if __name__ == '__main__':
    unittest.main()
