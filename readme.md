# 🧠 GenAnIML

This project sets up a local AI-powered chatbot using `ollama`, with document and weblink ingestion capabilities. It features a Streamlit-based frontend for easy interaction.

---

## 🚀 Setup

### 1. Install Dependencies

Install the required system packages using Homebrew:

```bash
brew install python poppler tesseract
```

### 2. Ensure Python and ollama are installed.
   
   Ensure Python version is >= 3.12.6.
   
   Ensure [ollama](https://ollama.com/download/windows) is installed
You can check your version with:

```bash
python3 --version
```
### 3. Create and Activate Virtual Environment
``` bash
python3 -m venv <path/to/venv>
source <path/to/venv>/bin/activate
```

### 4. Install Python Packages

```bash
python -m pip install -r requirements.txt
```

### 5. Pull the AI Model
   Make sure ollama is installed and then run:

```bash
python -c "import ollama; ollama.pull('gemma2:2b')"
```

🛠️ Usage

1. Start the Web UI

```bash
streamlit run frontend.py
```

2. Add Local Documents

```bash
python vectore_store.py
```

3. Add FAQ / Weblink Data

```bash
python faq_parser.py
```

📁 Project Structure

```bash
.
├── app.py                # Main application script
├── chroma_db/            # Directory for ChromaDB persistent storage
├── frontend.py           # Streamlit UI
├── gen_ollama.py         # Script for interacting with the Ollama chat model
├── pdf_chunk.py          # Script for processing and translating PDF files
├── faq_parser.py         # Script to parse and add FAQ/weblink data
├── SpeechToText.py       # Speech-to-text processing script
├── rag_llama_chroma.py   # Script for querying vector store and AI response generation
├── vector_store.py       # Script to manage vector store using ChromaDB
├── requirements.txt      # Python package dependencies
├── readme.md             # Project documentation
├── test.py               # Test script for translation
├── karnataka.pdf         # Example PDF file for processing
└── .gitignore            # Git ignore file
```

✅ Notes
Make sure to activate the virtual environment before running any scripts.
The AI model will be pulled using ollama, ensure you have it installed and set up correctly.
