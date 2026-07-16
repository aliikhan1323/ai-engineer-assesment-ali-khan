"""FastAPI app – exposes POST /ask endpoint."""

import logging
from contextlib import asynccontextmanager

from dotenv import load_dotenv
load_dotenv()

from fastapi import FastAPI

import agent as agent_module
from tools.kb_tool import init_vector_store
from schemas import AgentAnswer, QuestionRequest

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
)
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Initialising knowledge base…")
    init_vector_store()
    logger.info("Startup complete.  POST /ask ready.")
    yield
    logger.info("Shutting down.")


app = FastAPI(title="AI Engineer Assessment Chatbot", lifespan=lifespan)


@app.post("/ask", response_model=AgentAnswer)
async def ask_endpoint(req: QuestionRequest) -> AgentAnswer:
    try:
        result = agent_module.ask(req.question)
    except Exception as exc:
        logger.exception("Agent failed")
        return AgentAnswer(
            answer=f"Sorry, something went wrong: {exc}",
            sources=["error"],
        )
    return AgentAnswer(**result)


@app.get("/health")
async def health():
    return {"status": "ok"}