import streamlit as st
import pandas as pd

# 1. ENHANCED DATA LOAD (Added Day 2 for testing)
def load_data():
    data = {
        "Category": ["Anxiety", "Anxiety", "Purpose", "Purpose"],
        "Day": [1, 2, 1, 2],
        "Scripture": ["Philippians 4:6-7", "John 14:27", "Ephesians 2:10", "Jeremiah 29:11"],
        "Verse": [
            "Do not be anxious about anything...",
            "Peace I leave with you; my peace I give you...",
            "For we are God’s handiwork...",
            "For I know the plans I have for you..."
        ],
        "Challenge": [
            "What is the one thing you are trying to control today?",
            "Identify a situation where you are choosing fear over peace.",
            "Identify one gift you have been hiding out of fear.",
            "What is one 'future fear' stopping you from acting today?"
        ],
        "Devotion": [
            "Surrender is the bridge to peace.",
            "Peace is a person (Jesus), not just the absence of noise.",
            "You were designed with intention.",
            "God's plans are for your good, even when the path is blurry."
        ],
        "Spirit_Prompt": ["Ask the Spirit...", "Ask the Spirit...", "Ask the Spirit...", "Ask the Spirit..."]
    }
    return pd.DataFrame(data)

# 2. SESSION STATE MANAGEMENT
if "active_tab" not in st.session_state:
    st.session_state.active_tab = "Daily Walk"
if "current_day" not in st.session_state:
    st.session_state.current_day = 1
if "day_completed" not in st.session_state:
    st.session_state.day_completed = False

# 3. CSS FOR CUSTOM BUTTON COLORS
st.markdown("""
    <style>
    /* Complete Day - Light Green */
    div.stButton > button:first-child {
        background-color: #90EE90 !important;
        color: black !important;
    }
    /* Get Help - Light Red */
    div.stColumns > div:nth-child(2) button {
        background-color: #FFCCCB !important;
        color: black !important;
    }
    /* Peek Ahead - Light Blue */
    .stButton > button[key="peek_button"] {
        background-color: #ADD8E6 !important;
        color: black !important;
        margin-top: 20px;
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
    
    # Filter by Category AND Current Day
    day_data = df[(df["Category"] == category) & (df["Day"] == st.session_state.current_day)]
    
    if not day_data.empty:
        selected = day_data.iloc[0]

        # Scripture Card
        scripture_html = f"""<div style="background-color:#f8f9fa;padding:20px;border-radius:10px;border-left:5px solid #6c757d;margin-bottom:20px;">
            <i style="color:#333;">"{selected['Verse']}"</i><br><b style="color:#666;">— {selected['Scripture']}</b>
        </div>"""
        st.markdown(scripture_html, unsafe_allow_html=True)

        st.subheader(f"Day {st.session_state.current_day}: The Challenge")
        st.info(selected['Challenge'])

        with st.expander("📖 View Daily Devotion"):
            st.write(selected['Devotion'])

        journal_entry = st.text_area("Your Response to the Spirit", placeholder="Record your breakthrough...", key="journal_input")

        # ACTION BUTTONS
        col1, col2 = st.columns(2)
        with col1:
            if st.button("Complete Day", use_container_width=True):
                if journal_entry:
                    st.session_state.day_completed = True
                    st.success("Day Complete!")
                    st.balloons()
                    st.rerun()
                else:
                    st.warning("Please record your thoughts first.")

        with col2:
            if st.button("Get Help", use_container_width=True):
                if journal_entry:
                    st.session_state.saved_journal = journal_entry
                    st.session_state.active_tab = "🆘 Request Coaching"
                    st.rerun()
                else:
                    st.error("Please enter a response first.")

        # 5. PEEK ahead logic
        if st.session_state.day_completed:
            st.divider()
            if st.button("✨ Peek Ahead to Next Day", key="peek_button", use_container_width=True):
                st.session_state.current_day += 1
                st.session_state.day_completed = False  # Reset for the new day
                st.rerun()
    else:
        st.success("🎉 You've reached the end of the available content for this category!")
        if st.button("Restart Journey"):
            st.session_state.current_day = 1
            st.rerun()

elif active_tab == "🆘 Request Coaching":
    st.header("Connect with a Coach")
    saved_text = st.session_state.get("saved_journal", "No entry provided.")
    message_to_coach = st.text_area("Message to Coach", value=f"Context:\n{saved_text}\n\nHelp me with...")
    
    if st.button("Submit to Coach"):
        st.success("Sent!")
    if st.button("← Back"):
        st.session_state.active_tab = "Daily Walk"
        st.rerun()
