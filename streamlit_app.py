import streamlit as st
import pandas as pd
import random

# --- 1. DATA LOAD ---
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
        "Challenge": ["Control", "Fear vs Peace", "Rest", "Guidance", "Strength"] * 2,
        "Devotion": ["Surrender...", "Peace...", "Yoke...", "Paths...", "Right hand..."] * 2,
        "Spirit_Prompt": ["Ask: What can I let go?", "Ask: Where is Your peace?", "Ask: Can I rest?", "Ask: Where next?", "Ask: Help me stand."] * 2
    }
    return pd.DataFrame(data)

# --- 2. SESSION STATE ---
for key, val in {
    "current_day": 1, "day_completed": False, "streak": 0, 
    "badges": [], "missed_days": 0, "active_tab": "Daily Walk", "tester_feedback": False
}.items():
    if key not in st.session_state: st.session_state[key] = val

# --- 3. STYLING ---
st.markdown("""
    <style>
    .badge-card { background-color: #fff; padding: 8px; border-radius: 8px; border: 1px solid #e0e0e0; margin-bottom: 5px; text-align: center; }
    .streak-box { background-color: #FFF9C4; padding: 10px; border-radius: 10px; text-align: center; font-weight: bold; border: 1px solid #FBC02D; margin-bottom: 20px; }
    button[key="complete_btn"] { background-color: #90EE90 !important; color: #000 !important; font-weight: bold !important; }
    button[key="help_btn"] { background-color: #FFCCCB !important; color: #000 !important; font-weight: bold !important; }
    button[key^="tester"] { background-color: #FFD700 !important; color: #000 !important; border: 2px solid #B8860B !important; font-weight: 800 !important; }
    </style>
""", unsafe_allow_html=True)

# --- 4. SIDEBAR ---
df = load_data()
st.sidebar.title("🕊️ SpiritWalk")
nav_choice = st.sidebar.radio("Navigation", ["Daily Walk", "🆘 Request Coaching"])

st.sidebar.divider()
st.sidebar.subheader("🏆 Achievement Case")
for b in st.session_state.badges:
    st.sidebar.markdown(f"<div class='badge-card'>🏅 <b>{b}</b></div>", unsafe_allow_html=True)

st.sidebar.divider()
st.sidebar.subheader("🛠️ Tester Suite")
if st.sidebar.button("🚀 FAST-TRACK DAY 3", key="tester_3", use_container_width=True):
    st.session_state.current_day, st.session_state.streak, st.session_state.tester_feedback = 3, 3, True
    if "Trinity Walker" not in st.session_state.badges: st.session_state.badges.append("Trinity Walker")
    st.rerun()
if st.sidebar.button("⚠️ MISS 1 DAY (SHIELD)", key="tester_shield", use_container_width=True):
    st.session_state.missed_days, st.session_state.tester_feedback = 1, True
    st.rerun()
if st.sidebar.button("🚨 MISS 3 DAYS (RESET)", key="tester_reset", use_container_width=True):
    st.session_state.streak, st.session_state.missed_days, st.session_state.tester_feedback = 0, 3, True
    st.rerun()

# --- 5. MAIN ---
if nav_choice == "Daily Walk":
    st.markdown(f"<div class='streak-box'>🔥 Spirit Streak: {st.session_state.streak} Days</div>", unsafe_allow_html=True)
    
    if st.session_state.tester_feedback:
        with st.expander("🛠️ Tester Feedback", expanded=True):
            if st.button("Submit Note"):
                st.session_state.tester_feedback = False
                st.rerun()

    category = st.selectbox("Focus Track:", df["Category"].unique())
    day_data = df[(df["Day"] == st.session_state.current_day)]
    
    if not day_data.empty:
        row = day_data.iloc[0]
        # REPLACED MULTI-LINE STRING WITH CLEAN CONCATENATION TO PREVENT SYNTAX ERROR
        card_style = "background-color:#f8f9fa;padding:20px;border-radius:10px;border-left:5px solid #6c757d;margin-bottom:20px;"
        scripture_html = f'<div style="{card_style}"><i style="color:#333;">"{row["Verse"]}"</i><br><b style="color:#666;">— {row["Scripture"]}</b></div>'
        st.markdown(scripture_html, unsafe_allow_html=True)

        if st.session_state.missed_days == 1: st.info("🛡️ Spirit Shield Active!")

        st.subheader(f"Day {st.session_state.current_day}")
        st.info(row['Challenge'])
        
        with st.expander("📖 View Daily Devotion"):
            st.write(row['Devotion'])
            st.caption(f"Spirit Prompt: {row['Spirit_Prompt']}")

        journal_entry = st.text_area("Your Response", key="journal_input")

        c1, c2 = st.columns(2)
        with c1:
            if st.button("Complete Day", key="complete_btn", use_container_width=True):
                if journal_entry:
                    st.session_state.day_completed, st.session_state.streak, st.session_state.missed_days = True, st.session_state.streak + 1, 0
                    if st.session_state.streak == 1: st.session_state.badges.append("First Step")
                    st.rerun()
        with c2:
            if st.button("Get Help", key="help_btn", use_container_width=True):
                st.session_state.saved_journal = journal_entry
                st.info("Switch tabs to send.")

        if st.session_state.day_completed:
            if st.button("✨ Step Into Next Day", type="primary", use_container_width=True):
                st.session_state.current_day += 1
                st.session_state.day_completed = False
                st.rerun()
else:
    st.header("Connect with a Coach")
    st.text_area("Context", value=st.session_state.get("saved_journal", ""), height=150)
    if st.button("Send"): st.success("Sent!")
