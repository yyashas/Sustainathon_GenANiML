import streamlit as st
import sounddevice as sd
import numpy as np
from scipy.io.wavfile import write
from rag_llama_chroma import get_response
from googletrans import Translator
from deep_translator import GoogleTranslator
from io import BytesIO
from SpeechToText import SpeechToText  # Import your SpeechToText class
from pdf_chunk import PDFTranslator


pfd_translator = PDFTranslator()
translator = Translator()
# Initialize session state for recording control
if "recording" not in st.session_state:
    st.session_state.recording = False
    st.session_state.audio_data = []

def start_recording(samplerate=44100):
    """Start recording audio."""
    st.session_state.recording = True
    st.session_state.audio_data = []  # Store audio chunks

    with sd.InputStream(samplerate=samplerate, channels=1, dtype="int16") as stream:
        st.info("Recording... Click 'Stop Recording' to end.")
        while st.session_state.recording:
            audio_chunk, _ = stream.read(1024)
            st.session_state.audio_data.append(audio_chunk)

def stop_recording(language):
    """Stop recording and process audio."""
    st.session_state.recording = False
    if st.session_state.audio_data:
        audio_data = np.concatenate(st.session_state.audio_data, axis=0)
        process_audio(audio_data, language)


def process_audio(audio_data, language):
    """Process recorded audio and generate AI response."""
    audio_buffer = BytesIO()
    write(audio_buffer, 44100, audio_data)  # Save as WAV
    audio_buffer.seek(0)

    stt_processor = SpeechToText(language=language)
    transcribed_text = stt_processor.recognize_speech_from_file(audio_buffer)
    
    st.text_area("Transcribed Text", transcribed_text, height=150)

    if transcribed_text and not transcribed_text.startswith("[Error"):
        # Generate AI response using your GenAI class
        if language == 'kn-IN':
            # Translate to English for processing
            translated_text = GoogleTranslator(source='kn', target='en').translate(transcribed_text)
            # transcribed_text = translator.translate(transcribed_text, src='kn', dest='en').text
            
        
        gen_ai_response = get_response(translated_text)
        st.text_area("AI Response", gen_ai_response, height=150)

# Streamlit app setup
st.set_page_config(
    page_title="Wildlife Conflict Resolution AI",
    page_icon="🌿",
    layout="wide",
)

st.markdown("""
    <style>
        body {
            background-color: #e1f5fe;
        }
        .main {
            background-color: #ffffff;
            padding: 30px;
            border-radius: 10px;
            box-shadow: 2px 2px 12px rgba(0, 0, 0, 0.1);
        }
        button {
            background-color: #4caf50;
            color: white;
            padding: 10px 20px;
            margin: 10px;
            border-radius: 5px;
            border: none;
            cursor: pointer;
        }
        
        h1 {
            color: #01579b;
            font-family: 'Arial', sans-serif;
        }
        h3 {
            color: #0277bd;
            font-family: 'Arial', sans-serif;
        }
    </style>
    """, unsafe_allow_html=True)

st.title("🌿 Wildlife Conflict Resolution AI")
st.markdown(
    """
    ### Welcome to the Wildlife and Environmental Law AI System

    This tool is designed to assist in resolving human-wildlife conflicts by leveraging advanced AI technologies. 
    Record your voice or type an issue, and the AI will provide insights and possible legal resolutions.
    """,
    unsafe_allow_html=True
)

# Input Mode Selection
input_mode = st.radio("Select Input Mode:", ("🎙️ Voice Input", "⌨️ Text Input"))

# Language selection
language_option = st.radio("Select Language for Processing:", ("English", "Kannada"))
language_code = 'en-US' if language_option == "English" else 'kn-IN'

if input_mode == "🎙️ Voice Input":
    # Recording buttons
    col1, col2 = st.columns(2)
    with col1:
        if st.button("🎙️ Start Recording"):
            start_recording()

    with col2:
        if st.button("🛑 Stop Recording"):
            stop_recording(language=language_code)

elif input_mode == "⌨️ Text Input":
    if language_code == 'en-US':
        user_text = st.text_area("Enter your text:", "")
        if st.button("Submit Text"):
            if user_text:
                # Process manually entered text
                gen_ai_response = get_response(user_query=user_text)
                st.text_area("AI Response", gen_ai_response, height=150)
            else:
                st.warning("Please enter some text before submitting.")
    else:
        st.warning("Kannada text Input not available yet 🙂")
    
    

st.markdown("<hr>", unsafe_allow_html=True)

st.markdown(
    """
    **How to Use:**
    - Choose either "Voice Input" to record or "Text Input" to type.
    - If using voice, select a language and record your issue.
    - If using text, type your issue and click submit.
    - Review the AI-generated response below.
    """,
    unsafe_allow_html=True
)

st.markdown("<hr>", unsafe_allow_html=True)
