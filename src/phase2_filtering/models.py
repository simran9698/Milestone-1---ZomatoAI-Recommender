from pydantic import BaseModel
from typing import Optional, List, Dict, Any

class UserPreferences(BaseModel):
    location: str
    cuisine: Optional[str] = None
    min_rating: Optional[float] = 0.0
    max_budget: Optional[float] = float('inf')
    extra_preferences: Optional[str] = None

class RecommendationResult(BaseModel):
    restaurants: List[Dict[str, Any]]
    reason_code: str
