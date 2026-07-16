"""Pydantic schemas for request/response models and structured agent output."""

from pydantic import BaseModel, Field


class QuestionRequest(BaseModel):
    """Incoming question from the user."""

    question: str = Field(..., min_length=1, max_length=500)


class AgentAnswer(BaseModel):
    """Structured response from the agent containing the answer and its sources.

    Used both as the ``response_format`` for ``create_agent`` (so the LLM is
    forced to return a structured tool call with these fields) and as the
    FastAPI response model.
    """

    answer: str = Field(description="The answer to the user's question")
    sources: list[str] = Field(
        default_factory=list,
        description=(
            "Sources cited in the answer.  Use 'Superhero API' for superhero "
            "data, 'Knowledge Base (PDF documents)' for knowledge-base data.  "
            "Leave empty if no tools were used."
        ),
    )