from dotenv import load_dotenv
load_dotenv()

from fastapi import FastAPI, HTTPException, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from app.schemas import JobRequest, JobResponse
import uuid
import logging
from app.state import StateManager

# Import agents for local worker execution
from app.agents.search import search_agent
from app.agents.extract import extract_agent
from app.agents.synthesis import synthesis_agent
from app.agents.fact_check import fact_check_agent

logger = logging.getLogger(__name__)

state_manager = StateManager()

app = FastAPI(title="Searchie API", version="0.1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


async def run_research_pipeline(job_id: str, topic: str, depth: str = "standard", model=None):
    try:
        logger.info(f"Starting research pipeline for job_id={job_id}, topic={topic}")
        
        # 1. Search
        await state_manager.save_job_state(job_id, {"status": "running", "step": "search", "topic": topic})
        search_res = await search_agent.run(f"Topic: {topic}, Depth: {depth}", model=model)
        
        # 2. Extract
        await state_manager.save_job_state(job_id, {"status": "running", "step": "extract", "topic": topic})
        extract_res = await extract_agent.run(search_res.output.raw_content, model=model)
        
        # 3. Synthesis
        await state_manager.save_job_state(job_id, {"status": "running", "step": "synthesis", "topic": topic})
        facts_text = "\n".join([f"- {f.claim} (Source: {f.source_context})" for f in extract_res.output.facts])
        synth_res = await synthesis_agent.run(facts_text, model=model)
        
        # 4. Fact Check
        await state_manager.save_job_state(job_id, {"status": "running", "step": "fact_check", "topic": topic})
        fact_check_res = await fact_check_agent.run(f"Report: {synth_res.output}\nFacts: {facts_text}", model=model)
        
        result = {
            "report": synth_res.output,
            "fact_check_score": fact_check_res.output.overall_score,
            "verifications": [v.model_dump() for v in fact_check_res.output.verifications]
        }
        
        await state_manager.save_job_state(job_id, {"status": "completed", "result": result, "topic": topic})
    except Exception as e:
        logger.error(f"Job {job_id} failed: {e}")
        await state_manager.save_job_state(job_id, {"status": "error", "error": str(e), "topic": topic})


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/api/v1/jobs", response_model=JobResponse)
async def submit_job(request: JobRequest, bg_tasks: BackgroundTasks):
    job_id = str(uuid.uuid4())
    await state_manager.save_job_state(
        job_id, {"status": "queued", "topic": request.topic}
    )
    # Run in background without Redis
    bg_tasks.add_task(run_research_pipeline, job_id, request.topic, request.depth)
    return JobResponse(job_id=job_id, status="queued")


@app.get("/api/v1/jobs/{job_id}")
async def get_job_status(job_id: str):
    job = await state_manager.get_job_state(job_id)
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")
    return job
