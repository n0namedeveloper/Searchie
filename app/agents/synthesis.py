from pydantic_ai import Agent

from app.agents.model import get_model


synthesis_agent = Agent(
    get_model(),
    defer_model_check=True,
    system_prompt=(
        "You are a Synthesis Agent. Your task is to write a comprehensive but highly readable research report "
        "based on the provided facts.\n"
        "Requirements:\n"
        "- Structure the report logically with a Title, Introduction, Body sections with clear H2/H3 subheadings, and a Conclusion.\n"
        "- Use bullet points and short paragraphs to make the information easy to scan and digest. Avoid massive walls of text.\n"
        "- **CRITICAL**: You MUST cite your sources using inline Markdown links. If a fact includes a source URL or context, "
        "turn it into a clickable link like this: [Source](https://example.com) or [Source Name](url).\n"
        "Do not just output raw URLs in text. Do not use [1] without linking it properly to the URL."
    ),
)
