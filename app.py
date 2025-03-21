import streamlit as st
import sounddevice as sd
import numpy as np
from scipy.io.wavfile import write
from io import BytesIO
from deep_translator import GoogleTranslator
from SpeechToText import SpeechToText  # Import your SpeechToText class
from rag_llama_chroma import get_response

# Path to the generated logo (Ensure it's in the same directory or adjust the path)
LOGO_PATH = "logo.png"

# Initialize session state variables
if "recording" not in st.session_state:
    st.session_state.recording = False
    st.session_state.audio_data = []
if "show_tasks" not in st.session_state:
    st.session_state.show_tasks = False  # Controls task list visibility
if "task_list" not in st.session_state:
    st.session_state.task_list = {}
if "gen_ai_response" not in st.session_state:
    st.session_state.gen_ai_response = None  # Stores AI response

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
        if language == 'kn-IN':
            # Translate to English for processing
            transcribed_text = GoogleTranslator(source='kn', target='en').translate(transcribed_text)
      
        st.session_state.gen_ai_response = get_response(transcribed_text) # Placeholder
        st.session_state.show_tasks = True  # Show task list after response

# Streamlit app setup
st.set_page_config(
    page_title="GenAnIML - Wildlife AI",
    page_icon="🌿",
    layout="wide",
)

# Display the logo at the top
st.image(LOGO_PATH, width=250)

st.title("🌿 GenAnIML - Wildlife Conflict Resolution AI")
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
                st.session_state.gen_ai_response = get_response(user_text)  # Placeholder
                st.session_state.show_tasks = True  # Show task list after response
            else:
                st.warning("Please enter some text before submitting.")
    else:
        st.warning("Kannada text Input not available yet 🙂")

st.markdown("<hr>", unsafe_allow_html=True)

# "New Chat" button to reset everything
if st.button("🆕 New Chat"):
    st.session_state.gen_ai_response = None
    st.session_state.show_tasks = False
    st.session_state.task_list = {f"task_{i}": False for i in range(7)}
    st.rerun()  # Refresh UI

# Display AI Response if available
if st.session_state.gen_ai_response:
    st.text_area("AI Response", st.session_state.gen_ai_response, height=150)

# Define task list
tasks = [
    "Verify the location of the conflict",
    "Identify the wildlife species involved",
    "Check local wildlife protection laws",
    "Consult with forest officials",
    "Report the incident through proper channels",
    "Explore mitigation strategies",
    "Educate the local community about wildlife safety"
]

# Initialize session state for task list
if not st.session_state.task_list:
    st.session_state.task_list = {f"task_{i}": False for i in range(len(tasks))}

# Show task list if AI response is available
if st.session_state.show_tasks:
    st.subheader("✅ Suggested Actions")

    # Display checkboxes with persistent states
    for i, task in enumerate(tasks):
        state_key = f"task_{i}"
        st.session_state.task_list[state_key] = st.checkbox(
            task, value=st.session_state.task_list[state_key], key=state_key
        )

    # "Done" button with validation
    if st.button("✔️ Done"):
        if all(st.session_state.task_list.values()):  # Check if all tasks are ticked
            st.success("🎉 ALL TASKS DONE! Great job!")
        else:
            st.warning("⚠️ Tasks are incomplete! Please complete all tasks before finishing.")

st.markdown("<hr>", unsafe_allow_html=True)

st.markdown(
    """
    **How to Use:**
    - Choose either "Voice Input" to record or "Text Input" to type.
    - If using voice, select a language and record your issue.
    - If using text, type your issue and click submit.
    - Review the AI-generated response below.
    - Complete the suggested actions and click "Done."
    - Click "New Chat" to start over.
    """,
    unsafe_allow_html=True
)

st.markdown("<hr>", unsafe_allow_html=True)


