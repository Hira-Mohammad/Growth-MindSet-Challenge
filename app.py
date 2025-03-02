import streamlit as st
import datetime
import pickle
import os
import random
import pandas as pd
from datetime import timedelta

DATA_FILE = "ibadah_data.pkl"

def load_data():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "rb") as f:
            return pickle.load(f)
    return {}

def save_data(data):
    with open(DATA_FILE, "wb") as f:
        pickle.dump(data, f)


st.title("30-Day Ibadah Growth Challenge")
st.write("Track your daily Ibadah progress and build lasting habits! 🕌")

# User Name Input
if "user_name" not in st.session_state:
    st.session_state.user_name = ""

st.session_state.user_name = st.text_input("Enter Your Name:", value=st.session_state.user_name)

if st.session_state.user_name:
    st.write(f"Welcome, {st.session_state.user_name}! 🌟")
    
    ibadah_list = [
        "Fajr", "Dhuhr", "Asr", "Maghrib", "Isha",
        "Quran Reading", "Morning Adhkar", "Evening Adhkar",
        "Tahajjud", "Duha Prayer", "Sadaqa", "Good Deed"
    ]
    
    # Date selection
    today = datetime.datetime.now().date()
    selected_date = st.date_input(
        "Select Date",
        value=today,
        min_value=today - timedelta(days=30),
        max_value=today
    )
    
    # Load previous data
    data = load_data()
    if st.session_state.user_name not in data:
        data[st.session_state.user_name] = {}
    
    selected_date_str = selected_date.strftime("%Y-%m-%d")
    if selected_date_str not in data[st.session_state.user_name]:
        data[st.session_state.user_name][selected_date_str] = {ibadah: False for ibadah in ibadah_list}
    
    # Create tabs for different views
    tab1, tab2, tab3 = st.tabs(["Daily Tracking", "30-Day Overview", "Statistics"])
    
    with tab1:
        st.subheader("Mark Your Ibadah ✅")
        completed_count = 0
        
        # Group ibadah into categories
        col1, col2 = st.columns(2)
        
        with col1:
            st.write("📿 Obligatory Prayers")
            for ibadah in ibadah_list[:5]:  # First 5 are prayers
                checked = st.checkbox(ibadah, value=data[st.session_state.user_name][selected_date_str][ibadah])
                data[st.session_state.user_name][selected_date_str][ibadah] = checked
                if checked:
                    completed_count += 1
        
        with col2:
            st.write("🌟 Additional Acts")
            for ibadah in ibadah_list[5:]:  # Remaining acts
                checked = st.checkbox(ibadah, value=data[st.session_state.user_name][selected_date_str][ibadah])
                data[st.session_state.user_name][selected_date_str][ibadah] = checked
                if checked:
                    completed_count += 1
        
        # Progress indicators
        progress = completed_count / len(ibadah_list)
        st.progress(progress)
        st.write(f"🌟 Today's Progress: {completed_count} / {len(ibadah_list)} Ibadah completed")
        
        if st.button("📥 Save Progress"):
            save_data(data)
            
            # Appreciation messages based on completion
            appreciation_messages = [
                "MashaAllah! Your dedication to ibadah is inspiring! 🌟",
                "SubhanAllah! Every act of worship brings you closer to Allah! ✨",
                "Alhamdulillah! Keep striving for excellence in your worship! 🌙",
                "Remember, Allah sees your efforts and dedication! 💫",
                "Your consistency in worship is beautiful to witness! 🤲",
                "May Allah accept your ibadah and increase you in good! 📿",
                "Keep going! Every small act of worship counts with Allah! ⭐",
                "Your dedication to spiritual growth is admirable! 🌺"
            ]
            
            st.success("✅ Your Ibadah data has been saved!")
            st.write(random.choice(appreciation_messages))
        
        # Daily Good Deed Challenge
        st.markdown("---")
        st.subheader("🌟 Today's Special Connection Challenge")
        
        challenges = [
            "Read the meaning of one new verse from the Quran 📖",
            "Call a family member you haven't spoken to in a while 📞",
            "Share a meal with someone in need 🍲",
            "Smile at 3 people today - it's Sunnah! 😊",
            "Learn a new name of Allah and its meaning ✨",
            "Give water to someone who is thirsty 💧",
            "Help your parents with household chores 🏠",
            "Visit a sick person 🤲",
            "Share beneficial Islamic knowledge with someone 📚",
            "Make dua for 3 people without them knowing 💝",
            "Clean your local masjid or prayer area 🕌",
            "Plant a tree or take care of a plant 🌱",
            "Give sincere compliments to 3 people today ❤️",
            "Donate clothes or books you no longer need 📦",
            "Make istighfar 100 times today 📿",
            "Help someone learn a new surah 🎯",
            "Feed a stray animal 🐱",
            "Write a letter of gratitude to someone 💌",
            "Memorize a new dua and teach it to someone else 📝",
            "Remove something harmful from the path 🛣️"
        ]
        
        # Generate a random challenge but keep it consistent for the same day
        today_seed = datetime.datetime.now().strftime("%Y-%m-%d")
        random.seed(today_seed)
        daily_challenge = random.choice(challenges)
        random.seed()  # Reset the seed
        
        st.write("Connect with Allah through this special deed:")
        st.info(daily_challenge)
        
        # Add motivational reminder
        st.markdown("---")
        st.write("Remember: 💫")
        reminders = [
            "Every small deed done consistently is beloved to Allah.",
            "Your relationship with Allah is the most important relationship to nurture.",
            "Today's efforts are tomorrow's rewards.",
            "Allah sees your struggles and efforts.",
            "Small steps lead to big changes."
        ]
        st.write(random.choice(reminders))
    
    with tab2:
        st.subheader("30-Day Overview")
        
        # Create 30-day overview
        dates = [(today - timedelta(days=x)).strftime("%Y-%m-%d") for x in range(30)]
        overview_data = []
        
        for date in dates:
            if date in data[st.session_state.user_name]:
                day_data = data[st.session_state.user_name][date]
                completion_rate = sum(day_data.values()) / len(ibadah_list) * 100
                overview_data.append({
                    "Date": date,
                    "Completion Rate": f"{completion_rate:.1f}%",
                    "Completed Acts": sum(day_data.values())
                })
        
        if overview_data:
            df = pd.DataFrame(overview_data)
            st.dataframe(df, hide_index=True)
            
            # Visualization
            st.line_chart(df.set_index("Date")["Completed Acts"])
    
    with tab3:
        st.subheader("Your Statistics")
        
        if data[st.session_state.user_name]:
            total_days = len(data[st.session_state.user_name])
            perfect_days = sum(1 for day in data[st.session_state.user_name].values() 
                             if all(day.values()))
            
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Days Tracked", total_days)
            with col2:
                st.metric("Perfect Days", perfect_days)
            with col3:
                avg_completion = sum(sum(day.values()) for day in data[st.session_state.user_name].values()) / (total_days * len(ibadah_list)) * 100
                st.metric("Average Completion", f"{avg_completion:.1f}%")
            
            # Most consistent ibadah
            ibadah_completion = {ibadah: 0 for ibadah in ibadah_list}
            for day in data[st.session_state.user_name].values():
                for ibadah, completed in day.items():
                    if completed:
                        ibadah_completion[ibadah] += 1
            
            most_consistent = max(ibadah_completion.items(), key=lambda x: x[1])
            st.write(f"🏆 Most Consistent Ibadah: **{most_consistent[0]}** ({most_consistent[1]} days)")

else:
    st.warning("Please enter your name to continue!")

# Footer
st.markdown("---")
st.write("Built By ❤️ Shiree..")