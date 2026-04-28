from pydantic import BaseModel
from typing import List, Optional

class RestaurantClean(BaseModel):
    name: str
    location: str
    cuisines: List[str]
    cost_for_two: float
    rating: float
    votes: int
