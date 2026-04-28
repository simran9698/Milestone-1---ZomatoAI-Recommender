import sys
import os
from fastapi.testclient import TestClient

# Add src to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.phase4_api.main import app

client = TestClient(app)

def test_recommend_success():
    print("\nTesting successful recommendation...")
    payload = {
        "location": "banashankari",
        "cuisine": "chinese",
        "min_rating": 4.0,
        "max_budget": 1000
    }
    response = client.post("/recommend", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert "results" in data
    assert len(data["results"]) > 0
    assert data["reason_code"] == "SUCCESS"
    print(f"Successfully retrieved {len(data['results'])} recommendations.")
    print(f"Sample recommendation: {data['results'][0]['name']} - {data['results'][0]['explanation'][:100]}...")

def test_recommend_no_match():
    print("\nTesting no match scenario (Non-existent location)...")
    payload = {
        "location": "mars",
        "cuisine": "alien_food",
        "min_rating": 5.0,
        "max_budget": 10
    }
    response = client.post("/recommend", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["results"] == []
    assert data["reason_code"] != "SUCCESS"
    print(f"Correctly returned no results with reason code: {data['reason_code']}")

def test_recommend_relaxation():
    print("\nTesting filter relaxation (Strict rating with high budget)...")
    # Using a known location but very high rating to trigger relaxation if possible
    payload = {
        "location": "banashankari",
        "cuisine": "chinese",
        "min_rating": 4.8, 
        "max_budget": 2000
    }
    response = client.post("/recommend", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert "results" in data
    print(f"Results with relaxation: {len(data['results'])}")
    if len(data['results']) > 0:
        print(f"Relaxation worked or matches found: {data['results'][0]['name']}")

if __name__ == "__main__":
    # If run directly as a script
    try:
        test_recommend_success()
        test_recommend_no_match()
        test_recommend_relaxation()
        print("\nAll tests passed!")
    except AssertionError as e:
        print(f"\nTest failed: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"\nAn error occurred: {e}")
        sys.exit(1)
