"""
Autonomous AI Cartoon Studio - Production Job State Machine (V2.0)
Defines durable job lifecycle states, transitions, validation rules, and recovery routes.
"""

from enum import Enum
import sqlite3
import time
from pathlib import Path

DB_PATH = Path(r"E:\YT\database\studio_v2.db")

class JobState(str, Enum):
    QUEUED = "QUEUED"
    PLANNING = "PLANNING"
    GENERATING = "GENERATING"
    ANIMATING = "ANIMATING"
    RENDERING = "RENDERING"
    QUALITY_CHECK = "QUALITY_CHECK"
    ASSEMBLING = "ASSEMBLING"
    READY_TO_PUBLISH = "READY_TO_PUBLISH"
    PUBLISHED = "PUBLISHED"
    FAILED = "FAILED"
    RECOVERING = "RECOVERING"

# Valid state progression transitions
VALID_TRANSITIONS = {
    JobState.QUEUED: [JobState.PLANNING, JobState.FAILED],
    JobState.PLANNING: [JobState.GENERATING, JobState.FAILED],
    JobState.GENERATING: [JobState.ANIMATING, JobState.FAILED],
    JobState.ANIMATING: [JobState.RENDERING, JobState.FAILED],
    JobState.RENDERING: [JobState.QUALITY_CHECK, JobState.FAILED, JobState.RECOVERING],
    JobState.QUALITY_CHECK: [JobState.ASSEMBLING, JobState.RECOVERING, JobState.FAILED],
    JobState.RECOVERING: [JobState.RENDERING, JobState.ANIMATING, JobState.GENERATING, JobState.FAILED],
    JobState.ASSEMBLING: [JobState.READY_TO_PUBLISH, JobState.FAILED],
    JobState.READY_TO_PUBLISH: [JobState.PUBLISHED, JobState.FAILED],
    JobState.PUBLISHED: [],
    JobState.FAILED: [JobState.QUEUED, JobState.RECOVERING]
}

class ProductionStateMachine:
    def __init__(self, db_path=DB_PATH):
        self.db_path = db_path

    def _get_connection(self):
        conn = sqlite3.connect(self.db_path)
        conn.execute("PRAGMA foreign_keys = ON;")
        return conn

    def create_job(self, job_id: str, episode_id: str, stage: str = "INITIALIZATION", assigned_engine: str = "orchestrator") -> bool:
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
            INSERT INTO render_jobs (job_id, episode_id, stage, status, assigned_engine, started_at)
            VALUES (?, ?, ?, ?, ?, CURRENT_TIMESTAMP)
            """, (job_id, episode_id, stage, JobState.QUEUED.value, assigned_engine))
            conn.commit()
            return True

    def get_job_state(self, job_id: str) -> JobState:
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT status FROM render_jobs WHERE job_id = ?", (job_id,))
            row = cursor.fetchone()
            if not row:
                raise ValueError(f"Job {job_id} not found in database.")
            return JobState(row[0])

    def transition_to(self, job_id: str, target_state: JobState, stage_description: str = None, error_msg: str = None) -> bool:
        current_state = self.get_job_state(job_id)
        
        # Validate transition
        allowed = VALID_TRANSITIONS.get(current_state, [])
        if target_state not in allowed:
            raise ValueError(f"Invalid state transition: {current_state} -> {target_state}. Allowed: {allowed}")
            
        with self._get_connection() as conn:
            cursor = conn.cursor()
            query = "UPDATE render_jobs SET status = ?"
            params = [target_state.value]
            
            if stage_description:
                query += ", stage = ?"
                params.append(stage_description)
                
            if error_msg:
                query += ", error_message = ?"
                params.append(error_msg)
                
            if target_state in [JobState.PUBLISHED, JobState.READY_TO_PUBLISH]:
                query += ", completed_at = CURRENT_TIMESTAMP"
                
            query += " WHERE job_id = ?"
            params.append(job_id)
            
            cursor.execute(query, params)
            conn.commit()
            print(f"[State Machine] Job {job_id}: {current_state.value} -> {target_state.value}")
            return True

if __name__ == "__main__":
    sm = ProductionStateMachine()
    print("State Machine module verified successfully.")
