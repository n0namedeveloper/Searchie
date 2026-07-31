import pytest
from httpx import AsyncClient, ASGITransport
from app.main import app

@pytest.mark.asyncio
async def test_submit_job():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        response = await ac.post("/api/v1/jobs", json={"topic": "AI Agents", "depth": "standard"})
    assert response.status_code == 200
    data = response.json()
    assert "job_id" in data
    assert data["status"] == "queued"

@pytest.mark.asyncio
async def test_get_job_status():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        # submit a job first
        response = await ac.post("/api/v1/jobs", json={"topic": "AI Agents"})
        assert response.status_code == 200
        job_id = response.json()["job_id"]
        
        # poll status
        status_response = await ac.get(f"/api/v1/jobs/{job_id}")
    
    assert status_response.status_code == 200
    data = status_response.json()
    assert data["job_id"] == job_id
    assert "status" in data
