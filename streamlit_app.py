import streamlit as st
import pandas as pd
import random

# --- 1. FULL 30-ROW ETL DATA ---
def load_data():
    data = {
        "Category": ["Anxiety"]*10 + ["Purpose"]*10 + ["Leadership"]*10,
        "Day": [1,2,3,4,5,6,7,8,9,10] * 3,
        "Scripture": [
            # Anxiety
            "Phil 4:6-7", "1 Pet 5:7", "Matt 6:34", "Isa 41:10", "Ps 56:3", 
            "John 14:27", "2 Tim 1:7", "Ps 94:19", "Matt 11:28", "Josh 1:9",
            # Purpose
            "Eph 2:10", "Jer 29:11", "Rom 12:2", "Ps 139:14", "Prov 3:5-6",
            "Prov 19:21", "1 Pet 4:10", "Col 3:23", "Ps 138:8", "Rom 8:28",
            # Leadership
            "Mark 10:45", "Prov 4:23", "Exod 18:21", "1 Tim 3:2", "Ps 78:72",
            "Phil 2:3", "Prov 11:14", "Gal 6:9", "1 Tim 4:12", "Heb 13:17"
        ],
        "Verse": [
            # Anxiety
            "Do not be anxious...", "Cast your anxiety...", "Do not worry...", "So do not fear...", "When I am afraid...",
            "Peace I leave with you.", "Not a spirit of fear...", "When anxiety was great...", "I will give you rest.", "Be strong...",
            # Purpose
            "For we are God's...", "Plans to prosper...", "Be transformed...", "Fearfully made...", "Trust in the Lord...",
            "Many are the plans...", "Use your gifts...", "Work with all heart...", "Lord will fulfill...", "All things work...",
            # Leadership
            "Came to serve...", "Guard your heart...", "Select capable men...", "Above reproach...", "Skilful hands...",
            "Nothing from rivalry...", "Lack of guidance...", "Not be weary...", "Be an example...", "Have confidence..."
        ],
        "Challenge": [
            # Anxiety
            "What are you controlling?", "What is your heavy burden?", "What future fear is here?", "Where do you feel weak?", "What is your current fear?",
            "Is your heart troubled?", "Where is fear acting?", "Is your mind racing?", "Are you weary?", "Where do you need courage?",
            # Purpose
            "What gift is hidden?", "Do you fear the future?", "Where are you conforming?", "Do you doubt your value?", "Are you leaning on self?",
            "Are you forcing a door?", "What gift ignoring?", "Working for men?", "Do you feel behind?", "Can you see the 'Good'?",
            # Leadership
            "Who are you serving?", "What is leaking in?", "Are you delegating?", "Is character solid?", "Growing skill?",
            "Is ego driving you?", "Leading alone?", "Ready to quit?", "Feel 'too young'?", "Are you leadable?"
        ],
        "Devotion": [
            # Anxiety
            "Surrender is peace.", "He cares for you.", "Today is enough.", "I will uphold you.", "Trust is a choice.",
            "Not as world gives.", "Power and love.", "His joy consoles.", "My yoke is easy.", "The Lord is with you.",
            # Purpose
            "Designed with intent.", "Plans are for good.", "Requires new mind.", "Not a mistake.", "Straight paths.",
            "Purpose outlasts plans.", "Grace is a gift.", "Act of worship.", "He perfects you.", "Detours have purpose.",
            # Leadership
            "Inverted power.", "Private life is power.", "Don't go alone.", "Character is a shield.", "Integrity + Skill.",
            "Humility is power.", "Wisdom in counsel.", "Due season reaping.", "Lead by example.", "Starts with hearing."
        ],
        "Spirit_Prompt": [
            # Anxiety
            "What can I let go?", "Will You take this?", "Help me stay in today.", "Be my strength.", "I trust You.",
            "I receive Your peace.", "Give me sound mind.", "Bring joy to my soul.", "Teach me to rest.", "Thank You for being here.",
            # Purpose
            "How can I bless?", "Show me next step.", "Renew my thoughts.", "Help me see worth.", "I trust Your direction.",
            "Surrender timeline.", "How can I serve?", "Do this for Him.", "Trust finishing work.", "Thank Him for process.",
            # Leadership
            "Who can I advocate?", "Cleanse my heart.", "Who can I empower?", "Help me walk in truth.", "What should I learn?",
            "Who can I lift up?", "Who should I ask?", "Second-wind grace.", "Set the pace.", "How can I follow?"
        ]
    }
    return pd.DataFrame(data)

