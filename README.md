# Shopping List API
[![Coverage Status](https://coveralls.io/repos/github/CeciliaCaroline/shoppinglist_api/badge.svg?branch=master)](https://coveralls.io/github/CeciliaCaroline/shoppinglist_api?branch=master)
[![Codacy Badge](https://api.codacy.com/project/badge/Grade/4013dca21e4349008e56ca415adbe4c3)](https://www.codacy.com/app/CeciliaCaroline/shoppinglist_api?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=CeciliaCaroline/shoppinglist_api&amp;utm_campaign=Badge_Grade)
[![Build Status](https://travis-ci.org/CeciliaCaroline/shoppinglist_api.svg?branch=master)](https://travis-ci.org/CeciliaCaroline/shoppinglist_api)
[![BCH compliance](https://bettercodehub.com/edge/badge/CeciliaCaroline/shoppinglist_api?branch=master)](https://bettercodehub.com/)

This API enables the user to keep track their shopping lists. This api has end points that allow the user to create, update, delete and get their shopping lists. Also, users can also add, edit, delete and get items for particular shopping lists.

## Requirements

Shopping list api is an application that utilises the flask framework. The app has been tested for python 3.6 and uses the PostgreSQL database

## Setup
Clone this repository as shown below;
```
https://github.com/CeciliaCaroline/shoppinglist_api.git
```
 Create the virtual environment and activate it
 
 ```
 virtualenv env
 source env/bin/activate
```

Then install all the required dependencies

```
pip install -r requirements.txt
```
Create the database and run migrations
```
$ python manage.py db init
```

```
$ python manage.py db migrate
```
```
$ python manage.py db upgrade
```

All done! Now, start your server by running ```python run.py```. For best experience, use a GUI platform like postman to make requests to the api.


This API enables the user to keep track their shopping lists
## Features
Endpoint | Functionality
------------ | -------------
POST /auth/login |Logs a user in
POST /auth/register | Registers a user
POST /shoppinglists/ | Creates a new shopping list
GET /shoppinglists/ | Lists all created shopping lists
GET /shoppinglists/id | Gets a single shopping list with the suppled id 
PUT /shoppinglists/id | Updates a shopping list with the suppled id
DELETE /shoppinglists/id | Deletes a shopping list with the suppled id
POST /shoppinglists/id/items/ | Creates a new item in a shopping list whose id is supplied
GET /shoppinglists/id/items/item_id | Get a single shopping list item
PUT /shoppinglists/id/items/item_id | Updates a shopping list item
DELETE /shoppinglists/id/items/item_id | Deletes an item in a shopping list

### Pagination

The api supports pagination so users can specify the number of results they would
like to have via a GET parameter ```limit```. By default, the application displays a maximum of 10 lists/items on page 1.

`GET http://localhost:/shoppinglists?limit=15`

This returns 15 shopping lists for the logged in user.

### Searching

It is possible to search shoppinglists using the parameter `q` in the GET request. 

`GET http://localhost:/shoppinglists?q=clothes`

This request will return all shoppinglists with `clothes` in their name