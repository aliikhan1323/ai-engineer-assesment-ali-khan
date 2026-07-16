# AI Engineer Assessment — FastAPI Chatbot

A FastAPI chatbot that answers questions from two sources — a **Superhero API** and a **PDF knowledge base** — using a LangChain agent backed by the **Groq** LLM. The agent decides which source(s) to consult based on the question.

## What it does

- **`POST /ask`** accepts `{"question": "…"}` and returns `{"answer": "…", "sources": [...]}`.
- The agent has two tools:
  1. `superhero_search` — queries the [Superhero API](https://superheroapi.com) for character data.
  2. `knowledge_base_search` — performs similarity search over PDFs in `data/` using FAISS + Google Gemini `gemini-embedding-001` embeddings.
- Every response includes where the information came from (tool names extracted from the agent's intermediate steps).

## Project structure

```
main.py              FastAPI app (POST /ask, /health)
schemas.py           Pydantic schemas (QuestionRequest, AgentAnswer)
agent.py             LangChain agent — binds tools to ChatGroq
app.py               Streamlit frontend chatbot interface (ChatGPT UI)
run.py               Startup script to run backend and frontend concurrently
tools/
  superhero_tool.py  Superhero API tool
  kb_tool.py         PDF loading + FAISS retrieval tool
data/                PDF knowledge base (sample included)
scripts/             Helper to (re)generate sample PDF
tests/               Unit tests (all mocked, no API keys needed)
```

## Setup

```bash
git clone https://github.com/<you>/ai-engineer-assessment-ali-khan.git
cd ai-engineer-assessment-ali-khan

python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate

pip install -r requirements.txt

cp .env.example .env
# Fill in GROQ_API_KEY (https://console.groq.com),
#       SUPERHERO_API_TOKEN (https://superheroapi.com → GitHub sign-in), and
#       GEMINI_API_KEY (https://aistudio.google.com/apikey)
```

A sample PDF (`data/intro_to_ai.pdf`) is included. To regenerate it:

```bash
python scripts/create_sample_pdf.py
```

## Run

To start both the FastAPI backend and Streamlit frontend concurrently:

```bash
python run.py
```

Otherwise, to start them manually in separate terminals:

### 1. Start the FastAPI Backend
```bash
uvicorn main:app --reload
```

### 2. Start the Streamlit Frontend
```bash
streamlit run app.py
```

### Example

```bash
curl -X POST http://localhost:8000/ask \
  -H "Content-Type: application/json" \
  -d '{"question": "What are Batman power stats and what is deep learning?"}'
```

```json
{
  "answer": "Batman has intelligence 100, strength 18… [Superhero API]…",
  "sources": ["Knowledge Base (PDF documents)", "Superhero API"]
}
```

## Tests

```bash
pytest tests/ -v
```

All tests are fully mocked — no API keys or LLM calls required.

## Decisions & tradeoffs

- **Groq + `llama-3.3-70b-versatile`** — Groq is free (email signup) and supports native tool-calling.
- **FAISS + Google Gemini `gemini-embedding-001` embeddings** — cloud-based via `GEMINI_API_KEY` for higher quality semantic retrieval.
- **FAISS Disk Caching** — Vector store is persisted on disk (`data/faiss_index`) on first run and loaded from cache on subsequent startups to optimize loading time.
- **`create_agent`** — LangChain agent harness using native LLM tool-calling.
- **Source attribution** — sources are dynamically extracted from the actual `ToolMessage` calls in the message history.
- **Error handling** — wrapped agent invocation in a `try/except` safety block returning a user-friendly sorry message on failure; tool-level HTTP error handling; basic validation via Pydantic.
- **Streamlit Frontend** — A dark-themed, ChatGPT-like conversation UI communicating with the backend.
- **Corners cut** — no rate-limiting on the API endpoint; `max_iterations=5` as a safeguard.