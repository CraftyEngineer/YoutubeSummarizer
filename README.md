# 🎬 YouTube Video Summarizer + Chatbot (CraftyEngineer)

An AI-powered Streamlit app that summarizes YouTube videos — and allows you to **chat** with the summary!  


![Banner](https://github.com/CraftyEngineer/youtubesummarizer/blob/main/ui_ss.png?raw=true)

![Made with Python](https://img.shields.io/badge/Made%20with-Python-1f425f.svg)
![Streamlit](https://img.shields.io/badge/Built%20with-Streamlit-orange)
![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)
[![Open in Streamlit](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://youtubesummarizer-craftyengineer.streamlit.app/)
![Groq API](https://img.shields.io/badge/API-Groq-blue)


---

## 🚀 Features

- 🔗 Summarize **any** YouTube video or short (that has transcript available - supports auto-transcript)
- 🤖 Ask questions about the video — powered by LLM (Groq's LLaMA3)
- ✨ Options to:
  - Choose tone: normal, bullet, simple, funny
  - Translate summary to: Hindi, Spanish, French, German, Japanese
- 📥 Download summary
- 🧼 Clear all session state
- 🖊️ Built-in chat with summarization memory


---

## 🛠 Setup Instructions

### 1. Clone the repo

```bash
git clone https://github.com/CraftyEngineer/youtubesummarizer.git
cd youtubesummarizer
```
## 2. Install requirements

```bash
pip install -r requirements.txt
```
### 3. Add your Groq API key in the terminal

```bash
export GROQ_API_KEY = "your_groq_api_key_here"
```
## 4. Run

```bash
streamlit run main.py
```

---

## 🧠 Example Usage

1. Paste a YouTube link (video or short)
2. Click ▶️ to generate summary (could be in any language and tone)
3. Ask questions like:
   - "What was the main topic?"
   - "Explain in bullet points"
   - "Summarize in Hindi"
  
---

## Deployment
Deployed to Streamlit Cloud  
Make sure to:
  - Add your GROQ_API_KEY in the Secrets section
  - Include requirements.txt in your repo
  - Set main.py as the entry point

---

## 📄 License
MIT License © 2025 CraftyEngineer

---
🙌 Made with ❤️ by CraftyEngineer

  
