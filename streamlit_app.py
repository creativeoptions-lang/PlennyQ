import streamlit as st
import pandas as pd

# 1. DATA LOAD
def load_data():
    data = {
        "Category": ["Anxiety", "Purpose", "Relationships"],
        "Day": [1, 1, 1],
        "Scripture": ["Philippians 4:6-7", "Ephesians 2:10", "1 Peter 4:8"],
        "Verse": [
            "Do not be anxious about anything...",
            "For we are God’s handiwork...",
            "Above all, love each other deeply..."
        ],
        "Challenge": [
            "What is the one thing you are trying to control today?",
            "Identify one gift you have been hiding out of fear.",
            "Who is the person you find hardest to extend grace to?"
        ],
        "Devotion": [
            "Surrender is the bridge to peace. When we stop managing outcomes, we start trusting the Provider.",
            "You were designed with intention. Your purpose isn't found, it's unleashed through obedience.",
            "Grace is the oxygen of a relationship. Breathe it in from God and exhale it toward others."
        ],
        "Spirit_Prompt": ["Ask the Spirit...", "Ask the Spirit...", "Ask the Spirit..."]
    }
    return pd.DataFrame(data)

# 2. SESSION STATE MANAGEMENT
if "active_tab" not in st.session_state:
    st.session_state.active_tab = "Daily Walk"

# 3. CSS FOR CUSTOM BUTTON COLORS
st.markdown("""
    <style>
    /* Targeting the 'Complete Day' Button (Green) */
    div.stButton > button:first-child {
        background-color: #90EE90 !important;
        color: black !important;
        border: none;
    }
    /* Targeting the 'Get Help' Button (Red) */
    div.stColumns > div:nth-child(2) button {
        background-color: #FFCCCB !important;
        color: black !important;
        border: none;
    }
    </style>
""", unsafe_allow_html=True)

# 4. NAVIGATION
df = load_data()
tabs = ["Daily Walk", "🆘 Request Coaching"]
active_tab = st.sidebar.radio("Navigation", tabs, index=tabs.index(st.session_state.active_tab))

if active_tab == "Daily Walk":
    st.title("🕊️ SpiritWalk")
    category = st.selectbox("Select Your Focus:", df["Category"].unique())
    selected = df[df["Category"] == category].iloc[0]

    # Scripture Card
    st.markdown(f"""<div style="background-color:#f8f
