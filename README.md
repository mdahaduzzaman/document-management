# README

# LIVE LINK

## OPEN IN YOUR BROWSER [https://documents-management.nkftcl.com/] 

Welcome to DOCUMENT MANAGEMENT.
The main goal of this project is to create a new user login this user and the logged in the user can create a document object and share this document with some other user of this current project and can provide some permission like can_view and can_edit. If the shared user have the permission to view then they can view this document object if have the permission to can edit then the user can also edit this document but can't add or delete shared user.

Start by cloning the repositories:

```
git clone https://github.com/mdahaduzzaman/document-management.git
```

Then create a new virtual environment for not conflicting with others project

```
py -m venv .env_document
```

Activate the virtual environment by using the following command


For Windows

```
.env_document\Scripts\activate
```

For Mac or Linux

```
source .env_document/bin/activate
```

Install all the dependencies by using the following command

```
pip install -r requirements.txt
```

Then run the following command to start the server
```
python manage.py runserver
```

### All credentials

```
Superuser
username: admin 
password: admin
```

The development server will start at [localhost](http://127.0.0.1:8000/) by Default

# API ENDPOINTS

These endpoints allow you to register user, jwt token for user, jwt refresh token for user, GET all documents, single document, put and patch documents where each document contains multiple it's shared person with their permission

## GET [http://127.0.0.1:8000/] 

### check that server is in the running state or not

`response` 200 OK ✅

```
{
  "message": "Server is up and running"
}
```

### these are the auto documentation endpoint genererated by openai and swagger
### you can check this following endpoint in your browser

## GET [http://127.0.0.1:8000/redoc/] 
## GET [http://127.0.0.1:8000/swagger/] 
## GET [http://127.0.0.1:8000/swagger<format>/] 

# PROJECT CUSTOM ROUTES

## POST [http://127.0.0.1:8000/api/v1/users/register/] 

### register a new user so that we can perform operation

payloads

```
{
  "email": "abc@gmail.com",
  "username": "abc",
  "first_name": "Abc",
  "last_name": "Def",
  "password": "12345678",
  "confirm_password": "12345678"
}

```

`response` 201 CREATED ✅

```
{
  "id": 2,
  "email": "abc@gmail.com",
  "username": "abc",
  "first_name": "Abc",
  "last_name": "Def"
}
```

else 

`response` 404 BAD REQUEST 

## POST [http://127.0.0.1:8000/api/v1/users/token/] 

### get a new token for this user so that this user can have access of resources

payloads

```
{
  "username": "abc",
  "password": "12345678"
}
```

`response` 200 OK ✅

```
{
  "refresh": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTcxMTQ5MzQ3MSwiaWF0IjoxNzExNDA3MDcxLCJqdGkiOiI0ZGEzMTg0MjAzNmY0MDQyYTI0ZTVhMmM4ODcyNDU0YyIsInVzZXJfaWQiOjJ9.GGFRq_dxqRjCcjL9zBuA7S-1XcMFvUWjAq-ZM5yyX3I",
  "access": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzExNDEwMDcxLCJpYXQiOjE3MTE0MDcwNzEsImp0aSI6ImRlYTA1ZjI1ZjAyNjRkYzg4N2Y3YzY2N2ZjMjFlYzEwIiwidXNlcl9pZCI6Mn0.ArneNCBc-XIMrhum34ifgp4oz8ZvEjn03yuhx6fXVow",
  "access_token_expiry": "2024-03-25 23:41:11",
  "refresh_token_expiry": "2024-03-26 22:51:11"
}
```

else 

`response` 404 BAD REQUEST 

## POST [http://127.0.0.1:8000/api/v1/users/token/refresh/] 

### refresh the token if access token expired

payloads

```
{
  "refresh": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTcxMTQ5MzcyNiwiaWF0IjoxNzExNDA3MzI2LCJqdGkiOiJhZmNhMzY3NDAwNzg0NjQzYmI3NTM5MTk3NTlhYzRjZSIsInVzZXJfaWQiOjJ9.AZ2W_b5Z0kAngqHnBSpxlbSc8-FiXo9KJjrqT3qpstc"
}
```

`response` 200 OK ✅

else

`response` 401 UNAUTHORIZED

```
{
  "detail": "Token is blacklisted",
  "code": "token_not_valid"
}
```

# N.B one refresh token can use once next time it will be blacklisted

## GET [http://127.0.0.1:8000/api/v1/users/me/] 

### get the currently logged in user information

`response` 200 OK ✅

```
{
  "id": 2,
  "password": "pbkdf2_sha256$720000$ZE6HGx0H8dA1ibOyRCRSz7$tuG7pb/nsBpLfPYZmqag4yiWAEaLADELdmIND7eXkWg=",
  "last_login": "2024-03-25T22:59:56.154082Z",
  "is_superuser": false,
  "username": "abc",
  "first_name": "",
  "last_name": "",
  "email": "abc@gmail.com",
  "is_staff": false,
  "is_active": true,
  "date_joined": "2024-03-25T16:25:47.271218Z",
  "groups": [],
  "user_permissions": []
}
```

else

`response` 401 UNAUTHORIZED

```
{
  "detail": "Given token not valid for any token type",
  "code": "token_not_valid",
  "messages": [
    {
      "token_class": "AccessToken",
      "token_type": "access",
      "message": "Token is invalid or expired"
    }
  ]
}
```

## GET [http://127.0.0.1:8000/api/v1/documents/]

### get all the documents which owner is request.user or have the permission to view this document it always gives the recent 10 records if available

`response` 200 OK ✅

```
{
  "count": 1,
  "next": null,
  "previous": null,
  "results": [
    {
      "id": 1,
      "shared_with": [
        {
          "id": 2,
          "can_edit": false,
          "can_view": true
        }
      ],
      "owner": {
        "id": 1,
        "username": "admin",
        "first_name": "",
        "last_name": ""
      },
      "title": "Title 1",
      "content": "Content 1",
      "created_at": "2024-03-25T23:17:02.082316Z",
      "updated_at": "2024-03-25T23:17:02.082458Z"
    }
  ]
}
```

`response` 401 UNAUTHORIZED

```
{
  "detail": "Given token not valid for any token type",
  "code": "token_not_valid",
  "messages": [
    {
      "token_class": "AccessToken",
      "token_type": "access",
      "message": "Token is invalid or expired"
    }
  ]
}

```

## POST [http://127.0.0.1:8000/api/v1/documents/]

### create a new document

payloads

```
{
  "title": "New Title",
  "content": "New Content"
}
```

`response` 200 OK ✅

```
{
  "id": 3,
  "shared_with": [],
  "owner": {
    "id": 2,
    "username": "abc",
    "first_name": "Abc",
    "last_name": "Def"
  },
  "title": "New Title",
  "content": "New Content",
  "created_at": "2024-03-25T23:31:36.322840Z",
  "updated_at": "2024-03-25T23:31:36.322917Z"
}
```

OR

Pass list of object contains user id and permission for this post

```
{
  "title": "New Title again",
  "content": "New Content again",
  "shared_with": [
    {
      "user_id": 1,
      "can_view": true,
      "can_edit": false
    }
  ]
}
```

`response` 200 OK ✅

```
{
  "id": 5,
  "shared_with": [
    {
        "id": 1, 
        "can_edit": false, 
        "can_view": true
    }
  ],
  "owner": {
      "id": 2, 
      "username": "abc", 
      "first_name": "Abc", 
      "last_name": "Def"
  },
  "title": "New Title again",
  "content": "New Content again",
  "created_at": "2024-03-25T23:36:13.763752Z",
  "updated_at": "2024-03-25T23:36:13.763813Z",
}

```

else

`response` 401 UNAUTHORIZED

```
{
  "detail": "Given token not valid for any token type",
  "code": "token_not_valid",
  "messages": [
    {
      "token_class": "AccessToken",
      "token_type": "access",
      "message": "Token is invalid or expired"
    }
  ]
}
```

## PUT [http://127.0.0.1:8000/api/v1/documents/4/]
## PATCH [http://127.0.0.1:8000/api/v1/documents/4/]

payloads

```
{
  "shared_with": [
    {
        "user_id": 1, 
        "can_edit": false, 
        "can_view": true
    }
  ],
  "title": "New Title again",
  "content": "New Content again"
}
```

`response` 200 OK ✅

```
{
  "id": 4,
  "shared_with": [
    {
      "id": 1,
      "can_edit": false,
      "can_view": false
    }
  ],
  "owner": {
    "id": 2,
    "username": "abc",
    "first_name": "Abc",
    "last_name": "Def"
  },
  "title": "New Title again",
  "content": "New Content again",
  "created_at": "2024-03-25T23:35:49.946308Z",
  "updated_at": "2024-03-25T23:43:43.868929Z"
}
```

else if user don't have the permission to edit or not the owner

`response` 403 FORBIDDEN

```
{
  "detail": "You don't have permission to update this document"
}
```

else

`response` 401 UNAUTHORIZED

```
{
  "detail": "Given token not valid for any token type",
  "code": "token_not_valid",
  "messages": [
    {
      "token_class": "AccessToken",
      "token_type": "access",
      "message": "Token is invalid or expired"
    }
  ]
}
```
