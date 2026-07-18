"""Tool package exposing all agent tools."""

from tools.superhero_tool import superhero_search
<<<<<<< HEAD
from tools.kb_tool import knowledge_base_search

__all__ = ["superhero_search", "knowledge_base_search"]
=======
from tools.kb_tool import knowledge_base_search, init_vector_store

__all__ = ["superhero_search", "knowledge_base_search", "init_vector_store"]
>>>>>>> 2e14aeff5efbb3b06bd3aa03a9da336262d6b7ef
