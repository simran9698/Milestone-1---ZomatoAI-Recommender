from pydantic import BaseModel
from typing import List, Optional

class RecommendRequest(BaseModel):
    location: str
    cuisine: Optional[str] = None
    min_rating: Optional[float] = 0.0
    max_budget: Optional[float] = float('inf')
    extra_preferences: Optional[str] = None

class RecommendationItem(BaseModel):
    name: str
    location: str
    cuisines: List[str]
    cost_for_two: float
    rating: float
    votes: int
    explanation: str

class RecommendResponse(BaseModel):
    reason_code: str
    results: List[RecommendationItem]
