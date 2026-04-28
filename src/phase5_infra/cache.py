import hashlib
import json
from src.phase5_infra.logger import logger

class RecommendationCache:
    def __init__(self):
        self.cache = {}
        
    def _generate_key(self, request_dict: dict) -> str:
        key_str = json.dumps(request_dict, sort_keys=True)
        return hashlib.md5(key_str.encode()).hexdigest()
        
    def get(self, request_dict: dict):
        key = self._generate_key(request_dict)
        return self.cache.get(key)
        
    def set(self, request_dict: dict, response_dict: dict):
        key = self._generate_key(request_dict)
        self.cache[key] = response_dict
        logger.info(f"Cached response for key {key}")
