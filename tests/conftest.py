import pytest
from fastapi.testclient import TestClient
from src.app import app

# Original activities data for resetting between tests
ORIGINAL_ACTIVITIES = {
    "Chess Club": {
        "description": "Learn strategies and compete in chess tournaments",
        "schedule": "Fridays, 3:30 PM - 5:00 PM",
        "max_participants": 12,
        "participants": ["michael@mergington.edu", "daniel@mergington.edu"]
    },
    "Programming Class": {
        "description": "Learn programming fundamentals and build software projects",
        "schedule": "Tuesdays and Thursdays, 3:30 PM - 4:30 PM",
        "max_participants": 20,
        "participants": ["emma@mergington.edu", "sophia@mergington.edu"]
    },
    "Gym Class": {
        "description": "Physical education and sports activities",
        "schedule": "Mondays, Wednesdays, Fridays, 2:00 PM - 3:00 PM",
        "max_participants": 30,
        "participants": ["john@mergington.edu", "olivia@mergington.edu"]
    },
    "Basketball Team": {
        "description": "Play competitive basketball and develop teamwork skills",
        "schedule": "Tuesdays and Thursdays, 4:00 PM - 6:00 PM",
        "max_participants": 15,
        "participants": ["matt@mergington.edu", "sarah@mergington.edu"]
    },
    "Swimming Club": {
        "description": "Improve swimming technique and participate in meets",
        "schedule": "Mondays and Wednesdays, 3:30 PM - 5:00 PM",
        "max_participants": 18,
        "participants": ["nina@mergington.edu", "oliver@mergington.edu"]
    },
    "Drama Club": {
        "description": "Practice acting, stagecraft, and prepare performances",
        "schedule": "Wednesdays, 4:00 PM - 5:30 PM",
        "max_participants": 20,
        "participants": ["anna@mergington.edu", "luke@mergington.edu"]
    },
    "Painting Workshop": {
        "description": "Explore painting techniques and create original artwork",
        "schedule": "Fridays, 4:00 PM - 6:00 PM",
        "max_participants": 14,
        "participants": ["zoe@mergington.edu", "ethan@mergington.edu"]
    },
    "Debate Team": {
        "description": "Develop argumentation skills and compete in debate tournaments",
        "schedule": "Mondays and Thursdays, 5:00 PM - 6:30 PM",
        "max_participants": 16,
        "participants": ["maria@mergington.edu", "alex@mergington.edu"]
    },
    "Science Club": {
        "description": "Conduct experiments and explore scientific concepts",
        "schedule": "Tuesdays, 4:00 PM - 5:30 PM",
        "max_participants": 18,
        "participants": ["kevin@mergington.edu", "mia@mergington.edu"]
    }
}


@pytest.fixture
def client():
    """Test client for FastAPI app"""
    return TestClient(app)


@pytest.fixture(autouse=True)
def reset_activities():
    """Reset activities data before each test"""
    import src.app
    # Deep copy the original activities
    import copy
    src.app.activities = copy.deepcopy(ORIGINAL_ACTIVITIES)