# Villiar

# Flask API With user Authentication

This project implements a Flask-based API with various endpoints, 
using the `login_required` decorator to enforce authentication. 
The API includes routes for fetching user information, registering new users, updating user information, 
logging in, and logging out.

## Components

### login_required Decorator
The `login_required` decorator is used to protect routes, ensuring that only authenticated users can access them. 
It checks for a valid JWT token in the request headers and, optionally, verifies user roles.

### Routes

1. GET /users/new
2. GET /users/`username`
3. POST /users/`username`
4. POST /login
5. POST /logout
