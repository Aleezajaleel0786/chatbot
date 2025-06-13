import streamlit as st
import pyttsx3
import speech_recognition as sr
import os
import webbrowser
import datetime
import time
import threading

# ----------------------- Load Training Data -----------------------
def load_training_data():
    responses = {}
    if os.path.exists("training_data.txt"):
        with open("training_data.txt", "r", encoding='utf-8') as file:
            for line in file:
                if ":" in line:
                    question, answer = line.strip().split(":", 1)
                    responses[question.lower()] = answer
    return responses

# ----------------------- Alarm Feature -----------------------
def set_alarm(alarm_time_str):
    try:
        alarm_time = datetime.datetime.strptime(alarm_time_str, "%H:%M")
        now = datetime.datetime.now()
        alarm_today = now.replace(hour=alarm_time.hour, minute=alarm_time.minute, second=0, microsecond=0)

        if alarm_today < now:
            alarm_today += datetime.timedelta(days=1)

        seconds_left = (alarm_today - now).total_seconds()

        def alarm_thread():
            time.sleep(seconds_left)
            speak("⏰ Alarm! Wake up!")
            st.warning("⏰ Alarm! Wake up!")

        threading.Thread(target=alarm_thread).start()
        return f"Alarm set for {alarm_time.strftime('%I:%M %p')}."

    except ValueError:
        return "Please enter time in HH:MM format (e.g., 07:30)."

# ----------------------- App Open Feature -----------------------
def open_app(app_name):
    if "chrome" in app_name:
        os.system("start chrome")
        return "Opening Chrome..."
    elif "notepad" in app_name:
        os.system("start notepad")
        return "Opening Notepad..."
    elif "calculator" in app_name or "calc" in app_name:
        os.system("start calc")
        return "Opening calculator..."
    elif "youtube" in app_name:
        webbrowser.open("https://www.youtube.com")
        return "Opening YouTube..."
    elif "tiktok" in app_name:
        webbrowser.open("https://www.tiktok.com")
        return "Opening TikTok..."
    elif "instagram" in app_name or "insta" in app_name:
        webbrowser.open("https://www.instagram.com")
        return "Opening Instagram..."
    else:
        return "App not recognized. Try: chrome, notepad, calculator, YouTube, TikTok, Instagram."

# ----------------------- Get Bot Response -----------------------
def get_response(user_input, responses):
    user_input = user_input.lower()

    # Alarm
    if "alarm" in user_input or "set alarm" in user_input or "الارم" in user_input:
        for word in user_input.split():
            if ":" in word:
                return set_alarm(word)
        return "Please tell the time like 'set alarm 07:30'."

    # Open app
    if "open" in user_input or "کھولو" in user_input:
        app_name = user_input.replace("open", "").replace("کھولو", "").strip()
        return open_app(app_name)

    # Training data
    for question in responses:
        if question in user_input:
            return responses[question]

    return "Sorry, I don't understand that."

# ----------------------- TTS -----------------------
def speak(text):
    def _speak():
        engine = pyttsx3.init()
        engine.say(text)
        engine.runAndWait()
    threading.Thread(target=_speak).start()


# ----------------------- Speech Recognition -----------------------
def recognize_speech():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        st.info("Listening... Speak now!")
        audio = recognizer.listen(source)
    try:
        text = recognizer.recognize_google(audio)
        return text
    except sr.UnknownValueError:
        return "Sorry, I couldn't understand."
    except sr.RequestError:
        return "Sorry, network error."

# ----------------------- Streamlit UI -----------------------
st.set_page_config(page_title="AI Chatbot", page_icon="🧠")
st.title("AI Chatbot🤖")

st.markdown("""
Type or speak your message below. This chatbot works offline, gives voice replies, opens apps, and even sets alarms!
""")

responses = load_training_data()

# Voice Input
if st.button("🎤 Speak"):
    user_query = recognize_speech()
    st.write(f"You said: {user_query}")
    bot_reply = get_response(user_query, responses)
    st.success(f"Bot: {bot_reply}")
    speak(bot_reply)

# Text Input
text_input = st.text_input("💬 Or type your message here:")
if st.button("Send") and text_input:
    bot_reply = get_response(text_input, responses)
    st.success(f"Bot: {bot_reply}")
    speak(bot_reply)