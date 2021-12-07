from fastapi.testclient import TestClient

# Test the Get user endpoint without auth - GET /api/v1/user
def test_get_user_auth_required(client: TestClient):
    response = client.get("/api/v1/user")
    assert response.status_code == 403  # Forbidden
    response_data = response.json()
    assert "detail" in response_data


# Test the Get user endpoint with auth - GET /api/v1/user
def test_get_user(client: TestClient, create_test_user_auth_header):
    response = client.get("/api/v1/user", headers=create_test_user_auth_header)
    assert response.status_code == 200, response.text
    response_data = response.json()
    assert "data" in response_data
    user_data = response_data["data"]["user"]
    assert "buckets" in response_data["data"]
    buckets_data = response_data["data"]["buckets"]
    assert "id" in user_data
    assert "email" in user_data
    assert "created_at" in user_data
    assert isinstance(buckets_data, list)


# Test the Get user endpoint with invalid token - GET /api/v1/user
def test_get_user_invalid_token(client: TestClient):
    invalid_auth_header = {"Authorization": "Bearer wrong.header"}
    response = client.get("/api/v1/user", headers=invalid_auth_header)
    assert response.status_code == 401, response.text
    response_data = response.json()
    assert "detail" in response_data


# Test the Update user endpoint without auth - PUT /api/v1/user
def test_update_user_auth_required(client: TestClient):
    response = client.put("/api/v1/user")
    assert response.status_code == 403
    response_data = response.json()
    assert "detail" in response_data


# Test the Update user endpoint with auth - PUT /api/v1/user
def test_update_user(client: TestClient, create_test_user_auth_header):
    data = {"location": "Updated Location Test", "bio": "Updated Bio Test"}
    response = client.put(
        "/api/v1/user", json=data, headers=create_test_user_auth_header
    )
    assert response.status_code == 200, response.text
    response_data = response.json()["data"]
    assert "id" in response_data
    assert "updated_at" in response_data
    assert response_data["bio"] == data["bio"]
    assert response_data["location"] == data["location"]


# Test the Delete user endpoint without auth - DELETE /api/v1/user
def test_delete_user_auth_required(client: TestClient):
    response = client.delete("/api/v1/user")
    assert response.status_code == 403
    response_data = response.json()
    assert "detail" in response_data


# Test the Get user buckets endpoint - GET /api/v1/user/buckets
def test_get_user_buckets(client: TestClient, create_test_user_auth_header):
    response = client.get("/api/v1/user/buckets", headers=create_test_user_auth_header)
    # Buckets might be empty
    assert response.status_code == 200 or response.status_code == 404, response.text
    if response.status_code == 200:
        response_data = response.json()["data"]
        assert "buckets" in response_data
        assert isinstance(response_data["buckets"], list)


# Test the Get user by ID endpoint - GET /api/v1/user/{user_id}
def test_get_user_by_id(client: TestClient):
    response = client.get("/api/v1/user/1")
    assert response.status_code == 200, response.text
    response_data = response.json()
    user_data = response_data["data"]["user"]
    assert "buckets" in response_data["data"]
    buckets_data = response_data["data"]["buckets"]
    assert "id" in user_data
    assert "created_at" in user_data
    assert isinstance(buckets_data, list)


# Test the Get user bucket by ID endpoint - GET /api/v1/user/bucket/{bucket_id}
def test_user_bucket_by_id(client: TestClient, create_test_user_auth_header):
    response = client.get("/api/v1/user/bucket/1", headers=create_test_user_auth_header)
    assert response.status_code == 200 or response.status_code == 404, response.text
    if response.status_code == 200:
        response_data = response.json()["data"]
        assert "id" in response_data
        assert "goal" in response_data
        assert "created_at" in response_data
