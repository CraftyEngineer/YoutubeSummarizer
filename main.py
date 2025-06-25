import time
start = time.time()

import streamlit as st
from youtube_transcript_api import YouTubeTranscriptApi, NoTranscriptFound
from groq import Groq
import os
import re
import base64
from deep_translator import GoogleTranslator
from io import StringIO

# ---------------- CONFIG ----------------
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
# MODEL = "deepseek-r1-distill-llama-70b"
MODEL = "llama3-8b-8192"
client = Groq(api_key=GROQ_API_KEY)


# ---------------- HELPERS ----------------
# print("Groq version:", groq.__version__)
def get_video_id(url):
    if "shorts/" in url:
        return url.split("shorts/")[-1].split("?")[0]
    elif "watch?v=" in url:
        return url.split("watch?v=")[-1].split("&")[0]
    else:
        return None

@st.cache_data(show_spinner=False)
def fetch_transcript(video_id):
    transcript = YouTubeTranscriptApi.get_transcript(video_id)
    return " ".join([entry['text'] for entry in transcript])

def clean_response(text):
    return re.sub(r"<think>.*?</think>", "", text, flags=re.DOTALL).strip()

def summarize(text, tone="normal"):
    tone_instruction = {
        "normal": "",
        "simple": "Make it beginner-friendly and easy to understand.",
        "bullet": "Return bullet points only.",
        "funny": "Add a humorous tone while summarizing."
    }.get(tone, "")

    prompt = f"Summarize the following YouTube transcript. {tone_instruction}\n\n{text[:18000]}"
    response = client.chat.completions.create(
        model=MODEL,
        messages=[
            {"role": "system", "content": "You are a helpful assistant summarizing YouTube transcripts."},
            {"role": "user", "content": prompt},
        ]
    )
    return clean_response(response.choices[0].message.content)

def query_llm(summary, user_input):
    prompt = f"Based on this summary:\n\n{summary}\n\nAnswer this:\n{user_input}"
    response = client.chat.completions.create(
        model=MODEL,
        messages=[
            {"role": "system", "content": "You are a helpful assistant answering questions from video summaries."},
            {"role": "user", "content": prompt},
        ]
    )
    return clean_response(response.choices[0].message.content)

def translate_text(text, lang_code):
    return GoogleTranslator(source='auto', target=lang_code).translate(text)


# ---------------- STREAMLIT UI ----------------
st.title("🎬 YouTube Video Summarizer + Chat")

# Session state
if "summary" not in st.session_state: st.session_state.summary = None
if "video_id" not in st.session_state: st.session_state.video_id = None
if "last_answer" not in st.session_state: st.session_state.last_answer = ""
if "user_query" not in st.session_state: st.session_state.user_query = ""
if "yt_url" not in st.session_state: st.session_state.yt_url = ""

# YouTube Input + Generate Button
col1, col2 = st.columns([5, 1])
with col1:
    st.session_state.yt_url = st.text_input("YouTube URL", value=st.session_state.yt_url, label_visibility="collapsed")
with col2:
    generate_clicked = st.button("▶️", use_container_width=True)

# Options
st.sidebar.header("🛠 Options")
tone = st.sidebar.selectbox("Tone of Summary", ["normal", "simple", "bullet", "funny"])
language = st.sidebar.selectbox("Translate Summary To", ["None", "hi", "es", "fr", "de", "ja"])

# Generate Summary
if st.session_state.yt_url and generate_clicked:
    video_id = get_video_id(st.session_state.yt_url)
    with st.spinner("Fetching transcript and summarizing..."):
        try:
            transcript_raw = fetch_transcript(video_id)
            # punctuated = punctuate_text(transcript_raw)
            summary = summarize(transcript_raw, tone=tone)
            if language != "None":
                summary = translate_text(summary, language)

            st.session_state.summary = summary
            st.session_state.video_id = video_id
            st.session_state.last_answer = ""
            st.session_state.user_query = ""
            st.success("✅ Summary Ready!")
        except NoTranscriptFound:
            st.error("❌ Transcript not available.")
        except Exception as e:
            st.error(f"❌ Error: {e}")

# Summary Display & Download
if st.session_state.summary:
    st.subheader("📄 Summary")
    st.info(st.session_state.summary)
    st.download_button("⬇️ Download Summary", st.session_state.summary, file_name="summary.txt")

    st.subheader("💬 Ask anything about the video")

    col3, col4 = st.columns([5, 1])
    with col3:
        user_query = st.text_input("Ask a question:", value="", label_visibility="collapsed", key="user_query_input")
    with col4:
        send_clicked = st.button("📤", use_container_width=True)

    if send_clicked and user_query:
        with st.spinner("Thinking..."):
            response = query_llm(st.session_state.summary, user_query)
            if language != "None":
                response = translate_text(response, language)
            st.session_state.last_answer = response


    if st.session_state.last_answer:
        st.subheader("🧠 Answer")
        st.success(st.session_state.last_answer)

# Clear All Button
st.markdown("---")
if st.button("🗑️ Clear All", type="primary"):
    
    for key in st.session_state.keys():
        del st.session_state[key]
    st.rerun()
    st.session_state.clear()
# Footer
st.markdown("---")

st.markdown(
    "<div style='text-align: left; color: gray;'>Made with ❤️ by <a href='https://github.com/CraftyEngineer' target='_blank'><b>CraftyEngineer</b></a></div>",
    unsafe_allow_html=True
)


print(f"✅ App loaded in {round(time.time() - start, 2)} sec")
