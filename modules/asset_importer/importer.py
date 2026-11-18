"""
Autonomous AI Cartoon Studio - 3D Asset Ingestion & Registration Pipeline (V2.0)
Validates license, extracts geometry metadata, registers in SQLite, and organizes canonical files.
"""

import os
import shutil
import sqlite3
from pathlib import Path
from modules.asset_metadata.metadata_extractor import AssetMetadataExtractor
from modules.asset_license_manager.license_checker import AssetLicenseManager

DB_PATH = Path(r"E:\YT\database\studio_v2.db")
ASSETS_ROOT = Path(r"E:\YT\assets")

class AssetImporter:
    def __init__(self, db_path=DB_PATH, assets_root=ASSETS_ROOT):
        self.db_path = db_path
        self.assets_root = assets_root

    def import_asset(self, source_file: str, asset_id: str, name: str, category: str, 
                     license_type: str = "CC0", rig_family: str = None, 
                     thumbnail_path: str = None) -> dict:
        source_path = Path(source_file)
        if not source_path.exists():
            raise FileNotFoundError(f"Source asset not found: {source_file}")

        # 1. License Compliance Gate
        lic_audit = AssetLicenseManager.audit_license(license_type)
        if not lic_audit["is_permitted"]:
            raise PermissionError(f"Asset ingestion rejected by License Manager: {lic_audit['reason']}")

        # 2. Extract Geometry Metadata
        meta = AssetMetadataExtractor.extract_metadata(str(source_path))

        # 3. Canonical Destination Organization
        target_dir = self.assets_root / category
        target_dir.mkdir(parents=True, exist_ok=True)
        dest_file = target_dir / f"{asset_id}{source_path.suffix.lower()}"
        
        if source_path.resolve() != dest_file.resolve():
            shutil.copy2(source_path, dest_file)

        # 4. Register in SQLite Database
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("""
            INSERT OR REPLACE INTO assets (
                asset_id, name, category, format, file_path, thumbnail_path,
                polygon_count, vertex_count, has_armature, rig_family,
                license_type, commercial_permitted, attribution_required, updated_at
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, CURRENT_TIMESTAMP)
            """, (
                asset_id, name, category, meta["format"], str(dest_file), thumbnail_path,
                meta["polygon_count"], meta["vertex_count"], meta["has_armature"], rig_family,
                lic_audit["license_type"], 1, 1 if lic_audit["attribution_required"] else 0
            ))
            conn.commit()

        print(f"[Asset Importer] Registered '{name}' ({asset_id}) in category '{category}' successfully.")
        return {
            "asset_id": asset_id,
            "name": name,
            "category": category,
            "destination": str(dest_file),
            "metadata": meta,
            "license": lic_audit
        }

if __name__ == "__main__":
    importer = AssetImporter()
    base_obj = r"E:\YT\third_party\mpfb2\src\mpfb\data\3dobjs\base.obj"
    res = importer.import_asset(base_obj, "char_base_mesh_v2", "Humanoid Base Mesh", "characters", "CC0")
    print("Asset Ingestion Test Result:", res)
