import streamlit as st
import pandas as pd
import random

# --- 1. ETL DATA LOAD (The App's "Brain") ---
def load_data():
    # In production, replace this with: return pd.read_csv("your_data.csv")
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

# --- 2. SESSION STATE MANAGEMENT ---
if "current_day" not in st.session_state: st.session_state.current_day = 1
if "day_completed" not in st.session_state: st.session_state.day_completed = False
if "streak" not in st.session_state: st.session_state.streak = 0
if "badges" not in st.session_state: st.session_state.badges = []
if "missed_days" not in st.session_state: st.session_state.missed_days = 0
if "active_tab" not in st.session_state: st.session_state.active_tab = "Daily Walk"

# --- 3. CUSTOM CSS STYLING ---
st.markdown("""
    <style>
    .badge-card { background-color: #ffffff; padding: 8px; border-radius: 8px; border: 1px solid #e0e0e0; margin-bottom: 5px; text-align: center; box-shadow: 2px 2px 5px rgba(0,0,0,0.05); }
    .streak-box { background-color: #FFF9C4; padding: 10px; border-radius: 10px; text-align: center; font-weight: bold; border: 1px solid #FBC02D; margin-bottom: 20px; }
    
    /* Button Coloring Logic */
    /* Complete Day - Light Green */
    div.stButton > button[key="complete_btn"] { background-color: #90EE90 !important; color: black !important; border: none; }
    /* Get Help - Light Red */
    div.stButton > button[key="help_btn"] { background-color: #FFCCCB !important; color: black !important; border: none; }
    /* Tester Buttons - Light Yellow */
    .stButton > button[key^="tester"] { background-color: #FFF59D !important; color: black !important; border: 1px solid #FBC02D !important; }
    </style>
""", unsafe_allow_html=True)

# --- 4. SIDEBAR & NAVIGATION ---
df = load_data()
st.sidebar.title("🕊️ SpiritWalk")
nav_choice = st.sidebar.radio("Navigation", ["Daily Walk", "🆘 Request Coaching"], index=0 if st.session_state.active_tab == "Daily Walk" else 1)

st.sidebar.divider()
st.sidebar.subheader("🏆 Achievement Case")
if not st.session_state.badges: st.sidebar.caption("Complete Day 1 to earn a badge.")
for badge in st.session_state.badges:
    st.sidebar.markdown(f"<div class='badge-card'>🏅 <b>{badge}</b></div>", unsafe_allow_html=True)

st.sidebar.divider()
st.sidebar.subheader("🛠️ Tester Suite")
if st.sidebar.button("🚀 Fast-Track Day 3", key="tester_3", use_container_width=True):
    st.session_state.current_day = 3
    st.session_state.streak = 3
    if "Trinity Walker" not in st.session_state.badges: st.session_state.badges.append("Trinity Walker")
    st.rerun()
if st.sidebar.button("⚠️ Miss 1 Day (Shield)", key="tester_shield", use_container_width=True):
    st.session_state.missed_days = 1
    st.rerun()
if st.sidebar.button("🚨 Miss 3 Days (Reset)", key="tester_reset_streak", use_container_width=True):
    st.session_state.streak = 0
    st.session_state.missed_days = 3
    st.rerun()

# --- 5. MAIN LOGIC: DAILY WALK ---
if nav_choice == "Daily Walk":
    st.markdown(f"<div class='streak-box'>🔥 Current Spirit Streak: {st.session_state.streak} Days</div>", unsafe_allow_html=True)
    
    category = st.selectbox("Focus Track:", df["Category"].unique())
    day_data = df[(df["Category"] == category) & (df["Day"] == st.session_state.current_day)]
    
    if not day_data.empty:
        selected = day_data.iloc[0]
        
        # Scripture Card
        st.markdown(f"""<div style="background-color:#f8f9fa;padding:20px;border-radius:10px;border-left:5px solid #6c757d;margin-bottom:20px;">
            <i style="color:#333;">"{selected['Verse']}"</i><br><b style="color:#666;">— {selected['Scripture']}</b>
        </div>""", unsafe_allow_html=True)

        if st.session_state.missed_days == 1:
            st.info("🛡️ **Shield Active:** Your streak is protected. Complete today to stay on track!")
        elif st.session_state.missed_days > 1:
            st.warning(f"Grace is new today! Rebuilding your streak after {st.session_state.missed_days} days.")

        st.subheader(f"Day {st.session_state.current_day}: The Challenge")
        st.info(selected['Challenge'])
        
        with st.expander("📖 View Daily Devotion"):
            st.write(selected['Devotion'])
            st.caption(f"**Holy Spirit Prompt:** {selected['Spirit_Prompt']}")

        journal_entry = st.text_area("Your Response", key="journal_input", placeholder="Record your thoughts...")

        # Interaction Buttons
        col1, col2 = st.columns(2)
        with col1:
            if st.button("Complete Day", key="complete_btn", use_container_width=True):
                if journal_entry:
                    st.session_state.day_completed = True
                    st.session_state.streak += 1
                    st.session_state.missed_days = 0
                    if st.session_state.streak == 1: st.session_state.badges.append("First Step")
                    if st.session_state.streak == 3: st.session_state.badges.append("Trinity Walker")
                    st.success("Breakthrough Saved!")
                    st.balloons()
                    st.rerun()
                else: st.error("Please enter a response.")
        
        with col2:
            if st.button("Get Help", key="help_btn", use_container_width=True):
                st.session_state.saved_journal = journal_entry
                st.session_state.active_tab = "🆘 Request Coaching"
                st.rerun()

        # Community Pulse
        st.divider()
        st.markdown(f"👥 **Community Pulse:** {random.randint(200, 500)} others are walking Day {st.session_state.current_day} with you.")

        # Beta Feedback (Unlocked at Day 3)
        if "Trinity Walker" in st.session_state.badges:
            with st.expander("📣 Beta Feedback"):
                st.select_slider("App Flow Rating", options=["1", "2", "3", "4", "5"])
                st.button("Submit Feedback")

        if st.session_state.day_completed:
            if st.button("✨ Step Into Next Day", type="primary", use_container_width=True):
                st.session_state.current_day += 1
                st.session_state.day_completed = False
                st.rerun()

# --- 6. MAIN LOGIC: COACHING ---
else:
    st.header("Connect with a Coach")
    context = st.session_state.get("saved_journal", "No entry provided.")
    st.text_area("Coach Context", value=f"Track: {st.session_state.get('category', 'General')}\nEntry: {context}\n\nI need help with...", height=200)
    if st.button("Send to Coach"): st.success("Coach notified!")
    if st.button("← Back to Walk"): 
        st.session_state.active_tab = "Daily Walk"
        st.rerun()
