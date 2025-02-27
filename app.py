import streamlit as st
import datetime
import pickle
import os
import random

DATA_FILE = "ibadah_data.pkl"

def load_data():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "rb") as f:
            return pickle.load(f)
    return {}

def save_data(data):
    with open(DATA_FILE, "wb") as f:
        pickle.dump(data, f)


st.title("Growth Mindset Challenge")
st.title("Ibadah Tracker")
st.write("Track your daily Ibadah progress and stay connected to Allah! 🕌")

# User Name Input
if "user_name" not in st.session_state:
    st.session_state.user_name = ""

st.session_state.user_name = st.text_input("Enter Your Name:", value=st.session_state.user_name)

if st.session_state.user_name:
    st.write(f"Welcome, {st.session_state.user_name}! 🌟")
    
    ibadah_list = ["Fajr", "Dhuhr", "Asr", "Maghrib", "Isha", "Quran", "Dua", "Sadaqa"]
    today = datetime.datetime.now().strftime("%Y-%m-%d")
    
    # Load previous data
    data = load_data()
    if st.session_state.user_name not in data:
        data[st.session_state.user_name] = {}
    
    if today not in data[st.session_state.user_name]:
        data[st.session_state.user_name][today] = {ibadah: False for ibadah in ibadah_list}
    
    # User selects Ibadah completed today
    st.subheader("Mark Your Ibadah for Today ✅")
    completed_count = 0
    for ibadah in ibadah_list:
        checked = st.checkbox(ibadah, value=data[st.session_state.user_name][today][ibadah])
        data[st.session_state.user_name][today][ibadah] = checked
        if checked:
            completed_count += 1
    
    if all(data[st.session_state.user_name][today].values()):
        st.success("Allah-humma Barik..!")
    
    # Progress Bar
    progress = completed_count / len(ibadah_list)
    st.progress(progress)
    st.write(f"🌟 Progress: {completed_count} / {len(ibadah_list)} Ibadah completed")
    
    if st.button("📥 Save Progress"):
        save_data(data)
        st.success("✅ Your Ibadah data has been saved!")
    
    # Daily Good Deed Challenge
    st.subheader("🌟 Today's Good Deed Challenge")
    challenges = [
        "Feed a poor person 🍛",
        "Pray for someone 🤲",
        "Make someone smile 😃",
        "Recite 5 verses of the Holy Quran 📖",
        "Give someone a gift 🎁",
        "Do charity 🙌🏻",
        "Forgive someone 🙏",
        "Listen to someone 👂",
        "Share a Quranic verse with others 📖",
        "Help someone in need 🤝🏻",
    ]
    random_challenge = random.choice(challenges)
    st.write(random_challenge)
else:
    st.warning("Please enter your name to continue!")




st.write("Built By Rizwana Shiree ")