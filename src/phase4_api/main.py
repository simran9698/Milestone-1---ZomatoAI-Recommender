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
    
    prompt = build_prompt(request.model_dump(), shortlist)
    llm_output = llm_client.generate_recommendations(prompt)
    
    final_results_raw = llm_client.merge_with_catalog(llm_output, shortlist)
    
    final_results = [RecommendationItem(**item) for item in final_results_raw]
    response = RecommendResponse(reason_code="SUCCESS", results=final_results)
    
    cache.set(request.model_dump(), response.model_dump())
    logger.info(f"Returning {len(final_results)} recommendations")
    return response

if __name__ == "__main__":
    import uvicorn
    from src.config import config
    uvicorn.run(app, host=config['app']['host'], port=config['app']['port'])
