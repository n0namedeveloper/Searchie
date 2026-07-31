"""Shared model factory for all agents.

Creates a single OpenAIChatModel instance configured for the DigitalOcean
AI Gateway, with the HTTPX transport patch applied to strip unsupported
request parameters (response_format, strict, etc.).
"""
import os
from pydantic_ai.models.openai import OpenAIChatModel
from pydantic_ai.providers.openai import OpenAIProvider
from app.do_patch import get_patched_openai_client
from app.config import settings

_client = get_patched_openai_client(
    api_key=settings.digital_ocean_key or os.getenv("OPENAI_API_KEY", ""),
    base_url=os.getenv("OPENAI_BASE_URL", "https://inference.do-ai.run/v1"),
)

_provider = OpenAIProvider(openai_client=_client)


def get_model(model_name: str | None = None) -> OpenAIChatModel:
    """Return an OpenAIChatModel wired through the DO-patched provider."""
    name = model_name or settings.llm_model
    return OpenAIChatModel(name, provider=_provider)
