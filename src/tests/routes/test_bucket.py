from fastapi.testclient import TestClient

# Test the Bucket creation endpoint without auth - POST /api/v1/bucket
def test_create_bucket_auth_required(client: TestClient):
    response = client.post("/api/v1/bucket")
    assert response.status_code == 403  # Forbidden
    response_data = response.json()
    assert "detail" in response_data


# Test the Bucket update endpoint without auth - PUT /api/v1/bucket/{bucket_id}
def test_update_bucket_auth_required(client: TestClient):
    response = client.put("/api/v1/bucket/1")
    assert response.status_code == 403  # Forbidden
    response_data = response.json()
    assert "detail" in response_data


# Test the Bucket delete endpoint without auth - DELETE /api/v1/bucket/{bucket_id}
def test_delete_bucket_auth_required(client: TestClient):
    response = client.delete("/api/v1/bucket/1")
    assert response.status_code == 403  # Forbidden
    response_data = response.json()
    assert "detail" in response_data


# Test the Bucket creation endpoint with auth - POST /api/v1/bucket/{bucket_id}
def test_create_bucket(client: TestClient, create_test_user_auth_header):
    data = {
        "goal": "Travel to Saturn",
        "category": "Travel",
        "active": True,
        "visibility": "private",
        "due_date": "2021-12-06T14:48:53.203Z",
    }
    response = client.post(
        "/api/v1/bucket", json=data, headers=create_test_user_auth_header
    )
    assert response.status_code == 200, response.text
    response_data = response.json()
    assert "data" in response_data
    bucket_data = response_data["data"]
    assert "id" in bucket_data
    assert "created_at" in bucket_data
    assert bucket_data["category"] == data["category"]


# Test the Bucket creation endpoint in bulk - POST /api/v/1/buckets
def test_create_multiple_buckets(client: TestClient, create_test_user_auth_header):
    data = [
        {
            "goal": "Test Bucket 1",
            "category": "Test Category",
            "active": True,
            "visibility": "private",
            "due_date": "2021-12-06T14:48:53.203Z",
        },
        {
            "goal": "Test Bucket 2",
            "category": "Test Category",
            "active": True,
            "visibility": "public",
            "due_date": "2021-12-06T14:48:53.203Z",
        },
    ]
    response = client.post(
        "/api/v1/buckets", json=data, headers=create_test_user_auth_header
    )
    assert response.status_code == 200, response.text
    response_data = response.json()
    assert "data" in response_data
    buckets_data = response_data["data"]
    assert isinstance(buckets_data, list)
    assert len(buckets_data) == 2


# Test the Bucket update endpoint with auth - PUT /api/v1/bucket/{bucket_id}
def test_update_bucket(client: TestClient, create_test_user_auth_header):
    data = {
        "goal": "Updated Test Bucket 1",
        "category": "Updated Category",
        "due_date": "2025-12-15T14:48:53.203Z",
        "visibility": "public",
    }
    response = client.put(
        "/api/v1/bucket/1", json=data, headers=create_test_user_auth_header
    )
    assert response.status_code == 200, response.text
    response_data = response.json()
    assert "data" in response_data
    assert "updated_at" in response_data["data"]
    bucket_data = response_data["data"]
    assert bucket_data["visibility"] == "public"
    assert bucket_data["goal"] == "Updated Test Bucket 1"


# Test the Bucket delete endpoint with auth - DELETE /api/v1/bucket/{bucket_id}
def test_delete_bucket(client: TestClient, create_test_user_auth_header):
    response = client.delete("/api/v1/bucket/1", headers=create_test_user_auth_header)
    assert response.status_code == 200, response.text
    response_data = response.json()
    assert "data" in response_data
