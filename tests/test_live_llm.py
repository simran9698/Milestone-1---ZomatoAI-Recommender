import os
import sys
import json
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.phase2_filtering.models import UserPreferences
from src.phase2_filtering.filter_engine import FilterEngine
from src.phase3_llm.prompt_builder import build_prompt
from src.phase3_llm.groq_client import GroqLLMClient

def run_test_case(name: str, prefs_dict: dict, filter_engine: FilterEngine, llm_client: GroqLLMClient):
    print(f"\n{'='*50}")
    print(f"TEST CASE: {name}")
    print(f"Preferences: {prefs_dict}")
    print(f"{'='*50}")

    prefs = UserPreferences(**prefs_dict)
    
    # Run Phase 2
    res = filter_engine.filter_restaurants(prefs)
    print(f"Phase 2 Output Code: {res.reason_code}")
    print(f"Shortlist Size: {len(res.restaurants)}")
    
    if len(res.restaurants) == 0:
        print("No restaurants found to send to LLM.")
        return

    # Run Phase 3
    # Only take top 2 for this quick test to keep LLM response fast
    test_shortlist = res.restaurants[:2] 
    
    prompt = build_prompt(prefs_dict, test_shortlist)
    print("Calling Groq LLM...")
    
    llm_response = llm_client.generate_recommendations(prompt)
    
    # Merge
    merged_results = llm_client.merge_with_catalog(llm_response, test_shortlist)
    
    print("\n--- FINAL RECOMMENDATIONS ---")
    for r in merged_results:
        print(f"\nName: {r['name']}")
        print(f"Rating: {r['rating']} | Cost for Two: {r['cost_for_two']}")
        print(f"Cuisines: {', '.join(r['cuisines'])}")
        print(f"LLM Explanation: {r.get('explanation')}")

def main():
    print("Initializing components...")
    filter_engine = FilterEngine()
    llm_client = GroqLLMClient()

    test_cases = [
        (
            "Highly Rated Chinese in Banashankari",
            {
                "location": "banashankari",
                "cuisine": "chinese",
                "min_rating": 4.0,
                "max_budget": 1000.0
            }
        ),
        (
            "Cafe in Banashankari",
            {
                "location": "banashankari",
                "cuisine": "cafe",
                "min_rating": 3.5,
                "max_budget": 800.0
            }
        ),
        (
            "North Indian in Basavanagudi",
            {
                "location": "basavanagudi",
                "cuisine": "north indian",
                "min_rating": 3.5,
                "max_budget": 1000.0
            }
        )
    ]

    for name, prefs in test_cases:
        run_test_case(name, prefs, filter_engine, llm_client)

if __name__ == "__main__":
    main()
