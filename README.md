


# Travel API with Microservices

This project implements a basic Travel API with multiple microservices using Flask. The API is designed to manage travel destinations, handle user accounts and authentication, and enforce role-based access for secure access to endpoints. It follows the OpenAPI/Swagger standards for documentation.

## Project Overview

The Travel API consists of three main microservices:

1. **Destination Service**: Manages travel destinations, including adding, deleting, and viewing destination details.
2. **User Service**: Handles user registration, authentication, and profile management.
3. **Authentication Service**: Manages user authentication tokens and enforces role-based access.

### Microservices Details

#### 1. Destination Service

- **Endpoints**:
  - `GET /destination`: Retrieve a list of all travel destinations.
  - `POST /destination`: Add  a new destination(Admin-only).
  - `DELETE /destination/<id>`: Delete a specific travel destination (Admin-only).
  
- **Destination Details**:
- `id`: Destination id (string)
  - `Name`: Destination name (string)
  - `Description`: Short description (string)
  - `Location`: Location name (string)

#### 2. User Service

- **Endpoints**:
  - `POST /register`: Register a new user.
  - `POST /login`: Authenticate a user and provide an access token.
  - `GET /profile`: View profile information (user-specific).
  
- **User Details**:
  - `id`: user id (string)
  - `Name`: Full name (string)
  - `Email`: Email address (string)
  - `Password`: Hashed password (string)
  - `Role`: User role, either "Admin" or "User" (string)

#### 3. Authentication Service

- **Endpoints**:
- `POST /auth/validate`: Validate a new user whether a user or admin.
  - **Role-based Access**: Ensure Admins have access to specific actions (e.g., destination management).

## Features & Requirements

### User Authentication Expansion:
- **Role-based Access Control**: Only admins should be allowed to access certain endpoints such as adding or removing destinations and viewing all bookings.

### Error Handling and Validation:
- **Input Validation**: Validate inputs for all endpoints, ensuring that required fields for user registration and login are checked.

### OpenAPI Documentation:
- **API Documentation**: The API follows OpenAPI standards, and Swagger UI is set up to make the documentation accessible.

## Setup and Run Instructions

### Prerequisites
- Python 3.7 or higher
- Flask 2.x
- Flask-RESTX
- OpenAPI/Swagger tools

### Installation

#### Clone the project repository

```
git clone https://github.com/uzzalcse/travel-api.git

```

#### Go to the project directory 

```
cd travel-api

```

#### Creating virtual environment 

```
python -m venv venv

```

#### Go to the virtual environment
##### In Windows
```
venv\Scripts\activate

```

###### In Mac/Linus

```
source/bin/activate

```


#### Now install  dependencies in virtual environment

```
pip install -r requirements.txt

```
#### To run each service go to that service directory

##### To run auth service go to the auth_service directory using the following command from project root directory

``` 
cd auth_service
python app.py

```

###### Follow the link to see the results


http://127.0.0.1:5001/

###### To run tests for auth service run the follwing commands (You have to run this command from auth_service directory)

```
pytest --cov=controllers --cov=app --cov-report=term-missing

```



##### To run destination service go to the destination_service directory using the following command from project root directory

```
cd destination_service
python app.py

```

###### Follow the link to see the results
http://127.0.0.1:5002/


###### To run tests for destination service run the follwing commands (You have to run this command from destination_service directory)

```
pytest --cov=controllers --cov=app --cov-report=term-missing

```


##### To run user service go to the user_service directory using the following command from project root directory

```
cd user_service

python app.py

```
###### Follow the link to see the results
http://127.0.0.1:5003/


###### To run tests for user service run the follwing commands (You have to run this command from user_service directory)

```
pytest --cov=controllers --cov=app --cov-report=term-missing

```





