from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from src.phase4_api.schemas import RecommendRequest, RecommendResponse, RecommendationItem
from src.phase2_filtering.models import UserPreferences
from src.phase2_filtering.filter_engine import FilterEngine
from src.phase3_llm.prompt_builder import build_prompt
from src.phase3_llm.groq_client import GroqLLMClient
from src.phase5_infra.cache import RecommendationCache
from src.phase5_infra.logger import logger
import os

app = FastAPI(title="Restaurant Recommender API")

filter_engine = FilterEngine()
llm_client = GroqLLMClient()
cache = RecommendationCache()

web_dir = os.path.join(os.path.dirname(__file__), '../../web')
os.makedirs(web_dir, exist_ok=True)
app.mount("/static", StaticFiles(directory=web_dir), name="static")

@app.get("/")
def read_root():
    return FileResponse(os.path.join(web_dir, "index.html"))

@app.get("/locations", response_model=list[str])
def get_locations():
    return filter_engine.get_unique_locations()

@app.post("/recommend", response_model=RecommendResponse)
def get_recommendations(request: RecommendRequest):
    logger.info("Received recommendation request", extra={"extra_info": {"request": request.model_dump()}})
    
    cached_result = cache.get(request.model_dump())
    if cached_result:
        logger.info("Serving from cache")
        return cached_result
        
    prefs = UserPreferences(
        location=request.location,
        cuisine=request.cuisine,
        min_rating=request.min_rating,
        max_budget=request.max_budget,
        extra_preferences=request.extra_preferences
    )
    
    filter_result = filter_engine.filter_restaurants(prefs)
    
    if not filter_result.reason_code.startswith("SUCCESS") or not filter_result.restaurants:
        response = RecommendResponse(reason_code=filter_result.reason_code, results=[])
        cache.set(request.model_dump(), response.model_dump())
        return response
        
    shortlist = filter_result.restaurants
    
    user_prefs_dict = request.model_dump()
    user_min_rating = round(float(user_prefs_dict.get('min_rating', 0.0)), 1)
    user_max_budget = float(user_prefs_dict.get('max_budget', 0.0)) if user_prefs_dict.get('max_budget') else None
    
    needs_llm = bool(user_prefs_dict.get('extra_preferences'))
    
    if needs_llm:
        prompt = build_prompt(user_prefs_dict, shortlist)
        llm_output = llm_client.generate_recommendations(prompt)
        llm_recs = {r.get('name', '').lower(): r.get('explanation', '') for r in llm_output.get('recommendations', [])}
    else:
        llm_recs = {}
        
    final_results = []
    for item in shortlist:
        name_lower = item['name'].lower()
        rest_rating = round(float(item.get('rating', 0.0)), 1)
        rest_cost = float(item.get('cost_for_two', 0.0))
        
        # Precise Rating Logic
        if rest_rating < user_min_rating:
            rating_eval = "Does not meet your rating preference"
        elif rest_rating == user_min_rating:
            rating_eval = "Matches your rating preference"
        else:
            rating_eval = "Exceeds your rating expectation"
            
        # Precise Budget Logic
        if user_max_budget is not None:
            if rest_cost <= user_max_budget:
                budget_eval = f"Within budget limit (₹{int(rest_cost)})"
            else:
                budget_eval = f"Exceeds budget limit (₹{int(rest_cost)})"
        else:
            budget_eval = f"₹{int(rest_cost)} for two"
            
        # Output mapping
        lines = []
        lines.append(f"Location: {item.get('location', user_prefs_dict.get('location'))}")
        
        cuisines = item.get('cuisines', [])
        cuisine_str = ', '.join(cuisines) if isinstance(cuisines, list) else str(cuisines)
        lines.append(f"Cuisine: {cuisine_str}")
        lines.append(f"Rating: {rest_rating} ({rating_eval})")
        lines.append(f"Budget: {budget_eval}")
        
        if needs_llm:
            llm_exp = llm_recs.get(name_lower, "")
            if llm_exp:
                lines.append(llm_exp)
            else:
                lines.append(f"Extra Preferences: Evaluated via context")
        else:
            lines.append("Match Summary: Matches your rating preference")
            
        merged_item = item.copy()
        merged_item['explanation'] = "\n".join(lines)
        final_results.append(RecommendationItem(**merged_item))
        
    response = RecommendResponse(reason_code="SUCCESS", results=final_results)
    
    cache.set(request.model_dump(), response.model_dump())
    logger.info(f"Returning {len(final_results)} recommendations")
    return response

if __name__ == "__main__":
    import uvicorn
    import os
    from src.config import config
    port = int(os.environ.get("PORT", config['app']['port']))
    uvicorn.run(app, host=config['app']['host'], port=port)

