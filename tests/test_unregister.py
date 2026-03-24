"""
Tests for the DELETE /activities/{activity_name}/signup endpoint
Using AAA pattern: Arrange, Act, Assert
"""


def test_unregister_success(client):
    """Test successful unregistration of a participant"""
    # Arrange
    activity_name = "Chess Club"
    email = "michael@mergington.edu"  # Already registered

    # Get initial participant count
    initial_activities = client.get("/activities").json()
    initial_count = len(initial_activities[activity_name]["participants"])
    assert email in initial_activities[activity_name]["participants"]

    # Act
    response = client.delete(
        f"/activities/{activity_name}/signup",
        params={"email": email}
    )

    # Assert
    assert response.status_code == 200
    data = response.json()
    assert "message" in data
    assert email in data["message"]
    assert activity_name in data["message"]

    # Verify participant was removed
    updated_activities = client.get("/activities").json()
    updated_count = len(updated_activities[activity_name]["participants"])
    assert updated_count == initial_count - 1
    assert email not in updated_activities[activity_name]["participants"]


def test_unregister_activity_not_found(client):
    """Test unregister from non-existent activity returns 404"""
    # Arrange
    activity_name = "Non Existent Activity"
    email = "student@mergington.edu"

    # Act
    response = client.delete(
        f"/activities/{activity_name}/signup",
        params={"email": email}
    )

    # Assert
    assert response.status_code == 404
    data = response.json()
    assert "detail" in data
    assert "not found" in data["detail"].lower()


def test_unregister_student_not_registered(client):
    """Test unregister for student not in activity returns 404"""
    # Arrange
    activity_name = "Gym Class"
    email = "nonexistent@mergington.edu"

    # Act
    response = client.delete(
        f"/activities/{activity_name}/signup",
        params={"email": email}
    )

    # Assert
    assert response.status_code == 404
    data = response.json()
    assert "detail" in data
    assert "not registered" in data["detail"].lower()


def test_unregister_response_format(client):
    """Test that unregister response has correct structure"""
    # Arrange
    activity_name = "Programming Class"
    email = "emma@mergington.edu"

    # Act
    response = client.delete(
        f"/activities/{activity_name}/signup",
        params={"email": email}
    )

    # Assert
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, dict)
    assert "message" in data
    assert isinstance(data["message"], str)


def test_unregister_then_reregister(client):
    """Test that student can re-register after unregistering"""
    # Arrange
    activity_name = "Art Studio"
    email = "lucas@mergington.edu"

    # Unregister
    response1 = client.delete(
        f"/activities/{activity_name}/signup",
        params={"email": email}
    )
    assert response1.status_code == 200

    # Act: Re-register
    response2 = client.post(
        f"/activities/{activity_name}/signup",
        params={"email": email}
    )

    # Assert
    assert response2.status_code == 200
    activities = client.get("/activities").json()
    assert email in activities[activity_name]["participants"]


def test_unregister_multiple_participants(client):
    """Test unregistering one participant doesn't affect others"""
    # Arrange
    activity_name = "Debate Team"
    # Get current participants
    activities = client.get("/activities").json()
    initial_participants = activities[activity_name]["participants"].copy()

    if len(initial_participants) > 0:
        email_to_remove = initial_participants[0]
        other_participants = initial_participants[1:]

        # Act
        response = client.delete(
            f"/activities/{activity_name}/signup",
            params={"email": email_to_remove}
        )

        # Assert
        assert response.status_code == 200
        updated_activities = client.get("/activities").json()
        updated_participants = updated_activities[activity_name]["participants"]

        # Verify removed participant is gone
        assert email_to_remove not in updated_participants

        # Verify other participants are still there
        for participant in other_participants:
            assert participant in updated_participants
