"""Superhero API tool – queries the Superhero API for character data."""

import os
import httpx
from langchain_core.tools import tool
import logging

logger = logging.getLogger(__name__)


@tool
def superhero_search(name: str) -> str:
    """Search for superhero information by name.
    Use this tool when the user asks about a superhero's powers,
    stats, biography, appearance, work, or connections.
    Provide the superhero's name (e.g. "Batman", "Superman").
    """

    token = os.getenv("SUPERHERO_API_TOKEN")
    if not token:
        logger.error("Superhero API token is not configured. Set SUPERHERO_API_TOKEN in .env to use this tool.")
        return (
            "Superhero API token is not configured. "
            "Set SUPERHERO_API_TOKEN in .env to use this tool."
        )

    url = f"https://superheroapi.com/api/{token}/search/{name}"

    try:
        response = httpx.get(url, timeout=10, follow_redirects=True)
        response.raise_for_status()
    except httpx.HTTPError as exc:
        return f"Superhero API request failed: {exc}"
    except httpx.RequestError as exc:
        return f"Could not reach Superhero API: {exc}"

    data = response.json()

    if data.get("response") == "error":
        return f"Superhero API error: {data.get('error', 'unknown error')}"

    results = data.get("results", [])
    if not results:
        return f"No superheroes found matching '{name}'."

    logger.info("Starting to process query superhero")
    logger.info("Query: %s", name)
    logger.info("Results: %s", results)
    logger.info("********************")

    return str(results)