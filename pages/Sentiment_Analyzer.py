import streamlit as st, base64, os
from transformers import pipeline

@st.cache_resource(show_spinner="Loading sentiment model...")
def get_analyzer():
    return pipeline("sentiment-analysis")

analyze = get_analyzer()

st.set_page_config(page_title="Sentiment Aalyzer by Safwen Gharbi",page_icon="🤖")
# Use Lexend font across this page
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Lexend:wght@300;400;500;600;700&display=swap');
body, p, h1, h2, h3, h4, h5, h6, input, textarea, button{
    font-family: 'Lexend', sans-serif;
}
/* --- bubble background for title and textarea label --- */
h1{
    display:inline-block;
    padding:.4rem 1rem;
    border-radius:10px;
    background:rgba(0,0,0,.35);
    color:#fff;
    backdrop-filter:blur(8px);
}
/* Target the label that Streamlit generates for the textarea */
div[data-baseweb="textarea"] > label{
    display:inline-block;
    padding:.3rem .9rem;
    border-radius:8px;
    background:rgba(0,0,0,.35);
    color:#fff;
    backdrop-filter:blur(8px);
}
/* broaden: apply to any label inside the container */
div[data-baseweb="textarea"] label{
    display:inline-block;
    padding:.3rem .9rem;
    border-radius:8px;
    background:rgba(0,0,0,.35);
    color:#fff;
    backdrop-filter:blur(8px);
}
</style>
""", unsafe_allow_html=True)
st.title("Real-Time Sentiment Analyzer")

# --- background helper ---
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

txt = st.text_area(
    "Paste any neglish text and click *Analyze*",
    height=180,
    placeholder="Type or paste a text"
)

if st.button("Analyze",use_container_width=True) and txt.strip():
    with st.spinner("Thinking..."):
        result = analyze(txt[:512])[0]

    lbl = result["label"].title()
    score = f"{result['score']*100:.2f}%"

    st.markdown(
        f"""
        <div style="
            margin-top:1.2rem;
            display:inline-block;
            padding:.5rem .9rem;
            border-radius:8px;
            backdrop-filter:blur(8px);
            background:rgba(255,255,255,.25);
            font-size:1.1rem;
            ">
            <b>Sentiment:</b> {lbl} &nbsp; • &nbsp; <b>Confidence:</b> {score}
        </div>
        """,
        unsafe_allow_html=True
    )