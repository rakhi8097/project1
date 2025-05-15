from dotenv import load_dotenv
load_dotenv()

import streamlit as st
import os
import google.generativeai as genai

# Configure the Gemini model
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))  # Store your key as an env var, not directly in code
model = genai.GenerativeModel("gemini-2.0-flash-lite")  # Use a valid model name
chat = model.start_chat(history=[])

# Function to get Gemini's career guidance response
def get_gemini_response(user_input):
    career_prompt = f"""
    You are a helpful career guidance assistant. Your job is to help users:
    - Explore suitable career paths based on their background, skills, and interests.
    - Assess their strengths and areas to improve.
    - Recommend learning resources (courses, websites, books, tools) based on their goals.

    Respond to the following user input accordingly:
    {user_input}
    """
    response = chat.send_message(career_prompt, stream=True)
    return response

# Set up page
st.set_page_config(page_title="Career Path Finder", page_icon="🔍", layout="wide")

# Sidebar
with st.sidebar:
    st.title("🎯 About This App")
    st.markdown("""
        **Career Path Finder** helps you:
        - Explore personalized career options
        - Identify skills and growth areas
        - Get learning recommendations
        
        Powered by Google's Gemini AI.
    """)
    st.markdown("---")
    st.button("Clear Chat", on_click=lambda: st.session_state.update(chat_history=[]))

# Header
st.markdown("""
    <style>
    .main-title { font-size: 2.5rem; font-weight: bold; text-align: center; color: #4A90E2; margin-bottom: 0.5rem; }
    .subtitle { font-size: 1.2rem; text-align: center; color: gray; margin-bottom: 2rem; }
    </style>
""", unsafe_allow_html=True)

st.markdown('<div class="main-title">🔍 Career Path Finder</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitle">Get personalized advice to find your ideal career direction.</div>', unsafe_allow_html=True)

# Initialize chat history
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# Input box
user_input = st.chat_input("Tell me about your background, skills, or career goals...")

# Handle user input
if user_input:
    # Display user's message
    st.chat_message("user").write(user_input)
    st.session_state.chat_history.append(("user", user_input))

    # Get AI response
    response = get_gemini_response(user_input)
    full_response = ""
    with st.chat_message("assistant"):
        for chunk in response:
            st.write(chunk.text)
            full_response += chunk.text
    st.session_state.chat_history.append(("assistant", full_response))

# Display chat history (on reload)
for role, message in st.session_state.chat_history:
    with st.chat_message(role):
        st.write(message)

