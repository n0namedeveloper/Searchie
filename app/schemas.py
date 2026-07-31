from pydantic import BaseModel
from typing import Optional

class JobRequest(BaseModel):
    topic: str
    depth: Optional[str] = "standard"

class JobResponse(BaseModel):
    job_id: str
    status: str
