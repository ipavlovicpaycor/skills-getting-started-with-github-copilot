"""
Tests for the GET /activities endpoint
Using AAA pattern: Arrange, Act, Assert
"""


def test_get_all_activities(client):
    """Test that GET /activities returns all activities"""
    # Arrange
    # (No setup needed; activities are pre-populated in app)

    # Act
    response = client.get("/activities")

    # Assert
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, dict)
    assert len(data) > 0


def test_get_activities_returns_correct_count(client):
    """Test that /activities returns expected number of activities"""
    # Arrange
    expected_count = 9

    # Act
    response = client.get("/activities")
    activities = response.json()

    # Assert
    assert len(activities) == expected_count


def test_get_activities_has_required_fields(client):
    """Test that each activity has required fields"""
    # Arrange
    required_fields = {"description", "schedule", "max_participants", "participants"}

    # Act
    response = client.get("/activities")
    activities = response.json()

    # Assert
    for activity_name, activity_data in activities.items():
        assert isinstance(activity_name, str)
        assert isinstance(activity_data, dict)
        assert required_fields.issubset(activity_data.keys())


def test_get_activities_participants_is_list(client):
    """Test that participants field is always a list"""
    # Arrange
    # (No setup needed)

    # Act
    response = client.get("/activities")
    activities = response.json()

    # Assert
    for activity_data in activities.values():
        assert isinstance(activity_data["participants"], list)
        for participant in activity_data["participants"]:
            assert isinstance(participant, str)


def test_get_activities_max_participants_is_positive(client):
    """Test that max_participants is a positive integer"""
    # Arrange
    # (No setup needed)

    # Act
    response = client.get("/activities")
    activities = response.json()

    # Assert
    for activity_data in activities.values():
        assert isinstance(activity_data["max_participants"], int)
        assert activity_data["max_participants"] > 0
