from sqlalchemy.orm import Session
from fastapi.testclient import TestClient
from db.repository.user import add_user, query_user_by_email
from db.models import User as UserModel

# Test User Credentials
TEST_USER_EMAIL = "test-user@gmail.com"
TEST_USER_PASSWORD = "Password1!"


def fetch_test_user_token(client: TestClient, email: str, password: str) -> dict:
    """
    Description: Fetch user bearer token from /login endpoint
    """
    data = {"email": email, "password": password}
    r = client.post("/api/v1/auth/login", json=data)
    response = r.json()
    print(response)
    access_token = response["access_token"]
    auth_header = {"Authorization": f"Bearer {access_token}"}
    return auth_header


def fetch_test_user_auth_header(client: TestClient, db: Session) -> dict:
    """
    Description: Generate test user authorization header
    """
    existing_test_user = query_user_by_email(db, TEST_USER_EMAIL)
    if not existing_test_user:
        test_user = UserModel(
            email=TEST_USER_EMAIL,
            username="test-user",
            bio="Test Bio",
            password=TEST_USER_PASSWORD,
        )
        test_user.set_password(TEST_USER_PASSWORD)
        db.add(test_user)
        db.commit()
        db.refresh(test_user)
        print(fetch_test_user_token(client, TEST_USER_EMAIL, TEST_USER_PASSWORD))
        return fetch_test_user_token(client, TEST_USER_EMAIL, TEST_USER_PASSWORD)
    return fetch_test_user_token(
        client, existing_test_user.email, existing_test_user.password
    )
