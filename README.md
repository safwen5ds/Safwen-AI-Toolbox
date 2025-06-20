# 🤖 Safwen Chatbot

Safwen Chatbot is a minimalist AI chat interface built with Streamlit and powered by Groq's large language models. Type a message and receive real-time answers, all wrapped in a modern glass-morphism UI.

---

## ✨ Features

- **Conversational AI** – Connects to Groq `compound-beta` model via the official SDK.
- **Stylish Interface** – Custom blurred chat bubbles, Google Lexend font, and full-screen background image.
- **Session History** – Keeps the conversation visible for the duration of the browser session.
- **One-Click Deploy** – Ready for Streamlit Community Cloud, Render, Railway, or any Python-friendly host.

---

## 🚀 Quick Start

### 1. Clone the repository

```bash
git clone https://github.com/<your-username>/safwen-chatbot.git
cd safwen-chatbot
```

### 2. (Optional) Create a virtual environment

```bash
python -m venv .venv
# Linux/macOS
source .venv/bin/activate
# Windows
.venv\Scripts\activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

*If you prefer, you can also install manually:*

```bash
pip install streamlit groq python-dotenv
```

### 4. Configure your environment

Create a `.env` file in the project root (same folder as `app.py`) and add your Groq API key:

```env
GROQ_API_KEY=your_api_key_here
```

### 5. Run the app

```bash
streamlit run app.py
```

Your browser should open at `http://localhost:8501` where you can start chatting.

---

## 🗂️ Project Structure

```
.
├── app.py            # Streamlit application
├── image.png         # Background image
├── README.md         # You are here
├── requirements.txt  # Python dependencies
└── .gitignore        # Git exclusion rules
```

---

## 🌐 Deployment

### Streamlit Community Cloud

1. Push this repository to GitHub.
2. Log in to [Streamlit Cloud](https://streamlit.io/cloud) and select "New app".
3. Point it to your repository and set **`app.py`** as the entry point.
4. In *Advanced settings → Secrets*, add `GROQ_API_KEY` with your key.
5. Click **Deploy**.

### Other Platforms

Any platform that supports Python 3.9+ can run the app. Simply install the dependencies and execute `streamlit run app.py`.

---

## 🤝 Contributing

Pull requests are welcome! For major changes, please open an issue first to discuss what you would like to change.

---

## 📄 License

MIT © 2024 Safwen 