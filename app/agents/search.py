from pydantic_ai import Agent, RunContext
from pydantic import BaseModel
from typing import List
import httpx
from bs4 import BeautifulSoup
from duckduckgo_search import DDGS
import asyncio

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
        "You are a Web Search Agent. Given a research topic, your job is to gather real facts.\n"
        "1. Formulate a search query based on the topic.\n"
        "2. Use the `search_and_scrape` tool to search the web and scrape the top results.\n"
        "3. Combine the scraped information into a detailed `raw_content` report.\n"
        "4. You MUST include the actual Source URLs (returned by the tool) in your `raw_content` so downstream agents can cite them."
    ),
)

@search_agent.tool
async def search_and_scrape(ctx: RunContext[None], query: str, max_results: int = 3) -> str:
    """Search DuckDuckGo and scrape the text content of the top URLs."""
    try:
        # DDGS.text is synchronous, run in thread to not block event loop
        results = await asyncio.to_thread(DDGS().text, query, max_results=max_results)

        
        scraped_data = []
        async with httpx.AsyncClient(timeout=10.0, follow_redirects=True) as client:
            for r in results:
                url = r.get("href")
                title = r.get("title")
                snippet = r.get("body")
                
                if not url: continue
                
                try:
                    resp = await client.get(url)
                    resp.raise_for_status()
                    soup = BeautifulSoup(resp.content, "html.parser")
                    
                    # Remove scripts, styles
                    for script in soup(["script", "style", "nav", "footer", "header", "noscript"]):
                        script.extract()
                        
                    text = soup.get_text(separator=" ", strip=True)
                    text = text.encode("ascii", "ignore").decode("ascii") # sanitize
                    text = text[:1000] # Limit size per page to avoid huge tool messages
                    scraped_data.append(f"Source URL: {url}\nTitle: {title}\nContent:\n{text}\n")
                except Exception as e:
                    # Fallback to snippet if scraping fails
                    snippet_safe = snippet.encode("ascii", "ignore").decode("ascii") if snippet else ""
                    scraped_data.append(f"Source URL: {url}\nTitle: {title}\nSnippet:\n{snippet_safe}\n")
                    
        return "\n\n---\n\n".join(scraped_data)
    except Exception as e:
        return f"Search failed: {str(e)}"
