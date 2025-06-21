import os, time, re, base64
import streamlit as st
from dotenv import load_dotenv
from groq import Groq, RateLimitError, APIStatusError

load_dotenv()
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

FALLBACK_MODELS = [
    "compound-beta",
    "compound-beta-mini",
    "mixtral-8x7b-32768",
    "llama3-70b-8192",
    "gemma2-9b-it",
    "deepseek-r1-distill-llama-70b",
]

def generate_response(history, model_list=FALLBACK_MODELS, max_wait=45):
    last_error = None
    for model in model_list:
        try:
            resp = client.chat.completions.create(
                model=model, messages=history, timeout=max_wait, stream=False
            )
            txt = re.sub(r"<think>.*?</think>", "", resp.choices[0].message.content,
                         flags=re.I | re.S).strip()
            return txt, model
        except RateLimitError as e:
            retry = float(getattr(e, "retry_after", 0) or e.headers.get("retry-after", 0) or 0)
            if retry:
                time.sleep(min(retry, max_wait))
                continue
            st.toast(f"{model} daily quota exhausted – switching …", icon="⚠️")
            last_error = e
        except (APIStatusError, Exception) as e:
            last_error = e
    raise RuntimeError("All configured free-tier model quotas are exhausted.") from last_error

def set_background(img_path):
    with open(img_path, "rb") as f:
        b64 = base64.b64encode(f.read()).decode()
    st.markdown(f"""
        <style>
        .stApp {{
            background: url("data:image/png;base64,{b64}") center/cover no-repeat;
        }}
        </style>
    """, unsafe_allow_html=True)

def add_chat_styles():
    st.markdown("""
        <style>
        .chat-bubble{{
            background:#262730!important;
            backdrop-filter:blur(8px);
            -webkit-backdrop-filter:blur(8px);
            border-radius:8px;
            padding:.75rem 1rem;
            margin-bottom:.5rem;
            color:#fff!important;
            font-size:1rem;
        }}
        .chat-bubble:first-child{{margin-top:2.5rem;}}
        .chat-bubble.user{{border-left:4px solid #1a73e8;}}
        .chat-bubble.bot{{border-left:4px solid #34a853;}}
        .model-tag{{
            background:#262730!important;
            backdrop-filter:blur(6px);
            -webkit-backdrop-filter:blur(6px);
            border-radius:6px;
            font-size:1rem;
            padding:.25rem .6rem;
            display:inline-block;
            margin-top:-.25rem;
            margin-bottom:.75rem;
            color:#fff!important;
        }}
        .appview-container .main .block-container{{
            background:#262730CC;
            padding:2rem 2.5rem;
            border-radius:16px;
        }}
        </style>
    """, unsafe_allow_html=True)

def add_fonts_and_overrides():
    st.markdown("""
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Lexend:wght@300;400;500;600;700&display=swap');
        body, p, h1, h2, h3, h4, h5, h6,
        .chat-bubble, .model-tag, input, textarea, button{{
            font-family:'Lexend',sans-serif;
        }}
        [data-testid="collapsed-control"] span{{
            font-family:'Material Symbols Outlined'!important;
            font-variation-settings:'FILL' 0,'wght' 400,'GRAD' 0,'opsz' 48;
        }}
        [data-testid="stMarkdownHeadingLink"]{{display:none!important;}}
        </style>
    """, unsafe_allow_html=True)

def add_title_style():
    st.markdown("""
        <style>
        .app-title{{
            margin:1.5rem auto 2.5rem auto;
            padding:.75rem 1.5rem;
            background:#262730!important;
            backdrop-filter:blur(8px);
            -webkit-backdrop-filter:blur(8px);
            border-radius:12px;
            font-size:2.4rem;
            width:max-content+3;
            display:flex;
            justify-content:center;
            align-items:center;
            gap:.5rem;
            color:#fff!important;  
            
        }}
        .app-title .emoji{{
            font-family:
              "Noto Color Emoji",
              "Apple Color Emoji",
              "Segoe UI Emoji",
              "Twemoji Mozilla",
              sans-serif;
        }}
        h1.app-title{{margin:0 auto;}}
        </style>
    """, unsafe_allow_html=True)

st.set_page_config(page_title="AI Chatbot", page_icon="🤖")
set_background("image.png")
add_chat_styles()
add_fonts_and_overrides()
add_title_style()

st.markdown(
    """
    <h1 class="app-title">
      <span class="emoji">🤖</span>
      <span>Safwen&nbsp;Chatbot</span>
      <span class="emoji">🤖</span>
    </h1>
    """,
    unsafe_allow_html=True,
)

# Use a page-specific key so that chat history is not shared across the whole app
HIST_KEY = "chatbot_history"

if HIST_KEY not in st.session_state:
    st.session_state[HIST_KEY] = []

user_msg = st.chat_input("You:")
if user_msg:
    st.session_state[HIST_KEY].append({"role":"user","content":user_msg})
    try:
        clean_hist = [{"role":t["role"],"content":t["content"]} for t in st.session_state[HIST_KEY]]
        bot_msg, used_model = generate_response(clean_hist)
    except RuntimeError as e:
        st.error(str(e))
        st.stop()
    st.session_state[HIST_KEY].append({"role":"assistant","content":bot_msg,"model":used_model})

for turn in st.session_state[HIST_KEY]:
    speaker = "You" if turn["role"]=="user" else "Bot"
    role_cls = "user" if turn["role"]=="user" else "bot"
    st.markdown(
        f"<div class='chat-bubble {role_cls}'><b>{speaker}:</b> {turn['content']}</div>",
        unsafe_allow_html=True
    )
    if turn["role"]=="assistant":
        st.markdown(
            f"<span class='model-tag'>Model: {turn['model']}</span>",
            unsafe_allow_html=True
        )