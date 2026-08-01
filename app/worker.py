import asyncio
import logging
from arq import Worker
from arq.connections import RedisSettings
from app.state import StateManager
import redis.asyncio as redis
import json

from app.agents.search import search_agent
from app.agents.extract import extract_agent
from app.agents.synthesis import synthesis_agent
from app.agents.fact_check import fact_check_agent
from app.models import Base
from app.state import engine

logger = logging.getLogger(__name__)

async def startup(ctx):
    logger.info("Worker starting up...")
    ctx['state_manager'] = StateManager()
    ctx['redis'] = redis.from_url("redis://localhost:6379/0", decode_responses=True)
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

async def shutdown(ctx):
    logger.info("Worker shutting down...")
    await ctx['redis'].close()

async def run_research_pipeline(ctx, job_id: str, topic: str, depth: str = "standard"):
    state_manager: StateManager = ctx['state_manager']
    redis_client = ctx['redis']
    
    async def publish(event, data):
        await redis_client.publish(f"job:{job_id}", json.dumps({"event": event, "data": data}))

    try:
        logger.info(f"Starting research pipeline for job_id={job_id}, topic={topic}")
        
        # 1. Search
        await state_manager.save_job_state(job_id, {"status": "running", "step": "search", "topic": topic})
        await publish("step", "search")
        search_res = await search_agent.run(f"Topic: {topic}, Depth: {depth}")
        
        # 2. Extract
        await state_manager.save_job_state(job_id, {"status": "running", "step": "extract", "topic": topic})
        await publish("step", "extract")
        extract_res = await extract_agent.run(search_res.output.raw_content)
        
        # 3. Synthesis (Streaming)
        await state_manager.save_job_state(job_id, {"status": "running", "step": "synthesis", "topic": topic})
        await publish("step", "synthesis")
        facts_text = "\n".join([f"- {f.claim} (Source: {f.source_context})" for f in extract_res.output.facts])
        
        full_report = ""
        async with synthesis_agent.run_stream(facts_text) as synth_stream:
            async for chunk in synth_stream.stream_text(delta=True):
                full_report += chunk
                await publish("stream", chunk)
        
        # 4. Fact Check
        await state_manager.save_job_state(job_id, {"status": "running", "step": "fact_check", "topic": topic})
        await publish("step", "fact_check")
        fact_check_res = await fact_check_agent.run(f"Report: {full_report}\nFacts: {facts_text}")
        
        result = {
            "report": full_report,
            "fact_check_score": fact_check_res.output.overall_score,
            "verifications": [v.model_dump() for v in fact_check_res.output.verifications]
        }
        
        await state_manager.save_job_state(job_id, {"status": "completed", "result": result, "topic": topic})
        await publish("completed", result)
    except Exception as e:
        logger.error(f"Job {job_id} failed: {e}")
        await state_manager.save_job_state(job_id, {"status": "error", "error": str(e), "topic": topic})
        await publish("error", str(e))

class WorkerSettings:
    functions = [run_research_pipeline]
    on_startup = startup
    on_shutdown = shutdown
    redis_settings = RedisSettings()
