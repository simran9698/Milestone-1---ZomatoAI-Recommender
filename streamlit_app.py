import streamlit as st
import pandas as pd
import json
from src.phase2_filtering.models import UserPreferences
from src.phase2_filtering.filter_engine import FilterEngine
from src.phase3_llm.prompt_builder import build_prompt
from src.phase3_llm.groq_client import GroqLLMClient
from src.phase5_infra.logger import logger

st.set_page_config(
    page_title="Zomato AI | Restaurant Recommender",
    page_icon="🍽️",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Hide Streamlit standard UI elements completely
st.markdown("""
    <style>
        #MainMenu {visibility: hidden;}
        header {visibility: hidden;}
        footer {visibility: hidden;}
        .stApp {
            background: #0b0f19 !important;
        }
        .block-container {
            padding: 0 !important;
            max-width: 100% !important;
        }
        iframe {
            border: none !important;
        }
    </style>
""", unsafe_allow_html=True)

# Initialize engines
@st.cache_resource
def load_engines():
    return FilterEngine(), GroqLLMClient()

filter_engine, llm_client = load_engines()

# Get unique locations
locations = filter_engine.get_unique_locations()

# Get query params
query_params = st.query_params

results = None
prefs = {}

if query_params.get("submitted") == "true":
    try:
        prefs = {
            "location": query_params.get("location"),
            "cuisine": query_params.get("cuisine") if query_params.get("cuisine") else None,
            "min_rating": float(query_params.get("min_rating", 0.0)),
            "max_budget": float(query_params.get("max_budget", 1000)),
            "extra_preferences": query_params.get("extra_preferences") if query_params.get("extra_preferences") else None
        }
        
        user_prefs = UserPreferences(
            location=prefs["location"],
            cuisine=prefs["cuisine"],
            min_rating=prefs["min_rating"],
            max_budget=prefs["max_budget"],
            extra_preferences=prefs["extra_preferences"]
        )
        
        filter_result = filter_engine.filter_restaurants(user_prefs)
        
        if not filter_result.reason_code.startswith("SUCCESS") or not filter_result.restaurants:
            results = []
        else:
            shortlist = filter_result.restaurants
            prompt = build_prompt(user_prefs.model_dump(), shortlist)
            llm_output = llm_client.generate_recommendations(prompt)
            final_results_raw = llm_client.merge_with_catalog(llm_output, shortlist)
            results = final_results_raw
            
    except Exception as e:
        results = {"error": str(e)}

# Load index.html
with open("streamlit_component/index.html", "r", encoding="utf-8") as f:
    html_content = f.read()

# Inject data
data_script = f"""
<script>
  window.STREAMLIT_DATA = {{
    locations: {json.dumps(locations)},
    results: {json.dumps(results)},
    prefs: {json.dumps(prefs)}
  }};
</script>
"""

html_content = html_content.replace('<script id="data-placeholder"></script>', data_script)

# Render HTML
st.components.v1.html(html_content, height=2000, scrolling=True)



