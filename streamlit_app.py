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

# 3. CSS FOR CUSTOM BUTTON COLORS (Cleaned and Fixed)
st.markdown("""
    <style>
    /* Complete Day - Light Green */
    button[kind="secondary"]:nth-of-type(1) {
        background-color: #90EE90 !important;
        color: black !important;
    }
    /* Get Help - Light Red */
    button[kind="secondary"]:nth-of-type(2) {
        background-color: #FFCCCB !important;
        color: black !important;
    }
    </style>
""", unsafe_allow_html=True)

# 4. NAVIGATION
df = load_data()
tabs = ["Daily Walk", "🆘 Request Coaching"]
# Sidebar navigation is more stable for state switching
active_tab = st.sidebar.radio("Navigation", tabs, index=tabs.index(st.session_state.active_tab))

if active_tab == "Daily Walk":
    st.title("🕊️ SpiritWalk")
    category = st.selectbox("Select Your Focus:", df["Category"].unique())
    selected = df[df["Category"] == category].iloc[0]

    # Scripture Card (String block fixed)
    scripture_html = f"""<div style="background-color:#f8f9fa;padding:20px;border-radius:10px;border-left:5px solid #6c757d;margin-bottom:20px;">
        <i style="color:#333;">"{selected['Verse']}"</i><br><b style="color:#666;">— {selected['Scripture']}</b>
    </div>"""
    st.markdown(scripture_html, unsafe_allow_html=True)

    st.subheader("Today's Challenge")
    st.info(selected['Challenge'])

    with st.expander("📖 View Daily Devotion"):
        st.write(selected['Devotion'])

    journal_entry = st.text_area("Your Response to the Spirit", placeholder="Record your breakthrough...", key="journal_input")

    # BUTTONS
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("Complete Day", use_container_width=True):
            if journal_entry:
                st.success("Entry Saved!")
                st.balloons()
            else:
                st.warning("Please record your thoughts.")

    with col2:
        if st.button("Get Help", use_container_width=True):
            if journal_entry:
                st.session_state.saved_journal = journal_entry
                st.session_state.active_tab = "🆘 Request Coaching"
                st.rerun()
            else:
                st.error("Please enter a response first so the coach has context.")

elif active_tab == "🆘 Request Coaching":
    st.header("Connect with a Coach")
    saved_text = st.session_state.get("saved_journal", "No journal entry provided.")
    
    message_to_coach = st.text_area("Message to Coach", 
                                    value=f"Context from my session:\n{saved_text}\n\nCoach, I need help with...")

    if st.button("Submit to Coach", use_container_width=True):
        st.success("Your coach has been notified!")
    
    if st.button("← Back to Walk", use_container_width=True):
        st.session_state.active_tab = "Daily Walk"
        st.rerun()
