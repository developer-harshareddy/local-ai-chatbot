
# Local AI Chatbot

A locally running AI chatbot built using Python, Streamlit, Ollama,
and PostgreSQL.

The project is designed as a hands-on AI engineering learning project,
covering LLM integration, conversation memory, RAG, tool calling,
agentic workflows, and backend development.

## Technology Stack

- Python
- Ollama
- Qwen 2.5 1.5B
- Streamlit
- PostgreSQL
- Psycopg
- Python-dotenv
- Git and GitHub

## Architecture

Browser / Streamlit UI
        |
        v
Python application
        |
        +------------------+
        |                  |
        v                  v
PostgreSQL             Ollama API
Chat history           Local LLM
                           |
                           v
                      Qwen 2.5 1.5B

## Current Features

- Local LLM integration using Ollama REST API
- Interactive terminal chatbot
- Conversation history management
- Streamlit web-based chat interface
- Clear conversation functionality
- PostgreSQL database setup for persistent chat history

## Project Progress

| Stage | Description | Status |
|---|---|---|
| 1 | Python environment setup | Completed |
| 2 | Ollama API integration | Completed |
| 3 | Terminal chatbot | Completed |
| 4 | Streamlit chatbot UI | Completed |
| 5A | PostgreSQL database setup | Completed |
| 5B–5F | Persistent conversation integration | In progress |
| 6 | Streaming responses | Planned |
| 7 | PDF document extraction | Planned |
| 8 | Chunking and embeddings | Planned |
| 9 | RAG implementation | Planned |
| 10 | Tool calling | Planned |
| 11 | Agentic AI with LangGraph | Planned |
| 12 | FastAPI backend | Planned |
| 13 | Testing and monitoring | Planned |
| 14 | Docker and deployment | Planned |
| 15 | FinTech AI assistant | Planned |

## Prerequisites

- Python 3
- Git
- PostgreSQL
- Ollama
- VS Code

## Local Setup

Clone the repository:

```bash
git clone https://github.com/YOUR_USERNAME/local-ai-chatbot.git
cd local-ai-chatbot
```

Create a virtual environment:

```bash
python -m venv .venv
```

Activate on Windows PowerShell:

```powershell
.\.venv\Scripts\Activate.ps1
```

Install dependencies:

```bash
python -m pip install -r requirements.txt
```

Copy `.env.example` to `.env` and update DATABASE_URL
with your local PostgreSQL credentials.

Make sure PostgreSQL and Ollama are running.

Download the model if it is not already installed:

```bash
ollama pull qwen2.5:1.5b
```

Start the chatbot:

```bash
python -m streamlit run app.py
```

Open:

http://localhost:8501

## Security Notes

- Never commit `.env` or passwords.
- Do not upload real payment-card information or confidential customer data.
- Use synthetic data for fintech demonstrations.
- The current application is a learning project, not a production payment system.

## Documentation

See the `docs/` directory for the offline implementation handbook.

## Future Enhancements

- Persistent conversation management
- Streaming LLM responses
- PDF-based RAG
- Vector database integration
- AI tool/function calling
- Agentic AI workflows
- FastAPI backend
- Docker deployment
- FinTech payment operations assistant

## Author

P HARSHA VARDHAN REDDY

## License

This project is currently a learning and portfolio project.
