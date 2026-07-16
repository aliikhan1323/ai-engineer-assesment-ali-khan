import os
# Set dummy env vars before any local imports to prevent validation errors in test environments
os.environ.setdefault("GROQ_API_KEY", "test-dummy-key")
os.environ.setdefault("SUPERHERO_API_TOKEN", "test-dummy-token")

import pytest
from unittest.mock import patch

class TestAPI:
    """Tests for the FastAPI endpoints in main.py."""

    @pytest.fixture
    def client(self):
        from fastapi.testclient import TestClient
        import main
        with patch("tools.kb_tool.init_vector_store"):
            yield TestClient(main.app)

    def test_ask_superman_contains_name(self, client):
        import main
        with patch.object(
            main.agent_module, "ask",
            return_value={
                "answer": "Superman is a fictional superhero appearing in American comic books published by DC Comics.",
                "sources": ["Superhero API"]
            },
        ):
            response = client.post("/ask", json={"question": "Tell me about Superman"})

        assert response.status_code == 200
        body = response.json()
        assert "superman" in body["answer"].lower()
        assert "Superhero API" in body["sources"]

    def test_ask_ai_contains_ai_and_kb_source(self, client):
        import main
        with patch.object(
            main.agent_module, "ask",
            return_value={
                "answer": "AI refers to the simulation of human intelligence in machines.",
                "sources": ["Knowledge Base (PDF documents)"]
            },
        ):
            response = client.post("/ask", json={"question": "What is AI?"})

        assert response.status_code == 200
        body = response.json()
        assert "ai" in body["answer"].lower()
        assert "Knowledge Base (PDF documents)" in body["sources"]