import os
import time
import re
import base64
import streamlit as st
from dotenv import load_dotenv
from groq import Groq
from groq import RateLimitError, APIStatusError

load_dotenv()
api_key = os.getenv("GROQ_API_KEY")
client = Groq(api_key=api_key)

FALLBACK_MODELS = [
    "compound-beta",
    "compound-beta-mini",
    "mixtral-8x7b-32768",
    "llama3-70b-8192",
    "gemma2-9b-it",
    "deepseek-r1-distill-llama-70b",
]

def generate_response(messages, model_list=FALLBACK_MODELS, max_wait=45):
    last_error = None
    for model in model_list:
        try:
            resp = client.chat.completions.create(
                model=model,
                messages=messages,
                timeout=max_wait,
                stream=False,
            )
            text = re.sub(r"<think>.*?</think>", "", resp.choices[0].message.content, flags=re.I | re.S).strip()
            return text, model
        except RateLimitError as e:
            retry = float(getattr(e, "retry_after", 0) or e.headers.get("retry-after", 0) or 0)
            if retry:
                time.sleep(min(retry, max_wait))
                continue
            st.toast(f"{model} daily quota exhausted – switching …", icon="⚠️")
            last_error = e
        except APIStatusError as e:
            last_error = e
        except Exception as e:
            last_error = e
    raise RuntimeError("All configured free-tier model quotas are exhausted.") from last_error

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
            color: #000;
            font-size: 1rem;
        }
        .chat-bubble:first-child { margin-top: 2.5rem; }
        .chat-bubble.user { border-left: 4px solid #1a73e8; }
        .chat-bubble.bot { border-left: 4px solid #34a853; }

        .model-tag {
            background: rgba(255, 255, 255, 0.25);
            backdrop-filter: blur(6px);
            -webkit-backdrop-filter: blur(6px);
            color: #000;
            font-size: 1rem;
            padding: 0.25rem 0.6rem;
            border-radius: 6px;
            display: inline-block;
            margin-top: -0.25rem;
            margin-bottom: 0.75rem;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )

def add_lexend_font():
    st.markdown(
        """
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Lexend:wght@300;400;500;600;700&display=swap');
        * { font-family: 'Lexend', sans-serif !important; }
        </style>
        """,
        unsafe_allow_html=True,
    )

def add_title_style():
    st.markdown(
        """
        <style>
        .app-title {
            text-align: center;
            margin: 1rem auto 2rem auto;
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
    st.session_state.history.append({"role": "user", "content": user_input})
    try:
        clean_history = [{"role": m["role"], "content": m["content"]} for m in st.session_state.history]
        bot_reply, model_used = generate_response(clean_history)
    except RuntimeError as e:
        st.error(str(e))
        st.stop()
    st.session_state.history.append({"role": "assistant", "content": bot_reply, "model": model_used})

for turn in st.session_state.history:
    speaker = "You" if turn["role"] == "user" else "Bot"
    role_class = "user" if turn["role"] == "user" else "bot"
    st.markdown(
        f"<div class='chat-bubble {role_class}'><b>{speaker}:</b> {turn['content']}</div>",
        unsafe_allow_html=True,
    )
    if turn["role"] == "assistant":
        st.markdown(f"<span class='model-tag'>Model: {turn['model']}</span>", unsafe_allow_html=True)
