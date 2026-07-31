import pytest
from app.worker import run_research_pipeline
import fakeredis.aioredis
from app.state import StateManager
from pydantic_ai.models.test import TestModel

@pytest.mark.asyncio
async def test_run_research_pipeline():
    # Mock state manager
    mock_state_manager = StateManager()
    mock_state_manager.redis = fakeredis.aioredis.FakeRedis(decode_responses=True)
    
    ctx = {"state_manager": mock_state_manager}
    job_id = "job-123"
    
    # Pass TestModel to prevent actual API calls
    model = TestModel()
    
    result = await run_research_pipeline(ctx, job_id, "AI Agents", "standard", model=model)
    
    assert result["status"] == "completed"
    state = await mock_state_manager.get_job_state(job_id)
    assert state["status"] == "completed"
    assert "report" in state["result"]
