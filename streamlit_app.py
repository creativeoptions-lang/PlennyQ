import streamlit as st
import pandas as pd

# 1. ETL DATA LOAD (Fixed logic for Devotion display)
def load_data():
    data = {
        "Category": ["Anxiety", "Purpose", "Relationships"],
        "Day": [1, 1, 1],
        "Scripture": ["Philippians 4:6-7", "Ephesians 2:10", "1 Peter 4:8"],
        "Verse": [
            "Do not be anxious about anything, but in every situation...",
            "For we are God’s handiwork, created in Christ Jesus...",
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
        "Spirit_Prompt": [
            "Ask the Spirit: 'What do You want me to let go of?'",
            "Ask the Spirit: 'How can I use my gift to bless someone?'",
            "Ask the Spirit: 'Help me see this person through Your eyes.'"
        ]
    }
    return pd.DataFrame(data)

# 2. STATE MANAGEMENT (For switching tabs)
if "active_tab" not in st.session_state:
    st.session_state.active_tab = "Daily Walk"

# 3. UI SETUP
st.set_page_config(page_title="SpiritWalk Beta", page_icon="🕊️")
df = load_data()

# Tabs logic with session state
tabs = ["Daily Walk", "🆘 Request Coaching"]
active_tab = st.sidebar.radio("Navigation", tabs, index=tabs.index(st.session_state.active_tab))

if active_tab == "Daily Walk":
    st.title("🕊️ SpiritWalk")
    category = st.selectbox("Select Your Focus:", df["Category"].unique())
    
    # Correctly filtering the row based on category selection
    selected = df[df["Category"] == category].iloc[0]

    # Scripture Card
    st.markdown(f"""<div style="background-color:#f8f9fa;padding:20px;border-radius:10px;border-left:5px solid #6c757d;">
        <i>"{selected['Verse']}"</i><br><b>— {selected['Scripture']}</b></div>""", unsafe_allow_html=True)

    st.subheader(f"Today's Challenge")
    st.info(selected['Challenge'])

    # FIXED: Devotion now explicitly displays for the selected focus
    with st.expander("📖 View Daily Devotion"):
        st.write(selected['Devotion'])

    journal_entry = st.text_area("Your Response to the Spirit", placeholder="Record your breakthrough...", key="journal_input")

    # 4. BUTTON ROW
    col1, col2, _ = st.columns([1, 1, 2])
    
    with col1:
        if st.button("Complete Day"):
            if journal_entry:
                st.success("Entry Saved!")
                st.balloons()
            else:
                st.warning("Please record your thoughts.")

    with col2:
        # Custom styled button for "Get Help"
        if st.button("Get Help"):
            if journal_entry:
                st.session_state.saved_journal = journal_entry
                st.session_state.active_tab = "🆘 Request Coaching"
                st.rerun() # Forces the app to switch tabs immediately
            else:
                st.error("Please fill in your response before requesting help so the coach has context.")

    # Custom CSS for the Pink Button
    st.markdown("""
        <style>
        div.stButton > button:first-child[kind="secondary"] {
            background-color: #ffd1dc;
            border: none;
        }
        </style>
    """, unsafe_allow_html=True)

elif active_tab == "🆘 Request Coaching":
    st.header("Connect with a Coach")
    st.write("Your current progress and journal entry have been attached for the coach.")
    
    # Retrieve saved journal from session state
    saved_text = st.session_state.get("saved_journal", "")
    
    message_to_coach = st.text_area("Message to Coach", 
                                    value=f"Journal Entry: {saved_text}\n\nI need help with...")

    if st.button("Submit Request"):
        st.success("Your coach has been notified!")
