import streamlit as st
import pandas as pd
import random

# --- 1. ETL DATA LOAD ---
def load_data():
    data = {
        "Category": ["Anxiety"] * 5 + ["Purpose"] * 5,
        "Day": [1, 2, 3, 4, 5] * 2,
        "Scripture": ["Phil 4:6", "John 14:27", "Matt 11:28", "Psalm 23", "Isa 41:10"] * 2,
        "Verse": [
            "Do not be anxious about anything...", 
            "My peace I give to you...", 
            "Come to me, all who are weary...", 
            "The Lord is my shepherd...", 
            "I will strengthen you and help you..."
        ] * 2,
        "Challenge": [
            "What is the one thing you are trying to control today?",
            "Identify a situation where you are choosing fear over peace.",
            "Where are you carrying a burden Jesus never asked you to bear?",
            "Are you following the Shepherd or the crowd today?",
            "Where do you feel 'weak' and need God's right hand?"
        ] * 2,
        "Devotion": [
            "Surrender is the bridge to peace...",
            "Peace is a person (Jesus), not a feeling...",
            "His yoke is easy and His burden is light...",
            "He leads us beside quiet waters for a reason...",
            "God's strength is made perfect in our weakness..."
        ] * 2,
        "Spirit_Prompt": ["Ask: What can I let go?", "Ask: Where is Your peace?", "Ask: Can I rest?", "Ask: Where next?", "Ask: Help me stand."] * 2
    }
    return pd.DataFrame(data)

# --- 2. SESSION STATE ---
if "current_day" not in st.session_state: st.session_state.current_day = 1
if "day_completed" not in st.session_state: st.session_state.day_completed = False
if "streak" not in st.session_state: st.session_state.streak = 0
if "badges" not in st.session_state: st.session_state.badges = []
if "missed_days" not in st.session_state: st.session_state.missed_days = 0
if "active_tab" not in st.session_state: st.session_state.active_tab = "Daily Walk"
if "tester_feedback" not in st.session_state: st.session_state.tester_feedback = False

# --- 3. CSS STYLING ---
st.markdown("""
    <style>
    .badge-card { background-color: #ffffff; padding: 8px; border-radius: 8px; border: 1px solid #e0e0e0; margin-bottom: 5px; text-align: center; }
    .streak-box { background-color: #FFF9C4; padding: 10px; border-radius: 10px; text-align: center; font-weight: bold; border: 1px solid #FBC02D; margin-bottom: 20px; }
    
    /* Main Action Buttons */
    button[key="complete_btn"] { background-color: #90EE90 !important; color: black !important; font-weight: bold !important; }
    button[key="help_btn"] { background-color: #FFCCCB !important; color: black !important; font-weight: bold !important; }
    
    /* Tester Buttons - HIGH CONTRAST GOLD */
    button[key^="tester"] {
        background-color: #FFD700 !important;
        color: #000000 !important;
        border: 2px solid #B8860B !important;
        font-weight: 800 !important;
    }
    </style>
""", unsafe_allow_html=True)

# --- 4. SIDEBAR ---
df = load_data()
st.sidebar.title("🕊️ SpiritWalk")
nav_choice = st.sidebar.radio("Navigation", ["Daily Walk", "🆘 Request Coaching"])

st.sidebar.divider()
st.sidebar.subheader("🏆 Achievement Case")
for badge in st.session_state.badges:
    st.sidebar.markdown(f"<div class='badge-card'>🏅 <b>{badge}</b></div>", unsafe_allow_html=True)

st.sidebar.divider()
st.sidebar.subheader("🛠️ Tester Suite")

if st.sidebar.button("🚀 FAST-TRACK DAY 3", key="tester_3", use_container_width=True):
    st.session_state.current_day = 3
    st.session_state.streak = 3
    st.session_state.tester_feedback = True
    if "Trinity Walker" not in st.session_state.badges: st.session_state.badges.append("Trinity Walker")
    st.rerun()

if st.sidebar.button("⚠️ MISS 1 DAY (SHIELD)", key="tester_shield", use_container_width=True):
    st.session_state.missed_days = 1
    st.session_state.tester_feedback = True
    st.rerun()

if st.sidebar.button("🚨 MISS 3 DAYS (RESET)", key="tester_reset", use_container_width=True):
    st.session_state.streak = 0
    st.session_state.missed_days = 3
    st.session_state.tester_feedback = True
    st.rerun()

# --- 5. MAIN INTERFACE ---
if nav_choice == "Daily Walk":
    st.markdown(f"<div class='streak-box'>🔥 Spirit Streak: {st.session_state.streak} Days</div>", unsafe_allow_html=True)
    
    # Tester Feedback Collector
    if st.session_state.tester_feedback:
        with st.expander("🛠️ Tester Feedback: How did that simulation feel?", expanded=True):
            f_back = st.text_input("Does the logic make sense?")
            if st.button("Submit Tester Note"):
                st.session_state.tester_feedback = False
                st.success("Note captured! Continuing test...")
                st.rerun()

    category = st.selectbox("Focus Track:", df["Category"].unique())
    day_data = df[(df["Category"] == category) & (df["Day"] == st.session_state.current_day)]
    
    if not day_data.empty:
        selected = day_data.iloc[0]
        v_text = selected['Verse']
        s_ref = selected['Scripture']
        p_text = selected['Spirit_Prompt']

        # Scripture Card
        st.markdown(f"""<div style="background-color:#f8f9fa;padding:20px;border-radius:10px;border-left:5px solid #6c757d;margin-bottom:20px;">
            <i style="color:#333;">"{v_text}"</i><br><b style="color:#666;">— {s_ref}</b>
