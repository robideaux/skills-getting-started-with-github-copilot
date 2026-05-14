import pytest
from fastapi.testclient import TestClient


class TestActivitiesAPI:
    """Test suite for activities API endpoints"""

    def test_get_activities(self, client: TestClient):
        """Test GET /activities returns all activities"""
        response = client.get("/activities")
        assert response.status_code == 200
        data = response.json()

        # Should return a dict with 9 activities
        assert isinstance(data, dict)
        assert len(data) == 9

        # Check structure of one activity
        chess_club = data["Chess Club"]
        assert "description" in chess_club
        assert "schedule" in chess_club
        assert "max_participants" in chess_club
        assert "participants" in chess_club
        assert isinstance(chess_club["participants"], list)

    def test_signup_success(self, client: TestClient):
        """Test successful signup for an activity"""
        response = client.post("/activities/Chess%20Club/signup?email=newstudent@mergington.edu")
        assert response.status_code == 200
        data = response.json()
        assert "message" in data
        assert "Signed up newstudent@mergington.edu for Chess Club" in data["message"]

        # Verify the student was added
        response = client.get("/activities")
        activities = response.json()
        assert "newstudent@mergington.edu" in activities["Chess Club"]["participants"]

    def test_signup_activity_not_found(self, client: TestClient):
        """Test signup for non-existent activity"""
        response = client.post("/activities/NonExistent/signup?email=test@mergington.edu")
        assert response.status_code == 404
        data = response.json()
        assert "detail" in data
        assert data["detail"] == "Activity not found"

    def test_signup_already_signed_up(self, client: TestClient):
        """Test signup when student is already signed up"""
        # First signup
        client.post("/activities/Chess%20Club/signup?email=duplicate@mergington.edu")

        # Try to signup again
        response = client.post("/activities/Chess%20Club/signup?email=duplicate@mergington.edu")
        assert response.status_code == 400
        data = response.json()
        assert "detail" in data
        assert data["detail"] == "Student already signed up for this activity"

    def test_remove_success(self, client: TestClient):
        """Test successful removal from an activity"""
        # First add a student
        client.post("/activities/Programming%20Class/signup?email=removeme@mergington.edu")

        # Now remove
        response = client.delete("/activities/Programming%20Class/remove?email=removeme@mergington.edu")
        assert response.status_code == 200
        data = response.json()
        assert "message" in data
        assert "Removed removeme@mergington.edu from Programming Class" in data["message"]

        # Verify the student was removed
        response = client.get("/activities")
        activities = response.json()
        assert "removeme@mergington.edu" not in activities["Programming Class"]["participants"]

    def test_remove_activity_not_found(self, client: TestClient):
        """Test remove from non-existent activity"""
        response = client.delete("/activities/NonExistent/remove?email=test@mergington.edu")
        assert response.status_code == 404
        data = response.json()
        assert "detail" in data
        assert data["detail"] == "Activity not found"

    def test_remove_not_signed_up(self, client: TestClient):
        """Test remove when student is not signed up"""
        response = client.delete("/activities/Chess%20Club/remove?email=notsignedup@mergington.edu")
        assert response.status_code == 400
        data = response.json()
        assert "detail" in data
        assert data["detail"] == "Student not signed up for this activity"

    def test_root_redirect(self, client: TestClient):
        """Test root endpoint redirects to static index"""
        response = client.get("/", follow_redirects=False)
        assert response.status_code == 307  # Temporary redirect
        assert response.headers["location"] == "/static/index.html"