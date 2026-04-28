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
    initial_sidebar_state="expanded"
)

# Initialize engines
@st.cache_resource
def load_engines():
    return FilterEngine(), GroqLLMClient()

filter_engine, llm_client = load_engines()

st.title("🍽️ Zomato AI Restaurant Recommender")
st.markdown("Find the best places to eat tailored to your preferences.")

# Sidebar for inputs
with st.sidebar:
    st.header("Your Preferences")
    
    locations = filter_engine.get_unique_locations()
    location = st.selectbox("Location", options=[""] + locations, index=0)
    
    cuisine = st.text_input("Cuisine (Optional)", placeholder="e.g., Italian, Chinese")
    
    min_rating = st.slider("Minimum Rating", min_value=0.0, max_value=5.0, value=0.0, step=0.1)
    
    max_budget = st.number_input("Maximum Budget (₹ for two)", min_value=0, value=1000, step=100)
    
    extra_preferences = st.text_area("Extra Preferences (Optional)", placeholder="e.g., outdoor seating, vegan options")
    
    submit_btn = st.button("Find Recommendations", type="primary")

if submit_btn:
    if not location:
        st.error("Please select a location.")
    else:
        prefs = UserPreferences(
            location=location,
            cuisine=cuisine if cuisine else None,
            min_rating=min_rating,
            max_budget=float(max_budget) if max_budget else float('inf'),
            extra_preferences=extra_preferences if extra_preferences else None
        )
        
        with st.spinner("Filtering restaurants..."):
            filter_result = filter_engine.filter_restaurants(prefs)
            
        if not filter_result.reason_code.startswith("SUCCESS") or not filter_result.restaurants:
            st.info(f"No recommendations found. Reason: {filter_result.reason_code.replace('_', ' ')}")
        else:
            st.success(f"Found {len(filter_result.restaurants)} matching restaurants!")
            
            shortlist = filter_result.restaurants
            
            with st.spinner("Generating AI Analysis..."):
                prompt = build_prompt(prefs.model_dump(), shortlist)
                llm_output = llm_client.generate_recommendations(prompt)
                final_results_raw = llm_client.merge_with_catalog(llm_output, shortlist)
                
            # Display results
            for item in final_results_raw:
                with st.container():
                    col1, col2 = st.columns([1, 3])
                    with col1:
                        st.subheader(item['name'])
                        st.markdown(f"**Cuisines:** {', '.join(item['cuisines'])}")
                        st.markdown(f"**Location:** {item['location']}")
                        st.markdown(f"**Rating:** ⭐ {item['rating']} ({item['votes']} votes)")
                        st.markdown(f"**Cost for Two:** ₹{item['cost_for_two']}")
                    with col2:
                        st.info("**AI Analysis**\n\n" + item.get('explanation', 'N/A'))
                    st.divider()
