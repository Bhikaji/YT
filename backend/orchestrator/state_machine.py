import uuid
import json
from datetime import datetime
from enum import Enum
from typing import Dict, Any, Optional, List
import aiosqlite
from backend.app.database import DB_FILE

class JobState(str, Enum):
    QUEUED = "QUEUED"
    PLANNING = "PLANNING"
    SCRIPTING = "SCRIPTING"
    VOICING = "VOICING"
    LIPSYNCING = "LIPSYNCING"
    ANIMATING = "ANIMATING"
    RENDERING = "RENDERING"
    QUALITY_CHECK = "QUALITY_CHECK"
    ASSEMBLING = "ASSEMBLING"
    READY_TO_PUBLISH = "READY_TO_PUBLISH"
    PUBLISHED = "PUBLISHED"
    FAILED = "FAILED"
    RECOVERY = "RECOVERY"

class ProductionJobStateMachine:
    """
    Durable finite state machine tracking production jobs.
    Guarantees atomic transitions, crash recovery, and state audit logs.
    """

    ALLOWED_TRANSITIONS = {
        JobState.QUEUED: [JobState.PLANNING, JobState.FAILED],
        JobState.PLANNING: [JobState.SCRIPTING, JobState.FAILED],
        JobState.SCRIPTING: [JobState.VOICING, JobState.FAILED],
        JobState.VOICING: [JobState.LIPSYNCING, JobState.FAILED],
        JobState.LIPSYNCING: [JobState.ANIMATING, JobState.FAILED],
        JobState.ANIMATING: [JobState.RENDERING, JobState.FAILED],
        JobState.RENDERING: [JobState.QUALITY_CHECK, JobState.FAILED],
        JobState.QUALITY_CHECK: [JobState.ASSEMBLING, JobState.RECOVERY, JobState.FAILED],
        JobState.RECOVERY: [JobState.ANIMATING, JobState.RENDERING, JobState.FAILED],
        JobState.ASSEMBLING: [JobState.READY_TO_PUBLISH, JobState.FAILED],
        JobState.READY_TO_PUBLISH: [JobState.PUBLISHED, JobState.FAILED],
        JobState.PUBLISHED: [],
        JobState.FAILED: [JobState.QUEUED, JobState.RECOVERY]
    }

    @classmethod
    async def create_job(cls, episode_id: str, priority: int = 1) -> Dict[str, Any]:
        """Creates and persists a new production job in QUEUED state."""
        job_id = str(uuid.uuid4())
        now = datetime.utcnow().isoformat()
        
        async with aiosqlite.connect(str(DB_FILE)) as db:
            await db.execute("""
                CREATE TABLE IF NOT EXISTS production_jobs (
                    id TEXT PRIMARY KEY,
                    episode_id TEXT NOT NULL,
                    current_state TEXT NOT NULL,
                    priority INTEGER DEFAULT 1,
                    retry_count INTEGER DEFAULT 0,
                    error_log TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                );
            """)
            await db.execute("""
                CREATE TABLE IF NOT EXISTS job_events (
                    id TEXT PRIMARY KEY,
                    job_id TEXT NOT NULL,
                    state_from TEXT NOT NULL,
                    state_to TEXT NOT NULL,
                    payload TEXT,
                    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                );
            """)
            await db.execute("""
                INSERT INTO production_jobs (id, episode_id, current_state, priority, retry_count, created_at, updated_at)
                VALUES (?, ?, ?, ?, 0, ?, ?)
            """, (job_id, episode_id, JobState.QUEUED.value, priority, now, now))
            
            await db.execute("""
                INSERT INTO job_events (id, job_id, state_from, state_to, payload, timestamp)
                VALUES (?, ?, 'NONE', ?, '{}', ?)
            """, (str(uuid.uuid4()), job_id, JobState.QUEUED.value, now))
            
            await db.commit()

        return {
            "job_id": job_id,
            "episode_id": episode_id,
            "state": JobState.QUEUED.value
        }

    @classmethod
    async def transition(cls, job_id: str, new_state: JobState, payload: Optional[Dict[str, Any]] = None) -> bool:
        """Transitions job to a new state if permitted by the state machine."""
        now = datetime.utcnow().isoformat()
        payload_str = json.dumps(payload or {})

        async with aiosqlite.connect(str(DB_FILE)) as db:
            db.row_factory = aiosqlite.Row
            cur = await db.execute("SELECT current_state FROM production_jobs WHERE id = ?", (job_id,))
            row = await cur.fetchone()
            if not row:
                raise ValueError(f"Job {job_id} not found.")

            current = JobState(row["current_state"])
            allowed = cls.ALLOWED_TRANSITIONS.get(current, [])

            if new_state not in allowed and new_state != JobState.FAILED:
                raise ValueError(f"Illegal transition: Cannot move from {current} to {new_state}.")

            await db.execute("""
                UPDATE production_jobs
                SET current_state = ?, updated_at = ?
                WHERE id = ?
            """, (new_state.value, now, job_id))

            await db.execute("""
                INSERT INTO job_events (id, job_id, state_from, state_to, payload, timestamp)
                VALUES (?, ?, ?, ?, ?, ?)
            """, (str(uuid.uuid4()), job_id, current.value, new_state.value, payload_str, now))

            await db.commit()
            return True

    @classmethod
    async def get_active_jobs(cls) -> List[Dict[str, Any]]:
        async with aiosqlite.connect(str(DB_FILE)) as db:
            db.row_factory = aiosqlite.Row
            cur = await db.execute("""
                SELECT * FROM production_jobs
                WHERE current_state NOT IN ('PUBLISHED', 'FAILED')
                ORDER BY priority DESC, created_at ASC
            """)
            rows = await cur.fetchall()
            return [dict(r) for r in rows]
