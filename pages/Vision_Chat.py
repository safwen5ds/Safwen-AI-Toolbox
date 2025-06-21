import os, base64, streamlit as st
from groq import Groq, RateLimitError, APIStatusError

def encode_image(file):
    return base64.b64encode(file.read()).decode()

def as_data_url(file, b64):
    mime = "image/png" if file.type.endswith("png") else "image/jpeg"
    return f"data:{mime};base64,{b64}"

@st.cache_resource(show_spinner="Connecting to Groq …")
def get_client():
    return Groq(api_key=os.getenv("GROQ_API_KEY"))

client = get_client()

# --- set page background ---
def set_background(img_path="image.png"):
    if not os.path.isfile(img_path):
        return
    with open(img_path, "rb") as f:
        b64 = base64.b64encode(f.read()).decode()
    st.markdown(f"""
        <style>
        .stApp {{
            background: url("data:image/png;base64,{b64}") center/cover no-repeat;
        }}
        </style>
    """, unsafe_allow_html=True)

# Page config & background
st.set_page_config(page_title="Groq Vision Chat By Safwen Gharbi",page_icon="🤖")
set_background("image.png")

# Use Lexend font across this page
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Lexend:wght@300;400;500;600;700&display=swap');
body, p, h1, h2, h3, h4, h5, h6, input, textarea, button{
    font-family: 'Lexend', sans-serif;
}
/* --- bubble background style --- */
h1,
.input-bubble,
div[data-baseweb="select"] label,
div[data-baseweb="textarea"] label{
    display:inline-block;
    padding:.4rem 1rem;
    border-radius:10px;
    background:rgba(0,0,0,.35);
    color:#fff;
    backdrop-filter:blur(8px);
    margin-bottom:.4rem;
}
</style>
""", unsafe_allow_html=True)
st.title("Groq Vision Chat – Llama-4 Scout 17 B")

# Custom bubble label for file uploader
st.markdown(
    """
    <div class="input-bubble">image (jpg/jpeg/png)</div>
    """,
    unsafe_allow_html=True
)

# Use a dedicated session key so Vision chat history is not shared with other pages
HIST_KEY = "vision_history"

if HIST_KEY not in st.session_state:
    st.session_state[HIST_KEY] = []

for turn in st.session_state[HIST_KEY]:
    with st.chat_message(turn["role"]):
        st.markdown(turn["content"], unsafe_allow_html=True)

user_text = st.chat_input("Ask me anything…")
user_img = st.file_uploader("", type=["jpg", "jpeg", "png"], label_visibility="collapsed")

if user_text or user_img:
    blocks = []
    if user_text:
        blocks.append({"type": "text", "text": user_text})
    if user_img:
        b64 = encode_image(user_img)
        blocks.append({"type": "image_url", "image_url": {"url": as_data_url(user_img, b64)}})

    st.session_state[HIST_KEY].append({"role": "user", "content": user_text if user_text else "*[image]*"})

    messages = [{"role": t["role"], "content": t["content"]} for t in st.session_state[HIST_KEY][:-1]] + [{"role": "user", "content": blocks}]

    streaming = not user_img
    try:
        resp = client.chat.completions.create(
            model="meta-llama/llama-4-scout-17b-16e-instruct",
            messages=messages,
            max_completion_tokens=1024,
            temperature=1,
            top_p=1,
            stream=streaming,
        )

        if streaming:
            full, slot = "", st.empty()
            with st.chat_message("assistant"):
                for chunk in resp:
                    tok = chunk.choices[0].delta.content or ""
                    full += tok
                    slot.markdown(full)
        else:
            full = resp.choices[0].message.content
            with st.chat_message("assistant"):
                st.markdown(full)

        st.session_state[HIST_KEY].append({"role": "assistant", "content": full})

    except RateLimitError:
        st.error("Daily Groq quota exhausted — please try again tomorrow.")
    except APIStatusError as e:
        st.error(f"Groq API error: {e.status_code}")
    except Exception as e:
        st.error(f"Unexpected error: {e}")
