import uuid
import json
from datetime import datetime
from typing import List, Dict, Any, Optional
import aiosqlite
from backend.app.database import DB_FILE

class MemoryStoreService:
    """Manages persistent episodic memory, character knowledge, and unresolved mysteries via aiosqlite."""

    @staticmethod
    async def record_episode_memory(
        episode_id: str,
        category: str,
        summary: str,
        character_states: Dict[str, Any],
        item_states: Dict[str, Any],
        unresolved_mystery: Optional[str] = None
    ) -> Dict[str, Any]:
        mem_id = str(uuid.uuid4())
        now = datetime.utcnow().isoformat()
        
        async with aiosqlite.connect(str(DB_FILE)) as db:
            await db.execute("""
                INSERT INTO story_memories (
                    id, episode_id, event_category, summary, character_states,
                    item_states, unresolved_mystery, is_resolved, created_at
                ) VALUES (?, ?, ?, ?, ?, ?, ?, 0, ?)
            """, (
                mem_id, episode_id, category, summary,
                json.dumps(character_states),
                json.dumps(item_states),
                unresolved_mystery,
                now
            ))
            await db.commit()

        return {
            "id": mem_id,
            "episode_id": episode_id,
            "category": category,
            "summary": summary,
            "unresolved_mystery": unresolved_mystery
        }

    @staticmethod
    async def get_active_lore_and_memories(series_id: str = "default") -> Dict[str, Any]:
        """
        Gathers unresolved mysteries, character states, and past episode summaries.
        """
        async with aiosqlite.connect(str(DB_FILE)) as db:
            db.row_factory = aiosqlite.Row
            cursor = await db.execute("""
                SELECT * FROM story_memories ORDER BY created_at DESC LIMIT 10
            """)
            rows = await cursor.fetchall()
            
            unresolved = []
            recent_events = []
            merged_character_states = {}
            merged_item_states = {}

            for r in rows:
                if r["unresolved_mystery"] and not r["is_resolved"]:
                    unresolved.append(r["unresolved_mystery"])
                recent_events.append(r["summary"])
                
                c_states = json.loads(r["character_states"]) if r["character_states"] else {}
                i_states = json.loads(r["item_states"]) if r["item_states"] else {}
                merged_character_states.update(c_states)
                merged_item_states.update(i_states)

            return {
                "unresolved_mysteries": unresolved,
                "recent_events": recent_events[:5],
                "current_character_states": merged_character_states,
                "current_item_states": merged_item_states
            }
