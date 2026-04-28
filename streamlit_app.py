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

# Hide Streamlit elements and apply custom dark theme
st.markdown("""
    <style>
        #MainMenu {visibility: hidden;}
        header {visibility: hidden;}
        footer {visibility: hidden;}
        
        .stApp {
            background: radial-gradient(circle at top, #1f242d 0%, #0e1117 100%) !important;
            color: #ffffff !important;
            font-family: 'Inter', sans-serif !important;
        }
        
        /* Custom Header Styles */
        .logo-container {
            display: flex;
            justify-content: center;
            align-items: center;
            gap: 10px;
            margin-top: 2rem;
            margin-bottom: 1rem;
        }
        .logo-text {
            font-size: 2.5rem;
            font-weight: bold;
            color: #e03546;
        }
        .title-text {
            font-size: 3.5rem;
            font-weight: 800;
            text-align: center;
            margin-bottom: 0.5rem;
            color: #ffffff;
        }
        .subtitle-text {
            font-size: 1.25rem;
            text-align: center;
            color: #8e95a5;
            margin-bottom: 3rem;
        }
        
        /* Input Labels */
        label {
            color: #8e95a5 !important;
            font-weight: 600 !important;
            font-size: 0.9rem !important;
        }
        
        /* Selectbox / Inputs */
        div[data-baseweb="select"] > div {
            background-color: #1e232d !important;
            border: 1px solid rgba(255, 255, 255, 0.1) !important;
            color: white !important;
        }
        input {
            background-color: #1e232d !important;
            color: white !important;
            border: 1px solid rgba(255, 255, 255, 0.1) !important;
        }
        textarea {
            background-color: #1e232d !important;
            color: white !important;
            border: 1px solid rgba(255, 255, 255, 0.1) !important;
        }
        
        /* Button */
        .stButton button {
            background-color: #e03546 !important;
            color: white !important;
            border: none !important;
            border-radius: 8px !important;
            padding: 0.75rem 2.5rem !important;
            font-weight: bold !important;
            font-size: 1.1rem !important;
            transition: all 0.3s ease !important;
            margin-top: 1rem;
        }
        .stButton button:hover {
            background-color: #ff4b5c !important;
            box-shadow: 0 4px 15px rgba(224, 53, 70, 0.4) !important;
            transform: translateY(-2px) !important;
        }
        
        /* Result Cards */
        .restaurant-card {
            background: rgba(30, 35, 45, 0.4);
            border-radius: 12px;
            padding: 1.5rem;
            margin-bottom: 1rem;
            border-left: 4px solid #e03546;
        }
    </style>
""", unsafe_allow_html=True)

# Initialize engines
@st.cache_resource
def load_engines():
    return FilterEngine(), GroqLLMClient()

filter_engine, llm_client = load_engines()

# Header Section
st.markdown("""
    <div class="logo-container">
        <span style="font-size: 2.5rem;">🍴</span>
        <span class="logo-text">ZomatoAI <span style="color: white;">Recommender</span></span>
    </div>
    <div class="title-text">Craving something specific?</div>
    <div class="subtitle-text">Let Zomato AI Recommender find the perfect table for your taste, mood, and budget.</div>
""", unsafe_allow_html=True)

# Form Section
locations = filter_engine.get_unique_locations()

col1, col2, col3, col4 = st.columns(4)

with col1:
    location = st.selectbox("Location", options=[""] + locations, index=0)
    
with col2:
    cuisine = st.text_input("Cuisine (Optional)", placeholder="e.g., Italian, Chinese")
    
with col3:
    min_rating = st.slider("Min Rating", min_value=0.0, max_value=5.0, value=0.0, step=0.1)
    
with col4:
    max_budget = st.number_input("Max Budget (₹)", min_value=0, value=1000, step=100)
    
extra_preferences = st.text_area("Extra Preferences (Optional)", placeholder="e.g., family-friendly, outdoor seating, quiet for dates")

submit_btn = st.button("Find Places →")

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
                st.markdown(f"""
                    <div class="restaurant-card">
                        <h3 style="color: #ffffff; margin-top: 0;">{item['name']}</h3>
                        <p style="color: #8e95a5; margin-bottom: 0.5rem;">
                            <strong>Cuisines:</strong> {', '.join(item['cuisines'])} | 
                            <strong>Location:</strong> {item['location']} | 
                            <strong>Rating:</strong> ⭐ {item['rating']} ({item['votes']} votes) | 
                            <strong>Cost for Two:</strong> ₹{item['cost_for_two']}
                        </p>
                        <div style="background: rgba(0, 0, 0, 0.2); padding: 1rem; border-radius: 8px; color: #fafafa;">
                            {item.get('explanation', 'N/A')}
                        </div>
                    </div>
                """, unsafe_allow_html=True)

