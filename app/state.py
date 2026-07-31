import json
from typing import Optional, Dict, Any

class StateManager:
    def __init__(self, redis_url: str = ""):
        self.db: Dict[str, str] = {}

    async def save_job_state(self, job_id: str, state: Dict[str, Any]):
        self.db[f"job:{job_id}"] = json.dumps(state)

    async def get_job_state(self, job_id: str) -> Optional[Dict[str, Any]]:
        data = self.db.get(f"job:{job_id}")
        if data:
            return json.loads(data)
        return None
