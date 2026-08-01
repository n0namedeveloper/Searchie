from dotenv import load_dotenv
load_dotenv()

from fastapi import FastAPI, HTTPException, Request, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from sse_starlette.sse import EventSourceResponse
from app.schemas import JobRequest, JobResponse
import uuid
import logging
import json
import asyncio
from app.state import StateManager
from app.pubsub import bus
from app.pipeline import run_research_pipeline

logger = logging.getLogger(__name__)

state_manager = StateManager()

app = FastAPI(title="Searchie API", version="0.2.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
async def startup():
    await state_manager.init_db()

@app.get("/health")
def health():
    return {"status": "ok"}

@app.post("/api/v1/jobs", response_model=JobResponse)
async def submit_job(request: JobRequest, bg_tasks: BackgroundTasks):
    job_id = str(uuid.uuid4())
    await state_manager.save_job_state(job_id, {"status": "queued", "topic": request.topic, "depth": request.depth})
    bg_tasks.add_task(run_research_pipeline, job_id, request.topic, request.depth, state_manager)
    return JobResponse(job_id=job_id, status="queued")

@app.get("/api/v1/jobs/{job_id}")
async def get_job_status(job_id: str):
    job = await state_manager.get_job_state(job_id)
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")
    return job

@app.get("/api/v1/jobs/{job_id}/stream")
async def job_stream(job_id: str, request: Request):
    async def event_generator():
        q = bus.subscribe(f"job:{job_id}")
        
        # Send initial state
        job = await state_manager.get_job_state(job_id)
        if job:
            yield {"event": "init", "data": json.dumps(job)}
            if job.get("status") in ["completed", "error"]:
                bus.unsubscribe(f"job:{job_id}", q)
                return

        try:
            while True:
                if await request.is_disconnected():
                    break
                
                try:
                    message = await asyncio.wait_for(q.get(), timeout=1.0)
                    data = json.loads(message)
                    yield {"event": data["event"], "data": json.dumps(data["data"])}
                    if data["event"] in ["completed", "error"]:
                        break
                except asyncio.TimeoutError:
                    continue
        finally:
            bus.unsubscribe(f"job:{job_id}", q)

    return EventSourceResponse(event_generator())
