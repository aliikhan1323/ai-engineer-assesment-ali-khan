"""RAG indexing - load PDFs, chunk with overlap, embed, and persist FAISS."""
#Importing necessary libraries
from __future__ import annotations
import json
import logging
import os
from pathlib import Path
from langchain_community.document_loaders import PyPDFLoader
from langchain_community.vectorstores import FAISS
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter

#Loggers
logger = logging.getLogger(__name__)

#Setting up the data directory
DATA_DIR = Path(__file__).resolve().parent / "data"
#Setting up the cache path
CACHE_PATH = DATA_DIR / "faiss_index"
FINGERPRINT_PATH = CACHE_PATH / "fingerprint.json"

#Setting up the chunk size and the chunk overlap
CHUNK_SIZE = 500
CHUNK_OVERLAP = 100

_vector_store: FAISS | None = None

#This function is used to build a fingerprint of the PDF documents
def _pdf_fingerprint(pdf_files: list[Path]) -> dict:
    """Build a fingerprint of PDF names, mtimes, and sizes for cache invalidation."""
    entries = []
    for path in pdf_files:
        stat = path.stat()
        entries.append(
            {
                "name": path.name,
                "mtime": stat.st_mtime,
                "size": stat.st_size,
            }
        )
    return {
        "chunk_size": CHUNK_SIZE,
        "chunk_overlap": CHUNK_OVERLAP,
        "pdfs": entries,
    }

#This function is used to check if the fingerprint of the PDF documents matches the stored fingerprint
def _fingerprint_matches(pdf_files: list[Path]) -> bool:
    if not FINGERPRINT_PATH.exists():
        return False
    try:
        stored = json.loads(FINGERPRINT_PATH.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return False
    return stored == _pdf_fingerprint(pdf_files)

#This function is used to save the fingerprint of the PDF documents
def _save_fingerprint(pdf_files: list[Path]) -> None:
    CACHE_PATH.mkdir(parents=True, exist_ok=True)
    FINGERPRINT_PATH.write_text(
        json.dumps(_pdf_fingerprint(pdf_files), indent=2),
        encoding="utf-8",
    )

#This function is used to get the embeddings for the PDF documents
def _get_embeddings() -> GoogleGenerativeAIEmbeddings:
    return GoogleGenerativeAIEmbeddings(
        model="models/gemini-embedding-001",
        google_api_key=os.getenv("GEMINI_API_KEY"),
    )

#This function is used to load and chunk the PDF documents
def _load_and_chunk_pdfs(pdf_files: list[Path]) -> list:
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=CHUNK_SIZE,
        chunk_overlap=CHUNK_OVERLAP,
    )
    documents = []
    for pdf_path in pdf_files:
        loader = PyPDFLoader(str(pdf_path))
        pages = loader.load()
        for page in pages:
            page.metadata["source_file"] = pdf_path.name
        chunks = splitter.split_documents(pages)
        documents.extend(chunks)
        logger.info(
            "  %s → %d pages → %d chunks",
            pdf_path.name,
            len(pages),
            len(chunks),
        )
    return documents

#This function is used to initialise the vector store
def init_vector_store(persist: bool = True) -> None:
    """Load PDFs from data/, chunk, embed, and build (or load) a FAISS store.
    Called once at application startup. Uses a disk cache when present and
    still valid for the current PDF set / chunk settings.
    """
    global _vector_store

    embeddings = _get_embeddings()
    pdf_files = sorted(DATA_DIR.glob("*.pdf"))

    if persist and CACHE_PATH.exists() and _fingerprint_matches(pdf_files):
        logger.info("Loading FAISS index from cache at %s", CACHE_PATH)
        _vector_store = FAISS.load_local(
            str(CACHE_PATH), embeddings, allow_dangerous_deserialization=True
        )
        return

    if not pdf_files:
        logger.warning("No PDF files found in %s", DATA_DIR)
        _vector_store = None
        return

    logger.info("Indexing %d PDF(s) from %s", len(pdf_files), DATA_DIR)
    documents = _load_and_chunk_pdfs(pdf_files)
    if not documents:
        logger.warning("No text chunks produced from PDFs in %s", DATA_DIR)
        _vector_store = None
        return

    _vector_store = FAISS.from_documents(documents, embeddings)

    if persist:
        _vector_store.save_local(str(CACHE_PATH))
        _save_fingerprint(pdf_files)

    logger.info("Vector store ready with %d chunks", len(documents))

#This function is used to return the initialised vector store
def get_vector_store():
    """Return the initialised vector store (or None)."""
    return _vector_store
