# 🧩 Safwen AI Toolbox

A multi-tool, glass-morphism-styled AI interface built with Streamlit. It bundles a conversational chatbot, vision-enabled image chat, real-time sentiment analysis, and text-to-speech, all powered by Groq's large-language-model API and Hugging Face transformers.

---

## ✨ Features

- **Conversational AI** – Connects to Groq `compound-beta` model and other models via the official API.
- **Stylish Interface** – Custom blurred chat bubbles, Google Lexend font, and full-screen background image.
- **Session History** – Keeps the conversation visible for the duration of the browser session.
- **One-Click Deploy** – Ready for Streamlit Community Cloud.

---

## 🗂️ Project Layout
```
.
├── App.py               # Main Streamlit entry point (chatbot UI)
├── pages/
│   ├── Vision_Chat.py   # Image + text conversation
│   ├── Sentiment_Analyzer.py
│   └── Text_to_Speech.py
├── image.png            # Background image asset
├── requirements.txt     # Python dependencies
└── README.md            # You are here
```

---

## 🤝 Contributing
Pull requests are welcome! For major changes, please open an issue first to discuss what you would like to change.

---

## 📄 License

MIT © 2024 Safwen Gharbi 
