import streamlit as st
from transcriber import transcribe_audio
import tempfile
import os

# --- Page Config ---
st.set_page_config(
    page_title="Audio Transcriber",
    page_icon="🎧",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# --- Custom CSS ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600&display=swap');

    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
        background: linear-gradient(135deg, #e0f7fa, #fce4ec);
        color: #2c3e50;
    }

    .main-card {
        background: rgba(255, 255, 255, 0.8);
        border-radius: 15px;
        padding: 30px;
        box-shadow: 0 8px 24px rgba(0,0,0,0.1);
        margin-top: 40px;
    }

    .title {
        font-size: 2.8em;
        font-weight: 600;
        text-align: center;
        margin-top: 20px;
        margin-bottom: 10px;
        color: #2c3e50;
    }

    .subtitle {
        font-size: 1.2em;
        text-align: center;
        margin-bottom: 30px;
        color: #555;
    }

    .stButton>button {
        background-color: #2c3e50;
        color: white;
        border-radius: 8px;
        padding: 0.6em 1.2em;
        font-size: 1em;
        font-weight: 600;
        border: none;
    }

    .stDownloadButton>button {
        background-color: #27ae60;
        color: white;
        border-radius: 8px;
        padding: 0.6em 1.2em;
        font-size: 1em;
        font-weight: 600;
        border: none;
        margin-top: 20px;
    }

    textarea {
        background-color: #f9f9f9 !important;
        border-radius: 10px !important;
        padding: 15px !important;
        font-size: 1em !important;
    }
    </style>
""", unsafe_allow_html=True)

# --- Title ---
st.markdown('<div class="title">🎙️ Audio Transcriber</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitle">Upload your audio file and get a clean, timestamped transcript</div>', unsafe_allow_html=True)

# --- Main Card ---
with st.container():
    st.markdown('<div class="main-card">', unsafe_allow_html=True)

    uploaded_file = st.file_uploader("📁 Upload your audio file (MP3 or WAV)", type=["mp3", "wav"])

    if uploaded_file is not None:
        with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as temp_audio:
            temp_audio.write(uploaded_file.read())
            temp_audio_path = temp_audio.name

        st.audio(temp_audio_path, format="audio/mp3")

        if st.button("Start Transcription"):
            with st.spinner("Transcribing..."):
                transcript = transcribe_audio(temp_audio_path)

            if transcript:
                st.subheader("📝 Transcript")
                st.text_area("Transcript Output", transcript, height=400)

                st.download_button(
                    label="📥 Download Transcript",
                    data=transcript,
                    file_name="transcription_output.txt",
                    mime="text/plain"
                )
            else:
                st.error("⚠️ No transcription was generated. Try a different file.")

        os.remove(temp_audio_path)

    st.markdown('</div>', unsafe_allow_html=True)
