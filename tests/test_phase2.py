import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.phase2_filtering.filter_engine import FilterEngine
from src.phase2_filtering.models import UserPreferences

def test_engine():
    engine = FilterEngine()
    
    prefs = UserPreferences(
        location="Banashankari",
        cuisine="cafe",
        min_rating=4.5,
        max_budget=500.0
    )
    
    res = engine.filter_restaurants(prefs)
    print(f"Reason Code: {res.reason_code}")
    print(f"Found {len(res.restaurants)} restaurants.")
    for r in res.restaurants[:2]:
        print(f" - {r['name']}: {r['rating']} rating, {r['cost_for_two']} cost")

if __name__ == "__main__":
    test_engine()
