from pydantic_ai import Agent
from pydantic import BaseModel
from typing import List

from app.agents.model import get_model
from app.config import settings


class SearchResult(BaseModel):
    queries_used: List[str]
    raw_content: str


search_agent = Agent(
    get_model(settings.search_model),
    output_type=SearchResult,
    defer_model_check=True,
    system_prompt=(
        "You are a Search Agent. Given a research topic, formulate search queries "
        "and return the compiled raw content from your findings.\n"
        "CRITICAL: Since this is a mock environment, you MUST invent or provide valid, DEEP URL links "
        "(with specific article paths, not just root domains) for all your sources in the raw content "
        "so downstream agents can extract them. (e.g. Source: https://en.wikipedia.org/wiki/Artificial_intelligence_agent "
        "or https://techcrunch.com/2024/01/01/ai-agents-explained/)"
    ),
)
