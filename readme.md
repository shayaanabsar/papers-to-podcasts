# Papers-to-Podcasts 🎙️📚

Convert dense academic papers into engaging, conversational podcasts. Perfect for researchers, students, and anyone who wants to absorb complex research while commuting, exercising, or doing chores.

**[Try it live →](https://papers-to-podcasts.streamlit.app/)**

## ✨ Features

- **📄 PDF Upload**: Drop any academic paper and get a podcast in minutes
- **🤖 AI-Powered Analysis**: Uses RAG (Retrieval Augmented Generation) to extract key insights accurately
- **🎭 Multi-Speaker Dialogue**: Natural conversation between two hosts (Sarah & Michael)
- **🔊 High-Quality Audio**: Neural TTS with distinct voices for each host
- **⚡ Fast Processing**: Optimized pipeline from paper to podcast

## 🎯 How It Works

1. **Extract & Chunk**: Paper text is split into semantic chunks and embedded
2. **Question Generation**: LLM identifies 5-10 key questions about the research
3. **RAG Retrieval**: For each question, relevant paper sections are retrieved using semantic search
4. **Answer Synthesis**: LLM generates simplified and detailed answers from retrieved context
5. **Script Creation**: Questions and answers are converted into natural dialogue
6. **Audio Generation**: Multi-speaker TTS creates the final podcast

## 🛠️ Tech Stack

- **Frontend**: Streamlit
- **LLM**: Ollama Cloud (GPT-OSS 120B)
- **Embeddings**: Sentence Transformers (all-MiniLM-L6-v2)
- **Vector Search**: FAISS
- **Text Processing**: LangChain, PyPDF2
- **TTS**: Kokoro ONNX (multi-speaker neural TTS)
- **Audio**: scipy, numpy

## 🚀 Local Installation
```bash
# Clone the repository
git clone https://github.com/shayaanabsar/papers-to-podcasts.git
cd papers-to-podcasts

# Install dependencies
pip install -r app/requirements.txt

# Set up API keys (create .streamlit/secrets.toml)
OLLAMA_API_KEY = "your_key_here"

# Run the app
cd app
streamlit run main.py
```

## 📝 Usage

1. Visit [papers-to-podcasts.streamlit.app](https://papers-to-podcasts.streamlit.app/)
2. Upload a PDF of an academic paper
3. Wait 2-5 minutes for processing
4. Listen to or download your podcast!

## 🎓 Perfect For

- **Researchers**: Stay updated on papers in your field during commutes
- **Students**: Review course readings while exercising or cooking
- **Curious Learners**: Explore new topics without reading dense PDFs


## 👤 Author

Built by [Shayaan Absar](https://github.com/shayaanabsar)

---

**Note**: This is a research project. Generated podcasts should supplement, not replace, reading the original papers.