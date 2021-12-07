from fastapi.testclient import TestClient

# Test the user registration endpoint - POST /api/v1/auth/register
def test_register(client: TestClient):
    data = {
        "email": "buhari@gmail.com",
        "password": "Password1!",
        "username": "buhari",
        "phone_number": "07085130123",
        "bio": "President of this woebegone Nation",
    }
    response = client.post("/api/v1/auth/register", json=data)
    assert response.status_code == 200, response.text
    response_data = response.json()
    user_data = response_data["data"]
    assert user_data["email"] == "buhari@gmail.com"
    assert "id" in user_data


# Test the user login endpoint - POST /api/v1/auth/login
def test_login(client: TestClient):
    data = {"email": "buhari@gmail.com", "password": "Password1!"}
    response = client.post("/api/v1/auth/login", json=data)
    assert response.status_code == 200, response.text
    response_data = response.json()
    user_data = response_data["data"]
    assert user_data["email"] == "buhari@gmail.com"
    assert "id" in user_data
    assert "access_token" in response_data
    assert len(response_data["access_token"])
