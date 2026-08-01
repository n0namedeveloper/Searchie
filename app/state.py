from typing import Dict, Any, Optional
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from app.models import Base, Job

# Local SQLite DB
DATABASE_URL = "sqlite+aiosqlite:///./searchie.db"
engine = create_async_engine(DATABASE_URL, echo=False)
async_session = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

class StateManager:
    async def init_db(self):
        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)

    async def save_job_state(self, job_id: str, state: Dict[str, Any]):
        async with async_session() as session:
            job = await session.get(Job, job_id)
            if not job:
                job = Job(id=job_id)
                session.add(job)
            
            # Update fields dynamically
            if "topic" in state: job.topic = state["topic"]
            if "depth" in state: job.depth = state["depth"]
            if "status" in state: job.status = state["status"]
            if "step" in state: job.step = state["step"]
            if "error" in state: job.error = state["error"]
            if "result" in state: job.result = state["result"]
            
            await session.commit()

    async def get_job_state(self, job_id: str) -> Optional[Dict[str, Any]]:
        async with async_session() as session:
            job = await session.get(Job, job_id)
            if not job:
                return None
            return {
                "job_id": job.id,
                "topic": job.topic,
                "depth": job.depth,
                "status": job.status,
                "step": job.step,
                "error": job.error,
                "result": job.result,
                "created_at": job.created_at.isoformat() if job.created_at else None
            }
