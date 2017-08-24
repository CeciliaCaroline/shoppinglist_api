# Shopping List API

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
OR
```
Code: 202  
Content: { message : 'Missing or wrong email format or password is less than four characters' }
```
#### Log in

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
OR
```
Code: 202  
Content: { 'status' : 'success', message : 'Missing or wrong email format or password is less than four characters' }
```

#### CRUD for shopping list
#### CRUD for shopping list items
