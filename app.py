import os
import streamlit as st
from dotenv import load_dotenv
from groq import Groq
import base64
import re

load_dotenv()
api_key = os.getenv("GROQ_API_KEY")

client = Groq(api_key=api_key)


def generate_response(user_prompt):
    response = client.chat.completions.create(
        messages=[
            {
                "role": "user",
                "content": user_prompt,
            }
        ],
        model="compound-beta",
    )
    content = response.choices[0].message.content
    content = re.sub(r"<think>[\s\S]*?</think>", "", content, flags=re.IGNORECASE).strip()
    return content

def set_background(image_file):
    with open(image_file, "rb") as img:
        encoded = base64.b64encode(img.read()).decode()
    st.markdown(
        f"""
        <style>
        .stApp {{
            background-image: url('data:image/jpeg;base64,{encoded}');
            background-size: cover;
            background-position: center;
            background-repeat: no-repeat;
        }}
        </style>
        """,
        unsafe_allow_html=True,
    )

def add_chat_styles():
    """Inject CSS that adds a blurred translucent background to chat bubbles."""
    st.markdown(
        """
        <style>
        .chat-bubble {
            background: rgba(255, 255, 255, 0.25);
            backdrop-filter: blur(8px);
            -webkit-backdrop-filter: blur(8px);
            border-radius: 8px;
            padding: 0.75rem 1rem;
            margin-bottom: 0.5rem;
            color: #000; /* Ensure text remains dark for readability */
            font-size: 1rem;
        }
        /* Extra space before the first chat bubble to avoid overlap with title */
        .chat-bubble:first-child {
            margin-top: 2.5rem;
        }
        .chat-bubble.user {
            border-left: 4px solid #1a73e8;
        }
        .chat-bubble.bot {
            border-left: 4px solid #34a853;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )

def add_lexend_font():
    """Import Google Lexend font and apply to all text elements."""
    st.markdown(
        """
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Lexend:wght@300;400;500;600;700&display=swap');
        html, body, div, span, input, textarea, label, h1, h2, h3, h4, h5, h6, p, .stApp {
            font-family: 'Lexend', sans-serif !important;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )

def add_title_style():
    """Inject CSS for the main title with blur and centering."""
    st.markdown(
        """
        <style>
        .app-title {
            text-align: center;
            margin: 1rem auto 2rem auto; /* More space below title */
            background: rgba(255, 255, 255, 0.25);
            backdrop-filter: blur(8px);
            -webkit-backdrop-filter: blur(8px);
            padding: 0.75rem 1.25rem;
            border-radius: 12px;
            width: fit-content;
            font-size: 2rem;
            position: relative;
            z-index: 1;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )

st.set_page_config(page_title="AI Chatbot")

set_background("image.png")
add_chat_styles()
add_lexend_font()
add_title_style()

st.markdown("<h1 class='app-title'>🤖 Safwen Chatbot 🤖</h1>", unsafe_allow_html=True)

if "history" not in st.session_state:
    st.session_state.history = []

user_input = st.chat_input("You:")

if user_input:
    bot_reply = generate_response(user_input)
    st.session_state.history.append(("You", user_input))
    st.session_state.history.append(("Bot", bot_reply))

for speaker, message in st.session_state.history:
    role_class = "user" if speaker.lower() == "you" else "bot"
    st.markdown(
        f"<div class='chat-bubble {role_class}'><b>{speaker}:</b> {message}</div>",
        unsafe_allow_html=True,
    )