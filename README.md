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

1. GET /me: Returns the current authenticated user
2. GET /users/new - Registers a new user (admin only).
3. GET /users/`username` - Fetches information for a specific user.
4. POST /users/`username` - Updates information for a specific user.
5. POST /login - Logs in a user and returns a JWT token.
6. POST /logout - Logs out the user and invalidates the JWT token.
