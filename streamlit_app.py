import streamlit as st
import pandas as pd

# 1. DATA LOAD
def load_data():
    data = {
        "Category": ["Anxiety", "Anxiety", "Purpose", "Purpose"],
        "Day": [1, 2, 1, 2],
        "Scripture": ["Philippians 4:6-7", "John 14:27", "Ephesians 2:10", "Jeremiah 29:11"],
        "Verse": ["Do not be anxious...", "Peace I leave...", "For we are God’s...", "For I know the plans..."],
        "Challenge": ["Control challenge", "Fear vs Peace", "Hidden gifts", "Future fear"],
        "Devotion": ["Surrender...", "Peace is a person...", "Intentional design...", "God's plans..."],
        "Spirit_Prompt": ["Prompt 1", "Prompt 2", "Prompt 3", "Prompt 4"]
    }
    return pd.DataFrame(data)

# 2. SESSION STATE
if "current_day" not in st.session_state:
    st.session_state.current_day = 1
if "day_completed" not in st.session_state:
    st.session_state.day_completed = False
if "streak" not in st.session_state:
    st.session_state.streak = 0

# 3. CSS STYLING (Colors for Nudges)
st.markdown("""
    <style>
    .streak-box {
        background-color: #FFF9C4;
        padding: 10px;
        border-radius: 10px;
        text-align: center;
        font-weight: bold;
        border: 1px solid #FBC02D;
        margin-bottom: 20px;
    }
    button[kind="secondary"]:nth-of-type(1) { background-color: #90EE90 !important; } /* Green */
    div.stColumns > div:nth-child(2) button { background-color: #FFCCCB !important; } /* Red */
    </style>
""", unsafe_allow_html=True)

# 4. DASHBOARD
df = load_data()
st.sidebar.title("🕊️ SpiritWalk")
category = st.sidebar.selectbox("Track:", df["Category"].unique())

# Streak Display
st.markdown(f"<div class='streak-box'>🔥 Current Spirit Streak: {st.session_state.streak} Days</div>", unsafe_allow_html=True)

# 5. CORE LOGIC
day_data = df[(df["Category"] == category) & (df["Day"] == st.session_state.current_day)]

if not day_data.empty:
    selected = day_data.iloc[0]
    
    st.subheader(f"Day {st.session_state.current_day}")
    st.info(f"**Today's Focus:** {selected['Challenge']}")
    
    with st.expander("📖 Daily Devotion"):
        st.write(selected['Devotion'])
    
    journal_entry = st.text_area("Your Response", key="journal_input")

    col1, col2 = st.columns(2)
    with col1:
        if st.button("Complete Day", use_container_width=True):
            if len(journal_entry) > 10: # Encouraging actual reflection
                st.session_state.day_completed = True
                st.session_state.streak += 1
                st.success("Breakthrough Recorded!")
                st.balloons()
                st.rerun()
            else:
                st.warning("The Spirit invites deeper reflection. Try writing a bit more!")

    with col2:
        if st.button("Get Help", use_container_width=True):
            st.toast("Connecting to Coach...")

    # 6. THE GENTLE NUDGE / GAMIFICATION
    st.divider()
    if not st.session_state.day_completed:
        st.markdown("### 🔒 Next Discovery")
        st.write("Complete today's walk to unlock tomorrow's revelation.")
        # Progress bar toward the next day
        st.progress(0)
        st.caption("Your journey is waiting for your 'Yes'.")
    else:
        st.markdown("### 🔓 Revelation Unlocked")
        st.progress(100)
        if st.button("✨ Step Into Day " + str(st.session_state.current_day + 1), type="primary", use_container_width=True):
            st.session_state.current_day += 1
            st.session_state.day_completed = False
            st.rerun()

---

### The Gamification Strategy
To create that "push ahead" excitement, we’ve used three psychological triggers:

1.  **The Spirit Streak:** A visible counter that rewards consistency. Users hate breaking a streak once it hits 3+ days.
2.  **Visual Scarcity (Progress Bar):** The progress bar sits at 0% until they submit. This creates a "need for closure" that encourages them to finish the journal entry.
3.  **Variable Reward:** The button for the next day changes from a "Locked" text to a "Shiny" Primary Blue button once completed.



### Deployment Note
Since you are testing this for an iPhone marketplace package, these "nudges" are exactly what Apple looks for in **User Engagement**. It shows the app isn't just a static document, but an interactive journey.

**Would you like me to add "Achievement Badges" (e.g., 'Prayer Warrior' for a 3-day streak) to the sidebar?**
