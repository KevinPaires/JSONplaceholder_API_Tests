import requests


def test_get_users(base_url: str):
    response = requests.get(f"{base_url}/users/1")
    assert response.status_code == 200
    data = response.json()
    print(data)
    assert data["id"] == 1
    assert "name" in data


def test_get_users_post(base_url: str):
    response = requests.get(f"{base_url}/posts/1")
    assert response.status_code == 200 or response.status_code == 201
    data = response.json()
    print(data)
    assert data["userId"] == 1
    assert "title" in data


def test_create_user(base_url: str):
    payload = {"name": "John Doe", "username": "johnd", "email": "johnd@example.com"}
    response = requests.post(f"{base_url}/users", json=payload)
    assert response.status_code == 201 or response.status_code == 200
    data = response.json()
    print(data)
    assert data["name"] == payload["name"]


def test_update_user(base_url: str):
    payload = {"name": "Updated Name"}
    response = requests.put(f"{base_url}/users/1", json=payload)
    assert response.status_code == 200
    data = response.json()
    print(data)
    assert data["name"] == "Updated Name"


def test_delete_user(base_url: str):
    response = requests.delete(f"{base_url}/users/1")
    print(response)
    assert response.status_code == 200 or response.status_code == 204

def test_get_nonexistent_user(base_url: str):
    """Test that API returns 404 for non-existent user"""
    response = requests.get(f"{base_url}/users/99999")
    assert response.status_code == 404

def test_get_user_with_string_id(base_url: str):
    """Test that API handles invalid ID type"""
    response = requests.get(f"{base_url}/users/abc")
    assert response.status_code in [400, 404]

def test_create_user_missing_fields(base_url: str):
    """Test creating user without required fields"""
    payload = {"username": "johnd"}  # Missing name and email
    response = requests.post(f"{base_url}/users", json=payload)
    assert response.status_code == 201
