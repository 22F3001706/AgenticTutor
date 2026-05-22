# KAI - Your AI Science & Maths Tutor 

An intelligent Retrieval-Augmented Generation (RAG) application that provides personalized, enthusiastic tutoring for Class 9 students. KAI makes science and maths engaging through real-world examples, storytelling, and voice responses.

## Features 

- **Smart RAG System**: Retrieves relevant content from PDF textbooks and generates contextual answers
- **Interactive Web UI**: User-friendly Gradio interface for easy access
- **Voice Output**: Optional text-to-speech for auditory learning
- **Multi-Subject Support**: Covers Class 9 Science and Maths
- **Multiple Chapters**: Organized content across different topics
- **Engaging Teaching Style**: Uses real-world examples, analogies, and storytelling to make learning exciting
- **Vector Search**: Fast similarity search using FAISS (Facebook AI Similarity Search)

## Project Structure 

```
KAI/V1/
├── main.py              # CLI entry point for RAG chatbot
├── requirements.txt     # Python dependencies
├── BOOKS/
│   ├── C9S/            # Class 9 Science PDFs
│   │   ├── CH1.pdf     # Matter in our surroundings
│   │   ├── CH2.pdf     # Is matter around us pure?
│   │   ├── CH3.pdf     # Atoms and molecules
│   │   └── CH4.pdf     # Structure of the atom
│   └── C9M/            # Class 9 Maths PDFs
├── rag/
│   ├── chain.py        # LLM chain with prompt engineering
│   ├── embeddings.py   # Vector store creation & management
│   ├── loader.py       # PDF loading and text splitting
│   └── voice.py        # Text-to-speech functionality
├── ui/
│   └── app.py          # Gradio web interface
└── vectorstore/        # FAISS vector indexes (auto-generated)
```

## Tech Stack 🛠️

- **LLM**: Groq (Llama 3.3 70B)
- **RAG Framework**: LangChain
- **Vector Database**: FAISS
- **Web UI**: Gradio
- **Text-to-Speech**: gTTS (Google Text-to-Speech)
- **Embeddings**: Hugging Face transformers

## Installation & Setup 

### Prerequisites
- Python 3.10 or higher
- Internet connection (for downloading models and API calls)

### Steps

1. **Clone the repository**
```bash
git clone <repository-url>
cd KAI/V1
```

2. **Create a virtual environment** (recommended)
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

4. **Set up environment variables**
Create a `.env` file in the project root with:
```
GROQ_API_KEY=your_groq_api_key_here
```
Get your API key from [Groq Console](https://console.groq.com)

5. **Add PDFs**
Place your Class 9 textbooks in the `BOOKS/` directory:
- `BOOKS/C9S/` for Science chapters
- `BOOKS/C9M/` for Maths chapters

## Usage 

### Option 1: CLI Chatbot
```bash
python main.py
```
This launches an interactive command-line interface where you can ask questions about Chapter 1.

**Example interaction:**
```
You: What is the difference between elements and compounds?
Assistant: [Enthusiastic explanation with real-world examples...]
```

### Option 2: Web Interface
```bash
python ui/app.py
```
Opens a Gradio web UI where you can:
- Select Class, Subject, and Chapter
- Ask questions through a chat interface
- See AI-generated answers with optional voice output

## How It Works 

1. **Document Loading**: PDFs are parsed and split into manageable chunks
2. **Embedding Generation**: Text chunks are converted into vector embeddings using Hugging Face models
3. **Vector Storage**: Embeddings are stored in FAISS for fast retrieval
4. **Query Processing**: User questions are embedded and matched against stored vectors
5. **LLM Generation**: Retrieved context is passed to Groq's Llama 3.3 with a crafted prompt
6. **Voice Output** (optional): Answers are converted to speech using gTTS

## Configuration 

### Add More Chapters/Subjects
Edit `ui/app.py` and modify the `CONTENT` dictionary:

```python
CONTENT = {
    "Class 9": {
        "Science": {
            "Ch 1 - Matter in our surroundings": "BOOKS/C9S/CH1.pdf",
            "Ch 2 - Is matter around us pure?": "BOOKS/C9S/CH2.pdf",
            # Add more chapters here
        },
        "Maths": {
            "Ch 1 - Number systems": "BOOKS/C9M/CH1.pdf",
            # Add more chapters here
        }
    }
}
```

### Adjust Teaching Style
Modify the system prompt in `rag/chain.py` to customize the teaching approach.

## Requirements 

See `requirements.txt` for the complete list. Key dependencies:
- langchain
- langchain-groq
- faiss-cpu (or faiss-gpu for GPU support)
- gradio
- gtts
- pypdf
- sentence-transformers

## Troubleshooting 

**PDF not found error?**
- Ensure PDF files are placed in the correct `BOOKS/` subdirectories
- Check file names match those in the `CONTENT` dictionary

**Voice not working?**
- Ensure gTTS is installed: `pip install gtts`
- Check internet connection (gTTS requires it)
- Voice errors are silently handled; the app will continue working

**Slow responses?**
- First response takes longer as models are loaded
- Subsequent responses are faster
- Consider using GPU with `faiss-gpu` for faster embeddings

**API errors?**
- Verify your `GROQ_API_KEY` is valid and set in `.env`
- Check your Groq account quota

## Future Enhancements 

- [ ] Support for more classes and subjects
- [ ] Offline LLM option using Ollama
- [ ] Quiz mode and progress tracking
- [ ] Multilingual support
- [ ] Student performance analytics
- [ ] Integration with learning management systems

## Contributing 

Contributions are welcome! Feel free to:
- Add more textbooks and chapters
- Improve the teaching prompt
- Add new features
- Report bugs



## Support 

For questions or issues, please open an issue on GitHub or contact the development team.

---

**Made with love for curious learners**
