#!/usr/bin/env python3
"""
Test script for the User Management API
This script demonstrates all the API endpoints with example requests.
"""

import requests
import json
import time

# API base URL
BASE_URL = "http://localhost:8000"

def print_response(response, title):
    """Print formatted response"""
    print(f"\n{'='*50}")
    print(f"{title}")
    print(f"{'='*50}")
    print(f"Status Code: {response.status_code}")
    print(f"Headers: {dict(response.headers)}")
    try:
        print(f"Response: {json.dumps(response.json(), indent=2)}")
    except:
        print(f"Response: {response.text}")

def test_api():
    """Test all API endpoints"""
    
    print("🚀 Starting API Tests...")
    print(f"API Base URL: {BASE_URL}")
    
    # Test 1: Root endpoint
    print("\n1️⃣ Testing Root Endpoint")
    response = requests.get(f"{BASE_URL}/")
    print_response(response, "GET / - Root Endpoint")
    
    # Test 2: Create users
    print("\n2️⃣ Testing User Creation")
    
    users_data = [
        {
            "name": "John Doe",
            "email": "john@example.com",
            "age": 30,
            "bio": "Software Developer"
        },
        {
            "name": "Jane Smith",
            "email": "jane@example.com",
            "age": 25,
            "bio": "Data Scientist"
        },
        {
            "name": "Bob Johnson",
            "email": "bob@example.com",
            "age": 35,
            "bio": "Product Manager"
        }
    ]
    
    created_users = []
    for i, user_data in enumerate(users_data, 1):
        print(f"\nCreating user {i}: {user_data['name']}")
        response = requests.post(
            f"{BASE_URL}/users",
            json=user_data,
            headers={"x-api-key": "test-key-123"}
        )
        print_response(response, f"POST /users - Create User {i}")
        if response.status_code == 201:
            created_users.append(response.json())
    
    # Test 3: Get all users
    print("\n3️⃣ Testing Get All Users")
    response = requests.get(f"{BASE_URL}/users")
    print_response(response, "GET /users - Get All Users")
    
    # Test 4: Get users with query parameters
    print("\n4️⃣ Testing Get Users with Query Parameters")
    response = requests.get(
        f"{BASE_URL}/users",
        params={
            "skip": 0,
            "limit": 2,
            "min_age": 25,
            "max_age": 35
        },
        headers={"authorization": "Bearer test-token"}
    )
    print_response(response, "GET /users - With Query Parameters")
    
    # Test 5: Get user by ID
    if created_users:
        print("\n5️⃣ Testing Get User by ID")
        user_id = created_users[0]["id"]
        response = requests.get(
            f"{BASE_URL}/users/{user_id}",
            headers={"x-user-id": "test-user-123"}
        )
        print_response(response, f"GET /users/{user_id} - Get User by ID")
    
    # Test 6: Update user (PUT)
    if created_users:
        print("\n6️⃣ Testing Update User (PUT)")
        user_id = created_users[0]["id"]
        update_data = {
            "name": "John Updated",
            "email": "john.updated@example.com",
            "age": 31,
            "bio": "Senior Software Developer"
        }
        response = requests.put(
            f"{BASE_URL}/users/{user_id}",
            json=update_data,
            headers={"x-api-key": "test-key-123"}
        )
        print_response(response, f"PUT /users/{user_id} - Update User")
    
    # Test 7: Update user (PATCH)
    if created_users:
        print("\n7️⃣ Testing Update User (PATCH)")
        user_id = created_users[0]["id"]
        patch_data = {
            "age": 32,
            "bio": "Lead Developer"
        }
        response = requests.patch(
            f"{BASE_URL}/users/{user_id}",
            json=patch_data,
            headers={"x-api-key": "test-key-123"}
        )
        print_response(response, f"PATCH /users/{user_id} - Partial Update")
    
    # Test 8: Search users
    print("\n8️⃣ Testing Search Users")
    response = requests.get(
        f"{BASE_URL}/users/search/john",
        headers={"content-type": "application/json"}
    )
    print_response(response, "GET /users/search/john - Search Users")
    
    # Test 9: Test error handling
    print("\n9️⃣ Testing Error Handling")
    
    # Test invalid user ID
    response = requests.get(f"{BASE_URL}/users/999")
    print_response(response, "GET /users/999 - Non-existent User")
    
    # Test duplicate email
    if created_users:
        duplicate_user = {
            "name": "Duplicate User",
            "email": created_users[0]["email"],  # Use existing email
            "age": 40,
            "bio": "This should fail"
        }
        response = requests.post(f"{BASE_URL}/users", json=duplicate_user)
        print_response(response, "POST /users - Duplicate Email")
    
    # Test invalid data
    invalid_user = {
        "name": "",  # Empty name
        "email": "invalid-email",  # Invalid email
        "age": -5,  # Negative age
        "bio": "A" * 600  # Too long bio
    }
    response = requests.post(f"{BASE_URL}/users", json=invalid_user)
    print_response(response, "POST /users - Invalid Data")
    
    # Test 10: Delete user
    if created_users:
        print("\n🔟 Testing Delete User")
        user_id = created_users[-1]["id"]  # Delete the last created user
        response = requests.delete(
            f"{BASE_URL}/users/{user_id}",
            headers={"x-api-key": "test-key-123"}
        )
        print_response(response, f"DELETE /users/{user_id} - Delete User")
        
        # Verify user is deleted
        response = requests.get(f"{BASE_URL}/users/{user_id}")
        print_response(response, f"GET /users/{user_id} - Verify Deletion")
    
    print("\n✅ API Testing Complete!")
    print(f"\n📖 Swagger Documentation: {BASE_URL}/docs")
    print(f"📖 ReDoc Documentation: {BASE_URL}/redoc")

if __name__ == "__main__":
    try:
        test_api()
    except requests.exceptions.ConnectionError:
        print("❌ Error: Could not connect to the API server.")
        print("Make sure the server is running with: python app.py")
    except Exception as e:
        print(f"❌ Error: {e}") 