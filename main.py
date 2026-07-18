"""FastAPI app - exposes POST /ask endpoint."""
#Importing necessary libraries
import logging
from contextlib import asynccontextmanager
from dotenv import load_dotenv
from fastapi import FastAPI
import agent as agent_module
from rag import init_vector_store
from schemas import AgentAnswer, QuestionRequest

#Loading environment variables
load_dotenv()

#Setting up logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
)
logger = logging.getLogger(__name__)

#Setting up lifespan for the app
@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Initialising knowledge base…")
    init_vector_store()
    logger.info("Startup complete.  POST /ask ready.")
    yield
    logger.info("Shutting down.")

#Setting up the FastAPI app
app = FastAPI(title="AI Engineer Assessment Chatbot", lifespan=lifespan)

#Setting up the /ask endpoint which will be used to ask questions to the agent
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

#Setting up the /health endpoint which will be used to check the health of the app
@app.get("/health")
async def health():
    return {"status": "ok"}