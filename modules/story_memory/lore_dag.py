"""
Story Memory & Lore DAG Engine
Maintains narrative continuity, character relationships, historical facts, and cliffhangers
across multi-season production schedules using a Directed Acyclic Graph (DAG).
"""

import json
import sqlite3
from pathlib import Path
from typing import Dict, Any, List, Optional

class LoreDAG:
    """Manages persistent world lore and narrative memory across episodes."""

    def __init__(self, db_path: str = r"E:\YT\database\studio_v2.db"):
        self.db_path = Path(db_path)

    def _get_connection(self):
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        return conn

    def record_episode_event(
        self,
        series_id: str,
        episode_number: int,
        event_name: str,
        character_involved: str,
        lore_fact: str,
        cliffhanger: Optional[str] = None
    ) -> int:
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO story_memory (series_id, episode_number, event_name, character_involved, lore_fact, cliffhanger)
                VALUES (?, ?, ?, ?, ?, ?)
            """, (series_id, episode_number, event_name, character_involved, lore_fact, cliffhanger))
            conn.commit()
            return cursor.lastrowid

    def get_series_lore_context(self, series_id: str) -> List[Dict[str, Any]]:
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT episode_number, event_name, character_involved, lore_fact, cliffhanger
                FROM story_memory
                WHERE series_id = ?
                ORDER BY episode_number ASC
            """, (series_id,))
            rows = cursor.fetchall()
            return [dict(r) for r in rows]

    def get_last_cliffhanger(self, series_id: str) -> Optional[str]:
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT cliffhanger
                FROM story_memory
                WHERE series_id = ? AND cliffhanger IS NOT NULL
                ORDER BY episode_number DESC
                LIMIT 1
            """, (series_id,))
            row = cursor.fetchone()
            return row["cliffhanger"] if row else None
