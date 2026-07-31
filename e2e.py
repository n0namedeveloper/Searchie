import asyncio
import os
from dotenv import load_dotenv

load_dotenv()

from app.agents.search import search_agent

async def main():
    print(f"Base URL: {os.getenv('OPENAI_BASE_URL')}")
    print(f"Model: {os.getenv('SEARCH_MODEL')}")
    print("Running Search Agent (E2E)...")
    try:
        result = await search_agent.run("What are AI agents? Briefly explain in 1 sentence.")
        print("\n=== SUCCESS ===")
        print(result.output)
    except Exception as e:
        print("\n=== FAILED ===")
        print(e)

if __name__ == "__main__":
    asyncio.run(main())
