import streamlit as st
from transformers import pipeline

@st.cache_resource(show_spinner="Loading sentiment model...")
def get_analyzer():
    return pipeline("sentiment-analysis")

analyze = get_analyzer()

st.set_page_config(page_title="Sentiment Aalyzer by Safwen Gharbi")
st.title("Real-Time Sentiment Analyzer")

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