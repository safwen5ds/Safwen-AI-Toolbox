import io, time, tempfile, base64, os
from pathlib import Path
import streamlit as st
from groq import Groq, RateLimitError, APIStatusError

st.set_page_config(page_title="Text-to-Speech",page_icon="🤖")

# --- background ---
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

set_background("image.png")

# Use Lexend font across this page
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Lexend:wght@300;400;500;600;700&display=swap');
body, p, h1, h2, h3, h4, h5, h6, input, textarea, button{
    font-family: 'Lexend', sans-serif;
}
/* --- bubble background --- */
h1,
.input-bubble,
div[data-baseweb="textarea"] label,
div[data-baseweb="select"] label{
    display:inline-block;
    padding:.4rem 1rem;
    border-radius:10px;
    background:rgba(0,0,0,.35);
    color:#fff;
    backdrop-filter:blur(8px);
    margin-bottom:.4rem;
}
/* bigger space below page title */
h1{
    margin-bottom:1.5rem;
}
</style>
""", unsafe_allow_html=True)
st.title("Text-to-Speech (Groq + PlayAI) By Safwen Gharbi")

# Custom bubble label for textarea
st.markdown(
    """
    <div class="input-bubble">Enter the text you'd like to hear:</div>
    """,
    unsafe_allow_html=True
)

text_input = st.text_area(
    "",
    height=180,
    placeholder="write something",
    label_visibility="collapsed"
)

EN_VOICES = [
    "Arista-PlayAI", "Atlas-PlayAI", "Basil-PlayAI", "Briggs-PlayAI",
    "Calum-PlayAI", "Celeste-PlayAI", "Cheyenne-PlayAI", "Chip-PlayAI",
    "Cillian-PlayAI", "Deedee-PlayAI", "Fritz-PlayAI", "Gail-PlayAI",
    "Indigo-PlayAI", "Mamaw-PlayAI", "Mason-PlayAI", "Mikail-PlayAI",
    "Mitch-PlayAI", "Quinn-PlayAI", "Thunder-PlayAI"
]
AR_VOICES = ["Ahmad-PlayAI", "Amira-PlayAI", "Khalid-PlayAI", "Nasser-PlayAI"]

LANG_MODEL = {
    "English": ("playai-tts", EN_VOICES),
    "Arabic" : ("playai-tts-arabic", AR_VOICES),
}

col1, col2 = st.columns(2)
language = col1.selectbox("Language", list(LANG_MODEL.keys()), index=0)
model_id, voices = LANG_MODEL[language]
voice = col2.selectbox("Voice", voices, index=1)

generate_btn = st.button("Generate 🔊", use_container_width=True, disabled=not text_input.strip())


@st.cache_resource(show_spinner="connecting to Groq ...")
def get_client():
    import os
    return Groq(api_key=os.getenv("GROQ_API_KEY"))

client = get_client()

if generate_btn:
    try:
        with  st.spinner("Voicing your text …"):
           resp = client.audio.speech.create(
                model=model_id,
                voice=voice,
                input=text_input.strip()[:10_000],
                response_format="wav",
            )

        with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as tmp:
                resp.write_to_file(tmp.name)
                tmp.seek(0)
                audio_bytes = tmp.read()

        st.audio(audio_bytes, format="audio/wav")

        fname = f"tts_{int(time.time())}.wav"
        st.download_button("Download .wav", audio_bytes,
                               file_name=fname, mime="audio/wav",
                               use_container_width=True)
        os.remove(tmp.name) 

    except RateLimitError:
        st.error("Daily Groq TTS quota exhausted — please try again tomorrow.")
    except APIStatusError as e:
        st.error(f"Groq API returned an error: {e.status_code}")
    except Exception as e:
        st.error(f"Something went wrong: {e}")