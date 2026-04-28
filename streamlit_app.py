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
    layout="centered",
    initial_sidebar_state="collapsed"
)

# Hide Streamlit standard header/footer and inject gorgeous styles
st.markdown("""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&display=swap');
        
        #MainMenu {visibility: hidden;}
        header {visibility: hidden;}
        footer {visibility: hidden;}
        
        .stApp {
            background-color: #0b0f19 !important;
            background-image: radial-gradient(circle at 50% 30%, rgba(183, 18, 42, 0.15), transparent 60%) !important;
            font-family: 'Plus Jakarta Sans', sans-serif !important;
            color: #f8fafc !important;
        }
        
        /* Style standard Streamlit inputs to match glassmorphic theme */
        div[data-testid="stSelectbox"], div[data-testid="stTextInput"], div[data-testid="stNumberInput"] {
            background: rgba(255, 255, 255, 0.04) !important;
            backdrop-filter: blur(10px);
            border: 1px solid rgba(255, 255, 255, 0.08) !important;
            border-radius: 0.75rem !important;
        }
        
        /* Premium Card layout for Results */
        .restaurant-card {
            background: rgba(255, 255, 255, 0.04);
            backdrop-filter: blur(12px);
            border: 1px solid rgba(255, 255, 255, 0.08);
            border-radius: 1.25rem;
            padding: 2rem;
            margin-bottom: 2rem;
            display: flex;
            flex-direction: column;
            gap: 1.5rem;
        }
        .card-header { display: flex; justify-content: space-between; align-items: flex-start; }
        .card-title h3 { font-size: 1.5rem; font-weight: 700; color: white; margin-bottom: 0.25rem; }
        .card-title p { color: #94a3b8; font-size: 0.95rem; }
        .rating-badge {
            background: rgba(226, 55, 68, 0.15);
            color: #E23744;
            padding: 0.4rem 0.8rem;
            border-radius: 0.75rem;
            font-weight: 700;
            font-size: 0.95rem;
        }
        .card-stats {
            display: flex;
            flex-direction: column;
            gap: 0.75rem;
            padding: 1.25rem 0;
            border-top: 1px solid rgba(255, 255, 255, 0.08);
            border-bottom: 1px solid rgba(255, 255, 255, 0.08);
        }
        .stat { display: flex; align-items: center; gap: 0.75rem; font-size: 0.95rem; color: #e2e8f0; }
        .explanation {
            background: rgba(0, 0, 0, 0.25);
            padding: 1.25rem;
            border-radius: 0.75rem;
            font-size: 0.95rem;
            color: #cbd5e1;
            border-left: 4px solid #E23744;
        }
        .explanation strong { color: #E23744; display: block; margin-bottom: 0.5rem; }
        
        /* Customize the primary button */
        button[kind="primary"] {
            background: linear-gradient(135deg, #E23744 0%, #b52339 100%) !important;
            border: none !important;
            border-radius: 0.75rem !important;
            font-weight: 700 !important;
            height: 50px !important;
        }
    </style>
""", unsafe_allow_html=True)

# Hero section
st.markdown("""
    <div style="text-align: center; margin-bottom: 2.5rem; margin-top: 1.5rem;">
        <h1 style="font-size: 2.8rem; font-weight: 800; letter-spacing: -0.04em; color: white; margin-bottom: 0.5rem;">
            Zomato<span style="color: #E23744;">AI Recommender</span>
        </h1>
        <h3 style="font-size: 1.3rem; font-weight: 600; color: #e2e8f0; margin-bottom: 1rem;">
            Craving something specific?
        </h3>
        <p style="color: #94a3b8; font-size: 1.1rem; max-width: 600px; margin: 0 auto;">
            Let AI find the perfect table for your taste, mood, and budget.
        </p>
    </div>
""", unsafe_allow_html=True)

filter_engine = FilterEngine()
llm_client = GroqLLMClient()

locations = filter_engine.get_unique_locations()

# Search Form using native widgets
with st.form(key="search_form"):
    selected_location = st.selectbox("📍 Select Location", options=locations, index=None, placeholder="Where do you want to eat?")
    
    col1, col2 = st.columns(2)
    with col1:
        cuisine_input = st.text_input("🍳 Cuisine (Optional)", placeholder="e.g. Italian, Chinese, Biryani")
    with col2:
        min_rating = st.slider("⭐ Minimum Rating", min_value=0.0, max_value=5.0, value=0.0, step=0.1)
        
    col3, col4 = st.columns(2)
    with col3:
        max_budget = st.number_input("💰 Max Budget for Two (₹)", min_value=0, value=1000, step=100)
    with col4:
        extra_prefs = st.text_input("✨ Extra Preferences (Optional)", placeholder="e.g. outdoor seating, quiet for dates")
        
    submit_btn = st.form_submit_button("Find Places", type="primary", use_container_width=True)

if submit_btn:
    if not selected_location:
        st.error("🚨 Please select a location to start searching!")
    else:
        with st.spinner("🔍 Analyzing catalog and generating tailored AI recommendations..."):
            try:
                user_prefs = UserPreferences(
                    location=selected_location,
                    cuisine=cuisine_input if cuisine_input.strip() else None,
                    min_rating=float(min_rating),
                    max_budget=float(max_budget),
                    extra_preferences=extra_prefs if extra_prefs.strip() else None
                )
                
                filter_result = filter_engine.filter_restaurants(user_prefs)
                
                if not filter_result.reason_code.startswith("SUCCESS") or not filter_result.restaurants:
                    st.info(f"ℹ️ No direct matches found for your criteria. (Reason: {filter_result.reason_code})")
                else:
                    shortlist = filter_result.restaurants
                    prompt = build_prompt(user_prefs.model_dump(), shortlist)
                    llm_output = llm_client.generate_recommendations(prompt)
                    final_results = llm_client.merge_with_catalog(llm_output, shortlist)
                    
                    st.success(f"🎉 Found {len(final_results)} delicious recommendations for you!")
                    st.markdown("<br>", unsafe_allow_html=True)
                    
                    for res in final_results:
                        st.markdown(f"""
                            <div class="restaurant-card">
                                <div class="card-header">
                                    <div class="card-title">
                                        <h3>{res['name']}</h3>
                                        <p>{', '.join(res['cuisines']) if isinstance(res['cuisines'], list) else res['cuisines']}</p>
                                    </div>
                                    <div class="rating-badge">
                                        ⭐ {res['rating']:.1f}
                                    </div>
                                </div>
                                <div class="card-stats">
                                    <div class="stat">📍 <b>Location:</b> {res['location'].title()}</div>
                                    <div class="stat">💰 <b>Cost for Two:</b> ₹{res['cost_for_two']}</div>
                                    <div class="stat">👥 <b>Votes:</b> {res['votes']}</div>
                                </div>
                                <div class="explanation">
                                    <strong>💡 AI Analysis</strong>
                                    {res['explanation']}
                                </div>
                            </div>
                        """, unsafe_allow_html=True)
                        
            except Exception as e:
                st.error(f"🚨 Error generating recommendations: {str(e)}")
