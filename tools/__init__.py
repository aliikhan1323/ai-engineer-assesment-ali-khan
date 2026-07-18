"""Tool package exposing all agent tools."""

from tools.superhero_tool import superhero_search
from tools.kb_tool import knowledge_base_search

__all__ = ["superhero_search", "knowledge_base_search"]
