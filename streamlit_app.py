import streamlit as st
import pandas as pd

# 1. ETL DATA LOAD
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
            "Identify one gift you have been hiding.",
            "Who is the person you find hardest to extend grace to?"
        ],
        "Devotion": ["Content here...", "Content here...", "Content here..."],
        "Spirit_Prompt": ["Ask the Spirit...", "Ask the Spirit...", "Ask the Spirit..."]
    }
    return pd.DataFrame(data)

# 2. UI SETUP
st.set_page_config(page_title="SpiritWalk Beta", page_icon="🕊️")
df = load_data()

# Sidebar Progress
st.sidebar.title("📈 Your Journey")
progress = st.sidebar.slider("Challenge Progress", 0, 30, 1)
st.sidebar.progress(progress / 30)

# 3. TABS FOR CLEAN NAVIGATION
tab1, tab2 = st.tabs(["Daily Walk", "🆘 Request Coaching"])

with tab1:
    st.title("🕊️ SpiritWalk")
    category = st.selectbox("Select Your Focus:", df["Category"].unique())
    selected = df[df["Category"] == category].iloc[0]

    # Scripture Card
    st.markdown(f"""<div style="background-color:#f8f9fa;padding:20px;border-radius:10px;border-left:5px solid #6c757d;">
        <i>"{selected['Verse']}"</i><br><b>— {selected['Scripture']}</b></div>""", unsafe_allow_html=True)

    st.subheader(f"Day {progress}: The Challenge")
    st.info(selected['Challenge'])

    journal_entry = st.text_area("Your Response to the Spirit", placeholder="Record your breakthrough...")

    if st.button("Complete Day"):
        st.success("Entry Saved!")
        st.balloons()

with tab2:
    st.header("Connect with a Coach")
    st.write("Feeling stuck? Send your current journal entry to a SpiritWalk coach for guidance.")
    
    coach_topic = st.selectbox("What do you need help with?", ["Understanding the Scripture", "Hearing the Spirit", "Personal Application", "Other"])
    message_to_coach = st.text_area("Message to Coach", value=f"Hi Coach, I'm working on the '{category}' track (Day {progress}). I'm struggling with: \n\n{journal_entry}")

    if st.button("Send to Coach"):
        if journal_entry and message_to_coach:
            # SIMULATION: In a real app, this would use an API like SendGrid or Twilio
            st.success(f"Message sent! A coach will review your Day {progress} entry and reach out via email.")
            st.toast("Message Transmitted", icon="📤")
        else:
            st.error("Please ensure your journal entry isn't empty before requesting help.")
