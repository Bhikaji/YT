import asyncio
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import aiosqlite
from backend.app.database import DB_FILE

async def main():
    async with aiosqlite.connect(str(DB_FILE)) as db:
        cur = await db.execute("SELECT id, episode_id, current_state FROM production_jobs")
        rows = await cur.fetchall()
        print(f"Total production jobs in DB: {len(rows)}")
        for r in rows:
            print(f"  • Job ID: {r[0]} | Episode: {r[1]} | State: {r[2]}")
        cur2 = await db.execute("SELECT count(*) FROM job_events")
        total_events = (await cur2.fetchone())[0]
        print(f"Total job transition events in DB: {total_events}")

if __name__ == "__main__":
    asyncio.run(main())
