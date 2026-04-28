import pandas as pd
from src.phase2_filtering.models import UserPreferences, RecommendationResult
from src.config import config
from src.phase5_infra.logger import logger

class FilterEngine:
    def __init__(self, data_path: str = None):
        self.data_path = data_path or config['data']['processed_path']
        try:
            self.df = pd.read_parquet(self.data_path)
            logger.info(f"Loaded {len(self.df)} records for filtering")
        except Exception as e:
            logger.error(f"Failed to load processed data: {e}")
            self.df = pd.DataFrame()

    def get_unique_locations(self) -> list[str]:
        if self.df.empty:
            return []
        locations = self.df['location'].dropna().unique().tolist()
        return sorted([str(loc).title() for loc in locations])

    def filter_restaurants(self, prefs: UserPreferences) -> RecommendationResult:
        if self.df.empty:
            return RecommendationResult(restaurants=[], reason_code="DATA_UNAVAILABLE")

        df_filtered = self.df.copy()

        # Exclude restaurants with missing prices (represented as 0.0)
        df_filtered = df_filtered[df_filtered['cost_for_two'] > 0]

        # 1. Location filter
        df_filtered = df_filtered[df_filtered['location'] == prefs.location.lower().strip()]
        if df_filtered.empty:
            return RecommendationResult(restaurants=[], reason_code="NO_MATCH_LOCATION")

        # 2. Cuisine filter
        if prefs.cuisine:
            cuisine_target = prefs.cuisine.lower().strip()
            df_filtered = df_filtered[df_filtered['cuisines'].apply(lambda c_list: cuisine_target in [str(c).lower().strip() for c in c_list] if hasattr(c_list, '__iter__') and not isinstance(c_list, str) else False)]
            if df_filtered.empty:
                return RecommendationResult(restaurants=[], reason_code="NO_MATCH_CUISINE")

        max_size = config['recommendation']['max_shortlist_size']
        reason_code = "SUCCESS"
        
        df_after_cuisine = df_filtered.copy()

        # 3. Rating filter
        df_after_rating = df_after_cuisine.copy()
        if prefs.min_rating is not None:
            df_after_rating = df_after_cuisine[df_after_cuisine['rating'] >= prefs.min_rating]
            
        # 4. Budget filter
        df_final = df_after_rating.copy()
        if prefs.max_budget is not None:
            df_final = df_after_rating[df_after_rating['cost_for_two'] <= prefs.max_budget]
            
        # Relaxation Logic
        if len(df_final) < max_size and prefs.min_rating is not None:
            relaxed_rating = prefs.min_rating - 0.5
            logger.info(f"Relaxing min_rating from {prefs.min_rating} to {relaxed_rating}")
            
            df_relaxed_rating = df_after_cuisine[df_after_cuisine['rating'] >= relaxed_rating]
            df_relaxed_final = df_relaxed_rating.copy()
            if prefs.max_budget is not None:
                df_relaxed_final = df_relaxed_rating[df_relaxed_rating['cost_for_two'] <= prefs.max_budget]
                
            if len(df_relaxed_final) > len(df_final):
                df_final = df_relaxed_final
                df_after_rating = df_relaxed_rating
                reason_code = "SUCCESS_RELAXED_RATING"

        # Determine Reason Codes
        if df_final.empty:
            if df_after_rating.empty:
                return RecommendationResult(restaurants=[], reason_code="NO_MATCH_RATING")
            else:
                return RecommendationResult(restaurants=[], reason_code="NO_MATCH_BUDGET")

        # Ranking
        df_filtered = df_final.sort_values(by=['rating', 'votes'], ascending=[False, False])
        df_filtered = df_filtered.drop_duplicates(subset=['name', 'location'])
        
        # Limit
        shortlist = df_filtered.head(max_size).to_dict('records')

        return RecommendationResult(restaurants=shortlist, reason_code=reason_code)
