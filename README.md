# Shopping List API
[![Coverage Status](https://coveralls.io/repos/github/CeciliaCaroline/shoppinglist_api/badge.svg?branch=master)](https://coveralls.io/github/CeciliaCaroline/shoppinglist_api?branch=master)
[![Codacy Badge](https://api.codacy.com/project/badge/Grade/4013dca21e4349008e56ca415adbe4c3)](https://www.codacy.com/app/CeciliaCaroline/shoppinglist_api?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=CeciliaCaroline/shoppinglist_api&amp;utm_campaign=Badge_Grade)
[![Build Status](https://travis-ci.org/CeciliaCaroline/shoppinglist_api.svg?branch=master)](https://travis-ci.org/CeciliaCaroline/shoppinglist_api)
[![BCH compliance](https://bettercodehub.com/edge/badge/CeciliaCaroline/shoppinglist_api?branch=master)](https://bettercodehub.com/)

This API enables the user to keep track their shopping lists
## Features
- Register / Login
- Create shopping list
- View shopping list
- Update shopping list
- Delete shopping list

## Usage

#### Registration
#### Log in
#### CRUD for shopping list
#### CRUD for shopping list items

This API enables the user to keep track their shopping lists
## Features
- User Register / Login
- CRUD for shopping list
- CRUD for shopping list items


## Usage

#### Registration
Returns json data about a user that has been registered.

-  URL: ```/auth/register```
- Method: ```POST```
- Params
````
Content :{'email': 'caroline@gmail.com', }
````
- Success Response:
```Code: 201 
Content: { 'status' : 'success', 'message' : 'Successfully registered', 'token':'qawscghfhfhjhgjlljjnljjdo' }
```
- Error Response:
```
Code: 202 
Content: { message : 'Failed, User already exists, Please try again' }
```
or
```
Code: 202  
Content: { message : 'Missing or wrong email format or password is less than four characters' }
```
#### Log In

- URL: ```/auth/login```
- Method: ```POST```
- Params
````
Content :{'email': 'caroline@gmail.com', }
````
- Success Response:
```Code: 201 
Content: { 'status' : 'success', 'message' : 'Successfully logged in', 'token':'qawscghfhfhjhgjlljjnljjdo' }
```
- Error Response:
```
Code: 202 
Content: { 'status' : 'success', message : 'Failed, User does not exists, Please try again' }
```
or
```
Code: 202  
Content: { 'status' : 'success', message : 'Missing or wrong email format or password is less than four characters' }
```

#### CRUD for shopping list
##### Create list
- URL: ```/shoppinglist```
- Method: ```POST```
- Params
````
Content :{'name': 'food', 'description': 'Buy food stuff' }
````
- Success Response:
```Code: 201 
Content: { 'id' : '1', 'name': 'food', 'description': 'Buy food stuff','message' : 'Shopping list has been created'}
```
##### View lists
- URL: ```/shoppinglist```
- Method: ```GET```
- Success Response:
```Code: 200 
Content: { 'id' : '1', 'name': 'food', 'description': 'Buy food stuff','status' : 'success'}
```
##### Update list
- URL: ```/shoppinglist/1```
- Method: ```PUT```
- Params
````
Content :{'name': 'food', 'description': 'Buy chicken' }
````
- Success Response:
```Code: 200 
Content: { 'id' : '1', 'name': 'food', 'description': 'Buy chicken','message' : 'Shopping list has been updated'}
```
##### Delete list
- URL: ```/shoppinglist/1```
- Method: ```DELETE```

- Success Response:
```Code: 200 
Content: {'message': 'Shopping list has been deleted'}
```

#### CRUD for shopping list items
##### Create item
- URL: ```/shoppinglist/1/item```
- Method: ```POST```
- Params
````
Content :{'name': 'food', 'price': '25 dollars' }
````
- Success Response:
```Code: 201 
Content: { 'id' : '1', 'name': 'food', 'price': '25 dollars','message' : 'Shopping list item has been created'}
```
##### View item
- URL: ```/shoppinglist/1/items```
- Method: ```GET```

- Success Response:
```Code: 200 
Content: { 'id' : '1', 'name': 'food', 'price': '25 dollars','status' : 'success'}
```
##### Update item
- URL: ```/shoppinglist/1/items/1```
- Method: ```PUT```
- Params
````
Content :{'name': chicken', 'price': '12 dollars' }
````
- Success Response:
```Code: 200 
Content: { 'id' : '1', 'name': 'food', 'price': '12 dollars','message' : 'Shopping list item has been updated'}
```
##### Delete list
- URL: ```/shoppinglist/1/items/1```
- Method: ```DELETE```

- Success Response:
```Code: 200 
Content: {'message': 'Shopping list item has been deleted'}
```
