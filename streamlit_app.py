import streamlit as st
import pandas as pd
import json
from src.phase2_filtering.models import UserPreferences
from src.phase2_filtering.filter_engine import FilterEngine
from src.phase3_llm.prompt_builder import build_prompt
from src.phase3_llm.groq_client import GroqLLMClient
from src.phase5_infra.logger import logger
import streamlit.components.v1 as components

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
    </style>
""", unsafe_allow_html=True)

# Initialize engines
@st.cache_resource
def load_engines():
    return FilterEngine(), GroqLLMClient()

filter_engine, llm_client = load_engines()

# Declare the custom component
my_component = components.declare_component("zomato_ui", path="streamlit_component")

# Get unique locations
locations = filter_engine.get_unique_locations()

# State to hold results
if 'results' not in st.session_state:
    st.session_state.results = None

# Render the component and capture interactions
component_value = my_component(
    locations=locations, 
    results=st.session_state.results
)

# Handle interactions from the custom UI
if component_value:
    prefs_dict = component_value
    
    # Check if preferences changed to prevent infinite loop
    if 'last_prefs' not in st.session_state or st.session_state.last_prefs != prefs_dict:
        st.session_state.last_prefs = prefs_dict
        
        try:
            prefs = UserPreferences(
                location=prefs_dict['location'],
                cuisine=prefs_dict['cuisine'],
                min_rating=prefs_dict['min_rating'],
                max_budget=prefs_dict['max_budget'],
                extra_preferences=prefs_dict['extra_preferences']
            )
            
            filter_result = filter_engine.filter_restaurants(prefs)
            
            if not filter_result.reason_code.startswith("SUCCESS") or not filter_result.restaurants:
                st.session_state.results = []
            else:
                shortlist = filter_result.restaurants
                prompt = build_prompt(prefs.model_dump(), shortlist)
                llm_output = llm_client.generate_recommendations(prompt)
                final_results_raw = llm_client.merge_with_catalog(llm_output, shortlist)
                
                st.session_state.results = final_results_raw
        except Exception as e:
            st.session_state.results = {"error": str(e)}
            
        st.rerun()


