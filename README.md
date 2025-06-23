# User Management API

A comprehensive REST API built with FastAPI for managing users with full CRUD operations, Swagger documentation, and SQLite database storage.

## Features

- ✅ **All HTTP Methods**: GET, POST, PUT, PATCH, DELETE
- ✅ **Swagger Documentation**: Interactive API docs at `/docs`
- ✅ **SQLite Database**: Lightweight, file-based storage
- ✅ **Request Body Validation**: Using Pydantic models
- ✅ **Query Parameters**: Filtering and pagination
- ✅ **Path Parameters**: URL-based resource identification
- ✅ **Headers**: Authentication and tracking headers
- ✅ **CORS Support**: Cross-origin resource sharing enabled
- ✅ **Error Handling**: Proper HTTP status codes and error messages

## Quick Start

### 0. Python Install

You need to have Python 3 installed on your computer with PIP working.

### 1. Create and activate Virtualenv and Install Dependencies

On Linux or Mac

```bash
python -m virtualenv -p 3 venv
source ./venv/bin/activate
pip install -r requirements.txt
```

On Windows (not recommended)

```bash
python -m virtualenv -p 3 venv
./venv/Scripts/activate.ps
pip install -r requirements.txt
```

### 2. Run the Application

```bash
python app.py
```

Or using uvicorn directly:

```bash
uvicorn app:app --reload --host 0.0.0.0 --port 8000
```

### 3. Access the API

- **API Base URL**: http://localhost:8000
- **Swagger Documentation**: http://localhost:8000/docs
- **ReDoc Documentation**: http://localhost:8000/redoc

## API Endpoints

### Root

- `GET /` - Welcome message and API info

### Users

#### Create User

- `POST /users` - Create a new user
  - **Body**: User data (name, email, age, bio)
  - **Headers**: `x-api-key` (optional)

#### Get Users

- `GET /users` - Get all users with filtering and pagination
  - **Query Params**:
    - `skip` (int): Number of users to skip
    - `limit` (int): Maximum users to return
    - `name` (str): Filter by name (partial match)
    - `min_age` (int): Minimum age filter
    - `max_age` (int): Maximum age filter
  - **Headers**: `authorization` (optional)

#### Get User by ID

- `GET /users/{user_id}` - Get specific user by ID
  - **Path Params**: `user_id` (int)
  - **Headers**: `x-user-id` (optional)

#### Update User (Complete)

- `PUT /users/{user_id}` - Update all user fields
  - **Path Params**: `user_id` (int)
  - **Body**: Complete user data
  - **Headers**: `x-api-key` (optional)

#### Update User (Partial)

- `PATCH /users/{user_id}` - Update only provided fields
  - **Path Params**: `user_id` (int)
  - **Body**: Partial user data
  - **Headers**: `x-api-key` (optional)

#### Delete User

- `DELETE /users/{user_id}` - Delete user by ID
  - **Path Params**: `user_id` (int)
  - **Headers**: `x-api-key` (optional)

#### Search Users

- `GET /users/search/{search_term}` - Search users by name or email
  - **Path Params**: `search_term` (str)
  - **Headers**: `content-type` (optional)

## Data Models

### User Model

```json
{
  "id": 1,
  "name": "John Doe",
  "email": "john@example.com",
  "age": 30,
  "bio": "Software developer",
  "created_at": "2024-01-01T00:00:00",
  "updated_at": "2024-01-01T00:00:00"
}
```

### Create User Request

```json
{
  "name": "John Doe",
  "email": "john@example.com",
  "age": 30,
  "bio": "Software developer"
}
```

### Update User Request (PATCH)

```json
{
  "name": "John Smith",
  "age": 31
}
```

## Example Usage

### Create a User

```bash
curl -X POST "http://localhost:8000/users" \
  -H "Content-Type: application/json" \
  -H "x-api-key: your-api-key" \
  -d '{
    "name": "John Doe",
    "email": "john@example.com",
    "age": 30,
    "bio": "Software developer"
  }'
```

### Get All Users

```bash
curl -X GET "http://localhost:8000/users?skip=0&limit=10&min_age=25"
```

### Get User by ID

```bash
curl -X GET "http://localhost:8000/users/1"
```

### Update User (PUT)

```bash
curl -X PUT "http://localhost:8000/users/1" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "John Smith",
    "email": "john.smith@example.com",
    "age": 31,
    "bio": "Senior Software Developer"
  }'
```

### Update User (PATCH)

```bash
curl -X PATCH "http://localhost:8000/users/1" \
  -H "Content-Type: application/json" \
  -d '{
    "age": 32,
    "bio": "Lead Developer"
  }'
```

### Delete User

```bash
curl -X DELETE "http://localhost:8000/users/1"
```

### Search Users

```bash
curl -X GET "http://localhost:8000/users/search/john"
```

## Database

The application uses SQLite as the database, which creates a `users.db` file in the project directory. This file contains:

- **users table**: Stores all user data with automatic timestamps
- **Indexes**: On id, name, and email for fast queries
- **Constraints**: Unique email addresses

## Error Handling

The API returns appropriate HTTP status codes:

- `200` - Success
- `201` - Created
- `204` - No Content (DELETE)
- `400` - Bad Request (validation errors)
- `404` - Not Found
- `422` - Validation Error (Pydantic)

## Development

### Project Structure

```
json-server-http-training/
├── app.py              # Main FastAPI application
├── requirements.txt    # Python dependencies
├── README.md          # This file
└── users.db           # SQLite database (created automatically)
```

### Adding New Features

1. **New Endpoints**: Add new route functions in `app.py`
2. **New Models**: Create new Pydantic models and database models
3. **Validation**: Use Pydantic Field validators
4. **Documentation**: Add docstrings for automatic Swagger generation

## Testing

You can test the API using:

1. **Swagger UI**: Visit http://localhost:8000/docs
2. **curl**: Use the examples above
3. **Postman**: Import the endpoints
4. **Python requests**: Use the requests library

## Production Deployment

For production deployment, consider:

1. **Environment Variables**: Use environment variables for configuration
2. **Database**: Consider PostgreSQL for production
3. **Authentication**: Implement proper authentication
4. **Rate Limiting**: Add rate limiting middleware
5. **Logging**: Add proper logging
6. **HTTPS**: Use HTTPS in production
