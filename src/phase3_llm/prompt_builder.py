import json

def build_prompt(user_prefs: dict, shortlist: list) -> str:
    shortlist_summary = []
    user_min_rating = round(float(user_prefs.get('min_rating', 0.0)), 1)
    user_max_budget = float(user_prefs.get('max_budget', 0.0)) if user_prefs.get('max_budget') else None
    
    for item in shortlist:
        cuisines = item.get("cuisines")
        if hasattr(cuisines, "tolist"):
            cuisines = cuisines.tolist()
            
        rest_rating = round(float(item.get("rating", 0.0)), 1)
        rest_cost = float(item.get("cost_for_two", 0.0))
        
        # Rating logic computed cleanly in Python
        if rest_rating < user_min_rating:
            rating_status = "Does not meet your rating preference"
        elif rest_rating == user_min_rating:
            rating_status = "Matches your rating preference"
        else:
            rating_status = "Exceeds your rating expectation"
            
        # Budget logic computed cleanly in Python
        if user_max_budget is not None:
            if rest_cost <= user_max_budget:
                budget_status = f"Within budget limit (₹{int(user_max_budget)})"
            else:
                budget_status = f"Exceeds budget limit (₹{int(user_max_budget)})"
        else:
            budget_status = f"₹{int(rest_cost)}"

        shortlist_summary.append({
            "name": item.get("name"),
            "location": item.get("location"),
            "cuisines": cuisines,
            "rating_value": rest_rating,
            "rating_evaluation": rating_status,
            "budget_evaluation": budget_status
        })
        
    cuisine_text = f" serving {user_prefs['cuisine']} food" if user_prefs.get('cuisine') else ""
    budget_text = f" with a maximum budget of ₹{int(user_max_budget)}" if user_max_budget else ""
    extra_prefs_text = f"\nThey have additional preferences: {user_prefs['extra_preferences']}." if user_prefs.get('extra_preferences') else ""
        
    prompt = f"""
You are a strict restaurant evaluation assistant.

The user is looking for a restaurant in {user_prefs['location']}{cuisine_text}{budget_text}.{extra_prefs_text}

Based on the user's request, here is the shortlisted data:
{json.dumps(shortlist_summary, indent=2)}

Task: Provide an evaluation for each restaurant in the shortlist.
You MUST use the pre-calculated evaluation fields provided in the data. Do NOT calculate your own comparisons.

Strict rules for the "explanation":
1. State the evaluated fields based ONLY on the provided data.
2. For Location, state matching location.
3. For Cuisine, state matching cuisines.
4. For Rating, output the EXACT `rating_evaluation` string provided.
5. For Budget, output the EXACT `budget_evaluation` string provided.
6. For Extra Preferences, evaluate them individually ONLY if user provided them.
7. Always use correct Indian currency symbol (₹) when discussing money. Do NOT use $.

The final text must be a structured string inside this JSON layout:
{{
  "recommendations": [
    {{
      "name": "restaurant name",
      "explanation": "Location: ... \\nCuisine: ... \\nRating: ... \\nBudget: ... \\nMatch Summary: ..."
    }}
  ]
}}
"""
    return prompt.strip()

