<<<<<<< HEAD
"""Knowledge-base tool — similarity search over the pre-built RAG index."""
#Importing necessary libraries
import logging
from langchain_core.tools import tool
from rag import get_vector_store

#Loggers
logger = logging.getLogger(__name__)

#This function is used to search the knowledge base for information relevant to a user query
=======
"""Knowledge-base tool – loads PDFs and provides similarity-search retrieval."""

import logging
import os
from pathlib import Path

from langchain_core.tools import tool

logger = logging.getLogger(__name__)

_vector_store = None  # module-level singleton

DATA_DIR = Path(__file__).resolve().parent.parent / "data"


def init_vector_store(persist: bool = True) -> None:
    """Load every PDF in data/ and build (or load) a FAISS vector store.

    Called once at application startup.
    """
    global _vector_store

    from langchain_community.document_loaders import PyPDFLoader
    from langchain_google_genai import GoogleGenerativeAIEmbeddings
    from langchain_community.vectorstores import FAISS

    embeddings = GoogleGenerativeAIEmbeddings(
        model="models/gemini-embedding-001",
        google_api_key=os.getenv("GEMINI_API_KEY"),
    )

    cache_path = DATA_DIR / "faiss_index"

    if persist and cache_path.exists():
        logger.info("Loading FAISS index from cache at %s", cache_path)
        _vector_store = FAISS.load_local(
            str(cache_path), embeddings, allow_dangerous_deserialization=True
        )
        return

    pdf_files = sorted(DATA_DIR.glob("*.pdf"))
    if not pdf_files:
        logger.warning("No PDF files found in %s", DATA_DIR)
        _vector_store = None
        return

    logger.info("Loading %d PDF(s) from %s", len(pdf_files), DATA_DIR)

    documents = []
    for pdf_path in pdf_files:
        loader = PyPDFLoader(str(pdf_path))
        docs = loader.load()
        for d in docs:
            d.metadata["source_file"] = pdf_path.name
        documents.extend(docs)
        logger.info("  %s → %d pages", pdf_path.name, len(docs))

    _vector_store = FAISS.from_documents(documents, embeddings)

    if persist:
        _vector_store.save_local(str(cache_path))

    logger.info("Vector store ready with %d chunks", len(documents))


def get_vector_store():
    """Return the initialised vector store (or None)."""
    return _vector_store


>>>>>>> 2e14aeff5efbb3b06bd3aa03a9da336262d6b7ef
@tool
def knowledge_base_search(query: str) -> str:
    """Search the knowledge base (PDF documents) for information relevant
    to a natural-language query.  Use this tool when the user asks about
    topics covered in the document collection — technology, science,
    history, general reference, etc.  Do NOT use this for questions about
    comic-book superheroes; those belong to the superhero_search tool.
    """

    store = get_vector_store()
    if store is None:
        return (
            "Knowledge base is empty or not initialised. "
            "Place PDF files in the data/ directory."
        )

    results = store.similarity_search_with_relevance_scores(query, k=3)

    if not results:
        return "No relevant documents found in the knowledge base."

    lines = ["[Source: Knowledge Base (PDF documents in data/)]"]

    logger.info("Starting to process query knowledge")
    logger.info("Query: %s", query)
    logger.info("Results: %s", results)
<<<<<<< HEAD

=======
    
>>>>>>> 2e14aeff5efbb3b06bd3aa03a9da336262d6b7ef
    for doc, score in results:
        source = doc.metadata.get("source_file", "unknown")
        page = doc.metadata.get("page", "?")
        snippet = doc.page_content.strip().replace("\n", " ")[:500]
        lines.append(f"\n[{source}, page {page}, relevance {score:.2f}]")
        lines.append(snippet)

<<<<<<< HEAD
    return "\n".join(lines)
=======
    return "\n".join(lines)
>>>>>>> 2e14aeff5efbb3b06bd3aa03a9da336262d6b7ef
