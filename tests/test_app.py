import pytest
from fastapi.testclient import TestClient
from src.app import app

client = TestClient(app)

# --- Test: GET /activities ---
def test_get_activities():
    # Arrange
    # (client is already arranged)
    # Act
    response = client.get("/activities")
    # Assert
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, dict)
    assert "Chess Club" in data
    assert "participants" in data["Chess Club"]

# --- Test: POST /activities/{activity_name}/signup ---
def test_signup_success():
    # Arrange
    activity = "Chess Club"
    email = "newstudent@mergington.edu"
    # Act
    response = client.post(f"/activities/{activity}/signup?email={email}")
    # Assert
    assert response.status_code == 200
    assert response.json()["message"] == f"Signed up {email} for {activity}"
    # Confirm participant added
    participants = client.get("/activities").json()[activity]["participants"]
    assert email in participants


def test_signup_duplicate():
    # Arrange
    activity = "Chess Club"
    email = "newstudent@mergington.edu"
    # Act
    response = client.post(f"/activities/{activity}/signup?email={email}")
    # Assert
    assert response.status_code == 400
    assert "already signed up" in response.json()["detail"]

# --- Test: POST /activities/{activity_name}/unregister ---
def test_unregister_success():
    # Arrange
    activity = "Chess Club"
    email = "newstudent@mergington.edu"
    # Act
    response = client.post(f"/activities/{activity}/unregister?email={email}")
    # Assert
    assert response.status_code == 200
    assert response.json()["message"] == f"Removed {email} from {activity}"
    # Confirm participant removed
    participants = client.get("/activities").json()[activity]["participants"]
    assert email not in participants


def test_unregister_not_registered():
    # Arrange
    activity = "Chess Club"
    email = "notregistered@mergington.edu"
    # Act
    response = client.post(f"/activities/{activity}/unregister?email={email}")
    # Assert
    assert response.status_code == 400
    assert "not registered" in response.json()["detail"]
