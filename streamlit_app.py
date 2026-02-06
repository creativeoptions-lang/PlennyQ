import streamlit as st
import pandas as pd

# 1. THE DATA (ETL)
def load_data():
    data = {
        "Category": ["Anxiety", "Purpose", "Relationships"],
        "Day": [1, 1, 1],
        "Scripture": ["Philippians 4:6-7", "Ephesians 2:10", "1 Peter 4:8"],
        "Verse": [
            "Do not be anxious about anything, but in every situation, by prayer and petition, with thanksgiving, present your requests to God.",
            "For we are God’s handiwork, created in Christ Jesus to do good works.",
            "Above all, love each other deeply, because love covers over a multitude of sins."
        ],
        "Challenge": [
            "What is the one thing you are trying to control today that isn't yours to carry?",
            "Identify one gift you have that you've been hiding out of fear.",
            "Who is the person you find hardest to extend grace to right now?"
        ],
        "Devotion": [
            "Surrender isn't giving up; it's getting free. When we release our grip, we make room for God's peace.",
            "You aren't a mistake. You are an intentional creation designed for a specific impact.",
            "Grace isn't earned by the receiver; it's given by the overflow of the Giver."
        ],
        "Spirit_Prompt": [
            "Ask the Holy Spirit: 'What do You want me to let go of?'",
            "Ask the Spirit: 'How can I use my unique voice to bless someone today?'",
            "Ask the Spirit: 'Help me see this person through Your eyes. What do You see?'"
        ]
    }
    return pd.DataFrame(data)

# 2. UI CONFIG
st.set_page_config(page_title="SpiritWalk Beta", page_icon="🕊️")
df = load_data()

# Sidebar
st.sidebar.title("📈 Your Journey")
progress = st.sidebar.slider("Challenge Progress", 0, 30, 1)
st.sidebar.progress(progress / 30)

# 3. CONTENT SELECTION
st.title("🕊️ SpiritWalk")
category = st.selectbox("Select Your Focus:", df["Category"].unique())
selected = df[df["Category"] == category].iloc[0]

# Scripture Card
st.markdown(
    f"""
    <div style="background-color: #f8f9fa; padding: 20px; border-radius: 10px; border-left: 5px solid #6c757d; margin-bottom: 20px;">
        <p style="font-style: italic; font-size: 1.1em; color: #343a40;">"{selected['Verse']}"</p>
        <b style="color: #6c757d;">— {selected['Scripture']}</b>
    </div>
    """, 
    unsafe_allow_html=True
)

# 4. MAIN FLOW
st.subheader(f"Day {progress}: The Challenge")
st.info(selected['Challenge'])

with st.expander("📖 Read Daily Devotion"):
    st.write(selected['Devotion'])

st.subheader("🔥 Holy Spirit Guidance")
st.write(f"**Prompt:** {selected['Spirit_Prompt']}")

journal_entry = st.text_area("Your Response", placeholder="Record your breakthrough...")

# 5. SHARE & FINISH
if st.button("Complete Today's Walk"):
    if journal_entry:
        st.success("Entry Saved!")
        st.balloons()
        
        # Prepare Shareable Text
        share_text = f"🕊️ SpiritWalk Day {progress}\n\nChallenge: {selected['Challenge']}\n\nMy Breakthrough: {journal_entry}\n\nScripture: {selected['Scripture']}"
        
        st.divider()
        st.subheader("📣 Share Your Breakthrough")
        st.code(share_text, language=None)
        st.caption("Copy the text above to share with your small group or a friend!")
    else:
        st.warning("Please record your thoughts to complete the day.")
