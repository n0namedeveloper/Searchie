from pydantic_ai import Agent
from pydantic import BaseModel
from typing import List

from app.agents.model import get_model


class Verification(BaseModel):
    claim: str
    is_accurate: bool
    reasoning: str


class FactCheckResult(BaseModel):
    verifications: List[Verification]
    overall_score: float


fact_check_agent = Agent(
    get_model(),
    output_type=FactCheckResult,
    defer_model_check=True,
    system_prompt=(
        "You are a Fact-check Agent. Given a drafted report and the original facts/raw data, "
        "verify the claims made in the report. Highlight any inaccuracies."
    ),
)
