"""
Tests for the POST /activities/{activity_name}/signup endpoint
Using AAA pattern: Arrange, Act, Assert
"""


def test_signup_valid_activity_and_email(client):
    """Test successful signup with valid activity and new email"""
    # Arrange
    activity_name = "Chess Club"
    email = "newstudent@mergington.edu"

    # Get initial participant count
    initial_activities = client.get("/activities").json()
    initial_count = len(initial_activities[activity_name]["participants"])

    # Act
    response = client.post(
        f"/activities/{activity_name}/signup",
        params={"email": email}
    )

    # Assert
    assert response.status_code == 200
    data = response.json()
    assert "message" in data
    assert email in data["message"]
    assert activity_name in data["message"]

    # Verify participant was added
    updated_activities = client.get("/activities").json()
    updated_count = len(updated_activities[activity_name]["participants"])
    assert updated_count == initial_count + 1
    assert email in updated_activities[activity_name]["participants"]


def test_signup_activity_not_found(client):
    """Test signup to non-existent activity returns 404"""
    # Arrange
    activity_name = "Non Existent Activity"
    email = "student@mergington.edu"

    # Act
    response = client.post(
        f"/activities/{activity_name}/signup",
        params={"email": email}
    )

    # Assert
    assert response.status_code == 404
    data = response.json()
    assert "detail" in data
    assert "not found" in data["detail"].lower()


def test_signup_duplicate_registration(client):
    """Test signing up same email twice returns 400"""
    # Arrange
    activity_name = "Programming Class"
    email = "emma@mergington.edu"  # Already registered

    # Act
    response = client.post(
        f"/activities/{activity_name}/signup",
        params={"email": email}
    )

    # Assert
    assert response.status_code == 400
    data = response.json()
    assert "detail" in data
    assert "already" in data["detail"].lower()


def test_signup_with_special_characters_in_email(client):
    """Test signup with email containing special characters"""
    # Arrange
    activity_name = "Drama Club"
    email = "student+test@mergington.edu"

    # Act
    response = client.post(
        f"/activities/{activity_name}/signup",
        params={"email": email}
    )

    # Assert
    assert response.status_code == 200
    data = response.json()
    assert "message" in data

    # Verify participant was added with special chars preserved
    updated_activities = client.get("/activities").json()
    assert email in updated_activities[activity_name]["participants"]


def test_signup_case_sensitivity(client):
    """Test that different case variations are treated as different emails"""
    # Arrange
    activity_name = "Tennis Club"
    email_lowercase = "newperson@mergington.edu"
    email_uppercase = "NewPerson@mergington.edu"

    # Act
    response1 = client.post(
        f"/activities/{activity_name}/signup",
        params={"email": email_lowercase}
    )
    response2 = client.post(
        f"/activities/{activity_name}/signup",
        params={"email": email_uppercase}
    )

    # Assert
    assert response1.status_code == 200
    assert response2.status_code == 200  # Currently different case = different emails
    activities = client.get("/activities").json()
    assert email_lowercase in activities[activity_name]["participants"]
    assert email_uppercase in activities[activity_name]["participants"]


def test_signup_response_format(client):
    """Test that signup response has correct structure"""
    # Arrange
    activity_name = "Science Club"
    email = "scientist@mergington.edu"

    # Act
    response = client.post(
        f"/activities/{activity_name}/signup",
        params={"email": email}
    )

    # Assert
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, dict)
    assert "message" in data
    assert isinstance(data["message"], str)
