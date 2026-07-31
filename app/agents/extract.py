from pydantic_ai import Agent
from pydantic import BaseModel
from typing import List

from app.agents.model import get_model


class Fact(BaseModel):
    claim: str
    source_context: str


class ExtractionResult(BaseModel):
    facts: List[Fact]


extract_agent = Agent(
    get_model(),
    output_type=ExtractionResult,
    defer_model_check=True,
    system_prompt=(
        "You are an Extract Agent. Given raw content from searches, extract key factual "
        "claims and their context. Do not synthesize or summarize, just extract facts."
    ),
)
