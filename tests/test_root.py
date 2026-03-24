"""
Tests for the root endpoint (GET /)
Using AAA pattern: Arrange, Act, Assert
"""


def test_root_redirects_to_index():
    """Test that GET / redirects to /static/index.html"""
    # Arrange
    # (No setup needed for simple redirect test)

    # Act
    from fastapi.testclient import TestClient
    from src.app import app
    client = TestClient(app)
    response = client.get("/", follow_redirects=False)

    # Assert
    assert response.status_code == 307  # Temporary redirect
    assert response.headers["location"] == "/static/index.html"
