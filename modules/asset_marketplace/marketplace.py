"""
Autonomous AI Cartoon Studio - Internal 3D Asset Marketplace & Browser Engine (V2.0)
Provides faceted search, filtering, metadata querying, and WebGL asset inspection endpoints.
"""

import sqlite3
from pathlib import Path

DB_PATH = Path(r"E:\YT\database\studio_v2.db")

class AssetMarketplace:
    def __init__(self, db_path=DB_PATH):
        self.db_path = db_path

    def list_categories(self) -> list:
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT DISTINCT category, count(*) FROM assets GROUP BY category")
            return [{"category": row[0], "count": row[1]} for row in cursor.fetchall()]

    def search_assets(self, query: str = None, category: str = None, 
                      rig_family: str = None, max_polycount: int = None,
                      limit: int = 50) -> list:
        with sqlite3.connect(self.db_path) as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            
            sql = "SELECT * FROM assets WHERE commercial_permitted = 1"
            params = []
            
            if query:
                sql += " AND (name LIKE ? OR asset_id LIKE ?)"
                params.extend([f"%{query}%", f"%{query}%"])
                
            if category:
                sql += " AND category = ?"
                params.append(category)
                
            if rig_family:
                sql += " AND rig_family = ?"
                params.append(rig_family)
                
            if max_polycount:
                sql += " AND polygon_count <= ?"
                params.append(max_polycount)
                
            sql += " ORDER BY created_at DESC LIMIT ?"
            params.append(limit)
            
            cursor.execute(sql, params)
            return [dict(row) for row in cursor.fetchall()]

    def get_asset_by_id(self, asset_id: str) -> dict:
        with sqlite3.connect(self.db_path) as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM assets WHERE asset_id = ?", (asset_id,))
            row = cursor.fetchone()
            return dict(row) if row else None

if __name__ == "__main__":
    amp = AssetMarketplace()
    cats = amp.list_categories()
    print("Marketplace categories:", cats)