# --- 2. SESSION STATE ---
if "current_day" not in st.session_state: st.session_state.current_day = 1
if "day_completed" not in st.session_state: st.session_state.day_completed = False
if "streak" not in st.session_state: st.session_state.streak = 0
if "badges" not in st.session_state: st.session_state.badges = []
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
    button[key^="tester"] { background-color: #34495E !important; color: #FFFFFF !important; border: 1px solid #2C3E50 !important; font-weight: 600 !important; }
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
if st.sidebar.button("🚀 Fast-Track Day 9", key="tester_9", use_container_width=True):
    st.session_state.current_day = 9
    st.session_state.streak = 9
    st.rerun()
if st.sidebar.button("🚨 Reset App", key="tester_reset", use_container_width=True):
    st.session_state.update({"current_day": 1, "streak": 0, "day_completed": False, "badges": []})
    st.rerun()

# --- 5. MAIN LOGIC ---
if nav_choice == "Daily Walk":
    # 10-Day Progress Bar
    progress = st.session_state.current_day / 10
    st.progress(progress)
    st.caption(f"Journey Progress: Day {st.session_state.current_day} of 10")

    st.markdown(f"<div class='streak-box'>🔥 SPIRIT STREAK: {st.session_state.streak} DAYS</div>", unsafe_allow_html=True)
    
    category = st.selectbox("Focus Track:", df["Category"].unique())
    day_data = df[(df["Category"] == category) & (df["Day"] == st.session_state.current_day)]
    
    if not day_data.empty:
        row = day_data.iloc[0]
        script_style = "background-color:#FDFDFD;padding:15px;border-radius:10px;border:1px solid #DDD;border-left:5px solid #34495E;margin-bottom:15px;"
        st.markdown(f'<div style="{script_style}"><p style="font-style:italic;color:#222;">"{row["Verse"]}"</p><b>— {row["Scripture"]}</b></div>', unsafe_allow_html=True)

        st.subheader(f"Day {st.session_state.current_day}")
        st.info(f"**Challenge:** {row['Challenge']}")
        
        with st.expander("📖 Daily Devotion & Guidance", expanded=True):
            st.write(row['Devotion'])
            st.markdown(f"**🕊️ Spirit Guidance Prompt:** *{row['Spirit_Prompt']}*")

        journal_entry = st.text_area("Your Response", key="journal_input", placeholder="Record your breakthrough...")

        c1, c2 = st.columns(2)
        with c1:
            if st.button("Complete Day", key="complete_btn", use_container_width=True):
                if journal_entry:
                    st.balloons()
                    st.snow()
                    st.session_state.day_completed = True
                    st.session_state.streak += 1
                    
                    # Milestone Badges
                    if st.session_state.current_day == 1 and "First Step" not in st.session_state.badges:
                        st.session_state.badges.append("First Step")
                    elif st.session_state.current_day == 10 and "Track Overcomer" not in st.session_state.badges:
                        st.session_state.badges.append("Track Overcomer")
                    
                    st.success("Day Completed!")
                    st.rerun()
                else:
                    st.warning("Please record a response.")
        
        with c2:
            if st.button("Get Help", key="help_btn", use_container_width=True):
                st.session_state.saved_journal = journal_entry
                st.info("Switch to Coaching tab to send.")

        if st.session_state.day_completed:
            st.divider()
            if st.session_state.current_day < 10:
                if st.button("✨ Step Into Next Day", type="primary", use_container_width=True):
                    st.session_state.current_day += 1
                    st.session_state.day_completed = False
                    st.rerun()
            else:
                st.success("🎉 You've finished the 10-day journey!")

else:
    st.header("Connect with a Coach")
    st.text_area("Context", value=st.session_state.get("saved_journal", ""), height=150)
    if st.button("Submit to Coach"): st.success("Sent!")
