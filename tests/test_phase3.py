import os
import sys
import json
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.phase2_filtering.models import UserPreferences
from src.phase3_llm.prompt_builder import build_prompt
from src.phase3_llm.groq_client import GroqLLMClient

def test_phase3():
    # Mock some data that Phase 2 would return
    shortlist = [
        {"name": "Spice Garden", "cuisines": ["indian", "chinese"], "rating": 4.5, "cost_for_two": 600},
        {"name": "Cafe Delight", "cuisines": ["cafe", "bakery"], "rating": 4.2, "cost_for_two": 400}
    ]
    
    prefs_dict = {
        "location": "Banashankari",
        "cuisine": "indian",
        "min_rating": 4.0,
        "max_budget": 800.0
    }
    
    prompt = build_prompt(prefs_dict, shortlist)
    print("--- GENERATED PROMPT ---")
    print(prompt)
    print("------------------------\n")
    
    # We won't actually call the LLM to save API credits, but we will test the merging logic
    # with a mock LLM output
    mock_llm_response = {
        "recommendations": [
            {"name": "Spice Garden", "explanation": "A highly rated choice serving exactly the Indian cuisine you requested well within your budget."},
            {"name": "Cafe Delight", "explanation": "While primarily a cafe, it offers a great atmosphere within your budget."}
        ]
    }
    
    client = GroqLLMClient()
    merged = client.merge_with_catalog(mock_llm_response, shortlist)
    
    print("--- MERGED RESULT ---")
    print(json.dumps(merged, indent=2))
    print("---------------------")

if __name__ == "__main__":
    test_phase3()
