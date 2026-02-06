import streamlit as st
import pandas as pd
import random

# --- 1. DATA LOAD (ETL SIMULATION) ---
def load_data():
    data = {
        "Category": ["Anxiety"] * 5 + ["Purpose"] * 5,
        "Day": [1, 2, 3, 4, 5] * 2,
        "Scripture": ["Phil 4:6", "John 14:27", "Matt 11:28", "Psalm 23:1", "Isa 41:10"] * 2,
        "Verse": ["Do not be anxious...", "My peace I give...", "Come to me...", "The Lord is my shepherd...", "I will help you..."] * 2,
        "Challenge": ["Control", "Fear vs Peace", "Rest", "Guidance", "Final Strength"] * 2,
        "Devotion": ["Surrender is the bridge to peace.", "Peace is a person, not a feeling.", "His yoke is easy and light.", "He leads us beside quiet waters.", "His strength is perfect in weakness."] * 2,
        "Spirit_Prompt": ["What can I let go of today?", "Where do I need Your peace?", "How can I rest in You?", "Where are You leading me?", "Help me stand in Your strength."] * 2
    }
    return pd.DataFrame(data)

# --- 2. SESSION STATE ---
# Initialize all necessary states to prevent 'KeyError'
if "current_day" not in st.session_state: st.session_state.current_day = 1
if "day_completed" not in st.session_state: st.session_state.day_completed = False
if "streak" not in st.session_state: st.session_state.streak = 0
if "badges" not in st.session_state: st.session_state.badges = []
if "missed_days" not in st.session_state: st.session_state.missed_days = 0
if "active_tab" not in st.session_state: st.session_state.active_tab = "Daily Walk"

# --- 3. UI STYLING ---
st.markdown("""
    <style>
    .badge-card { background-color: #fff; padding: 10px; border-radius: 8px; border: 1px solid #e0e0e0; margin-bottom: 5px; text-align: center; font-weight: bold; color: #000; }
    
    .streak-box { 
        background-color: #FFF9C4; 
        padding: 10px; 
        border-radius: 10px; 
        text-align: center; 
        font-weight: 800; 
        border: 1px solid #FBC02D; 
        margin-bottom: 20px;
        color: #000000 !important;
    }
    
    button[key="complete_btn"] { background-color: #2ECC71 !important; color: white !important; font-weight: bold !important; border-radius: 20px !important; }
    button[key="help_btn"] { background-color: #E74C3C !important; color: white !important; font-weight: bold !important; border-radius: 20px !important; }
    
    button[key^="tester"] {
        background-color: #34495E !important; 
        color: #FFFFFF !important; 
        border: 1px solid #2C3E50 !important;
        font-weight: 600 !important;
    }
    </style>
""", unsafe_allow_html=True)

# --- 4. SIDEBAR ---
df = load_data()
st.sidebar.title("🕊️ SpiritWalk")
nav_choice = st.sidebar.radio("Navigation", ["Daily Walk", "🆘 Request Coaching"])

st.sidebar.divider()
st.sidebar.subheader("🏆 Achievement Case")
for b in st.session_state.badges:
    st.sidebar.markdown(f"<div class='badge-card'>🏅 {b}</div>", unsafe_allow_html=True)

st.sidebar.divider()
st.sidebar.subheader("🛠️ Admin Tools")
if st.sidebar.button("🚀 Fast-Track Day 3", key="tester_3", use_container_width=True):
    st.session_state.current_day = 3
    st.session_state.streak = 3
    if "Trinity Walker" not in st.session_state.badges: st.session_state.badges.append("Trinity Walker")
    st.rerun()
if st.sidebar.button("🚨 Reset App", key="tester_reset", use_container_width=True):
    st.session_state.update({"current_day": 1, "streak": 0, "missed_days": 0, "day_completed": False, "badges": []})
    st.rerun()

# --- 5. MAIN LOGIC ---
if nav_choice == "Daily Walk":
    st.markdown(f"<div class='streak-box'>🔥 SPIRIT STREAK: {st.session_state.streak} DAYS</div>", unsafe_allow_html=True)
    
    category = st.selectbox("Focus Track:", df["Category"].unique())
    day_data = df[(df["Category"] == category) & (df["Day"] == st.session_state.current_day)]
    
    if not day_data.empty:
        row = day_data.iloc[0]
        script_style = "background-color:#FDFDFD;padding:15px;border-radius:10px;border:1px solid #DDD;border-left:5px solid #34495E;margin-bottom:15px;"
        st.markdown(f'<div style="{script_style}"><p style="font-style:italic;color:#222;">"{row["Verse"]}"</p><b>— {row["Scripture"]}</b></div>', unsafe_allow_html=True)

        st.subheader(f"Day {st.session_state.current_day}")
        st.info(f"**Today's Challenge:** {row['Challenge']}")
        
        # FIXED: Devotion expanded by default
        with st.expander("📖 Daily Devotion & Guidance", expanded=True):
            st.write(row['Devotion'])
            st.markdown(f"**🕊️ Spirit Guidance Prompt:** *{row['Spirit_Prompt']}*")

        journal_entry = st.text_area("Your Response", key="journal_input", placeholder="Record your breakthrough...")

        c1, c2 = st.columns(2)
        with c1:
            if st.button("Complete Day", key="complete_btn", use_container_width=True):
                if journal_entry:
                    st.session_state.day_completed = True
                    st.session_state.streak += 1
                    
                    # Milestone Celebrations
                    new_badge = None
                    if st.session_state.current_day == 1: new_badge = "First Step"
                    elif st.session_state.current_day == 3: new_badge = "Trinity Walker"
                    elif st.session_state.current_day == 5: new_badge = "Track Overcomer"
                    
                    if new_badge and new_badge not in st.session_state.badges:
                        st.session_state.badges.append(new_badge)
                        st.snow()
                    
                    st.balloons()
                    st.rerun()
                else:
                    st.warning("Please record a response.")
        
        with c2:
            if st.button("Get Help", key="help_btn", use_container_width=True):
                st.session_state.saved_journal = journal_entry
                st.info("Head to the Coaching tab to send.")

        if st.session_state.day_completed:
            st.divider()
            if st.session_state.current_day < 5:
                if st.button("✨ Step Into Next Day", type="primary", use_container_width=True):
                    st.session_state.current_day += 1
                    st.session_state.day_completed = False
                    st.rerun()
            else:
                st.success("🎉 Track Complete!")

else:
    st.header("Connect with a Coach")
    st.text_area("Your Context", value=st.session_state.get("saved_journal", ""), height=150)
    if st.button("Submit to Coach"): st.success("Message Sent!")
