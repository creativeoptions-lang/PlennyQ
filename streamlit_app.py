import streamlit as st
import pandas as pd
import random

# 1. DATA LOAD
def load_data():
    data = {
        "Category": ["Anxiety"] * 5 + ["Purpose"] * 5,
        "Day": [1, 2, 3, 4, 5] * 2,
        "Scripture": ["Phil 4:6", "John 14:27", "Matt 11:28", "Psalm 23", "Isa 41:10"] * 2,
        "Verse": ["Do not be anxious...", "My peace I give...", "Come to me all who are weary...", "The Lord is my shepherd...", "So do not fear..."] * 2,
        "Challenge": ["Control", "Fear vs Peace", "Rest", "Guidance", "Strength"] * 2,
        "Devotion": ["Surrender...", "Peace...", "Yoke...", "Paths...", "Right hand..."] * 2,
        "Spirit_Prompt": ["Prompt 1", "Prompt 2", "Prompt 3", "Prompt 4", "Prompt 5"] * 2
    }
    return pd.DataFrame(data)

# 2. SESSION STATE
if "current_day" not in st.session_state: st.session_state.current_day = 1
if "day_completed" not in st.session_state: st.session_state.day_completed = False
if "streak" not in st.session_state: st.session_state.streak = 0
if "badges" not in st.session_state: st.session_state.badges = []

# 3. CSS STYLING
st.markdown("""
    <style>
    .badge-card { background-color: #ffffff; padding: 8px; border-radius: 8px; border: 1px solid #e0e0e0; margin-bottom: 5px; text-align: center; }
    .streak-box { background-color: #FFF9C4; padding: 10px; border-radius: 10px; text-align: center; font-weight: bold; border: 1px solid #FBC02D; margin-bottom: 20px; }
    /* Button Colors */
    button[kind="secondary"]:nth-of-type(1) { background-color: #90EE90 !important; } 
    div.stColumns > div:nth-child(2) button { background-color: #FFCCCB !important; } 
    .stButton > button[key^="tester"] { background-color: #FFF59D !important; color: black !important; border: 1px solid #FBC02D !important; }
    </style>
""", unsafe_allow_html=True)

# 4. SIDEBAR
st.sidebar.title("🏆 Achievement Case")
if not st.session_state.badges:
    st.sidebar.info("Walk to earn badges!")
else:
    for badge in st.session_state.badges:
        st.sidebar.markdown(f"<div class='badge-card'>🏅 <b>{badge}</b></div>", unsafe_allow_html=True)

st.sidebar.divider()
st.sidebar.title("🛠️ Tester Suite")
if st.sidebar.button("🚀 Fast-Track to Day 3", key="tester_day3", use_container_width=True):
    st.session_state.current_day = 3
    st.session_state.streak = 3
    if "Trinity Walker" not in st.session_state.badges: st.session_state.badges.append("Trinity Walker")
    st.rerun()

# 5. MAIN LOGIC
df = load_data()
st.markdown(f"<div class='streak-box'>🔥 Current Spirit Streak: {st.session_state.streak} Days</div>", unsafe_allow_html=True)

# 6. CORE CONTENT
day_data = df[(df["Day"] == st.session_state.current_day)]
if not day_data.empty:
    selected = day_data.iloc[0]
    st.subheader(f"Day {st.session_state.current_day}")
    st.info(f"**Focus:** {selected['Challenge']}")
    
    journal_entry = st.text_area("Your Response", key="journal_input")

    col1, col2 = st.columns(2)
    with col1:
        if st.button("Complete Day", use_container_width=True):
            if journal_entry:
                st.session_state.day_completed = True
                st.session_state.streak += 1
                if st.session_state.streak == 1: st.session_state.badges.append("First Step")
                if st.session_state.streak == 3: st.session_state.badges.append("Trinity Walker")
                st.success("Day Saved!")
                st.rerun()

    with col2:
        if st.button("Get Help", use_container_width=True): st.toast("Coach notified.")

    # 7. BETA FEEDBACK TRIGGER (Unlocked at Day 3)
    if "Trinity Walker" in st.session_state.badges:
        st.divider()
        st.success("🎉 **Beta Tester Bonus Unlocked!**")
        with st.expander("📣 Give Feedback (Help us improve SpiritWalk)"):
            rating = st.select_slider("How is the daily flow?", options=["Too Hard", "Average", "Excellent"])
            feature_req = st.text_input("What one feature is missing?")
            if st.button("Submit Feedback"):
                st.balloons()
                st.write("Thank you! Your input is shaping the future of SpiritWalk.")

    if st.session_state.day_completed:
        st.divider()
        if st.button("✨ Step Into Next Day", type="primary", use_container_width=True):
            st.session_state.current_day += 1
            st.session_state.day_completed = False
            st.rerun()
