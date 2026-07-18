"""
This script is used to test the agent for the AI Chatbot by mocking the agent's behavior and checking the response
"""
#Importing necessary libraries
import os
import pytest
from unittest.mock import patch
from fastapi.testclient import TestClient
import main

#Setting up dummy environment variables before any local imports to prevent validation errors in test environments
# Set dummy env vars before any local imports to prevent validation errors in test environments
os.environ.setdefault("GROQ_API_KEY", "test-dummy-key")
os.environ.setdefault("SUPERHERO_API_TOKEN", "test-dummy-token")

#This class is used to test the FastAPI endpoints in main.py
class TestAPI:
    """Tests for the FastAPI endpoints in main.py."""

    @pytest.fixture
    def client(self):        
        with patch("main.init_vector_store"):
            yield TestClient(main.app)

    def test_ask_superman_contains_name(self, client):
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