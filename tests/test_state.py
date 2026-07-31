import pytest
import fakeredis.aioredis
from app.state import StateManager

@pytest.fixture
def state_manager():
    manager = StateManager()
    manager.redis = fakeredis.aioredis.FakeRedis(decode_responses=True)
    return manager

@pytest.mark.asyncio
async def test_save_and_get_job_state(state_manager):
    job_id = "test-job-123"
    state = {"status": "running", "step": "search"}
    
    await state_manager.save_job_state(job_id, state)
    
    retrieved_state = await state_manager.get_job_state(job_id)
    assert retrieved_state == state

@pytest.mark.asyncio
async def test_get_nonexistent_job(state_manager):
    state = await state_manager.get_job_state("nonexistent")
    assert state is None
