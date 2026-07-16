"""LangChain agent – binds tools to the Groq LLM using create_agent (LangChain 1.x)."""

import logging
import os

from dotenv import load_dotenv
load_dotenv()

from langchain.agents import create_agent
from langchain_core.messages import AIMessage, ToolMessage
from langchain_groq import ChatGroq

from tools import superhero_search, knowledge_base_search

logger = logging.getLogger(__name__)

SYSTEM_PROMPT = """You are a helpful assistant that answers user questions using
two information sources:

1. **Superhero API** – for anything about comic-book superheroes (powers, stats,
   biography, appearance, connections).  Use the `superhero_search` tool.
2. **Knowledge Base** – a collection of PDF documents.  Use the
   `knowledge_base_search` tool for any non-superhero topic.

Rules:
- Decide which source(s) to use based on the question.  You may call both tools
  if the question spans superhero and non-superhero topics.
- **Always cite your sources** in every answer.  Mention whether information
  came from the Superhero API, the Knowledge Base (include file name and page
  number), or both.
- If a tool returns no results, say so honestly rather than making things up.
- Keep answers concise and accurate.
"""

MODEL_NAME = os.getenv("GROQ_MODEL", "llama-3.3-70b-versatile")
llm = ChatGroq(model=MODEL_NAME, temperature=0, max_retries=5, timeout=60)

tools = [superhero_search, knowledge_base_search]

_tool_source_map = {
    "superhero_search": "Superhero API",
    "knowledge_base_search": "Knowledge Base (PDF documents)",
}

agent = create_agent(
    model=llm,
    tools=tools,
    system_prompt=SYSTEM_PROMPT,
)


def ask(question: str) -> dict:
    """Run the agent and return the answer + extracted sources."""
    try:
        result = agent.invoke({"messages": [{"role": "user", "content": question}]})
    except Exception as exc:
        logger.exception("Agent invocation failed")
        return {
            "answer": f"Sorry, the agent failed to answer: {exc}",
            "sources": ["error"],
        }

    messages = result.get("messages", [])

    sources = set()
    for msg in messages:
        if isinstance(msg, ToolMessage) and msg.name in _tool_source_map:
            sources.add(_tool_source_map[msg.name])

    answer = ""
    for msg in reversed(messages):
        if isinstance(msg, AIMessage) and msg.content and not msg.tool_calls:
            answer = msg.content
            break
    if not answer and messages:
        answer = messages[-1].content

    return {
        "answer": answer if isinstance(answer, str) else str(answer),
        "sources": sorted(sources) if sources else ["LLM (no tools used)"],
    }