"""Knowledge-base tool — similarity search over the pre-built RAG index."""
#Importing necessary libraries
import logging
from langchain_core.tools import tool
from rag import get_vector_store

#Loggers
logger = logging.getLogger(__name__)

#This function is used to search the knowledge base for information relevant to a user query
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

    for doc, score in results:
        source = doc.metadata.get("source_file", "unknown")
        page = doc.metadata.get("page", "?")
        snippet = doc.page_content.strip().replace("\n", " ")[:500]
        lines.append(f"\n[{source}, page {page}, relevance {score:.2f}]")
        lines.append(snippet)

    return "\n".join(lines)
