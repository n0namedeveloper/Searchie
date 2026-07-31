import pytest
from app.agents.search import search_agent, SearchResult
from app.agents.extract import extract_agent, ExtractionResult
from app.agents.synthesis import synthesis_agent
from app.agents.fact_check import fact_check_agent, FactCheckResult
from pydantic_ai.models.test import TestModel

@pytest.mark.asyncio
async def test_search_agent():
    model = TestModel()
    result = await search_agent.run("Topic: AI Agents", model=model)
    assert isinstance(result.output, SearchResult)

@pytest.mark.asyncio
async def test_extract_agent():
    model = TestModel()
    result = await extract_agent.run("Raw text here.", model=model)
    assert isinstance(result.output, ExtractionResult)

@pytest.mark.asyncio
async def test_synthesis_agent():
    model = TestModel()
    result = await synthesis_agent.run("Fact 1, Fact 2", model=model)
    assert isinstance(result.output, str)

@pytest.mark.asyncio
async def test_fact_check_agent():
    model = TestModel()
    result = await fact_check_agent.run("Report text here. Facts here.", model=model)
    assert isinstance(result.output, FactCheckResult)
