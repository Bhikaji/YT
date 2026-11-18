"""
Downloads and extracts official Blender 4.2 LTS portable into E:\YT\tools\blender
"""

import os
import sys
import urllib.request
import zipfile
from pathlib import Path

BLENDER_URL = "https://download.blender.org/release/Blender4.2/blender-4.2.16-windows-x64.zip"
TARGET_DIR = Path("E:/YT/tools/blender")
ZIP_FILE = TARGET_DIR / "blender.zip"

def download_and_extract():
    TARGET_DIR.mkdir(parents=True, exist_ok=True)
    
    # Check if blender.exe already exists
    for root, dirs, files in os.walk(str(TARGET_DIR)):
        if "blender.exe" in files:
            blender_path = os.path.join(root, "blender.exe")
            print(f"✔ Blender already extracted at: {blender_path}")
            return blender_path

    print(f"Downloading Blender 4.2 LTS from: {BLENDER_URL}...")
    
    def reporthook(blocknum, blocksize, totalsize):
        readsofar = blocknum * blocksize
        if totalsize > 0:
            percent = readsofar * 1e2 / totalsize
            s = f"\rDownloading: {readsofar / (1024*1024):.1f}MB / {totalsize / (1024*1024):.1f}MB ({percent:.1f}%)"
            sys.stdout.write(s)
            sys.stdout.flush()

    urllib.request.urlretrieve(BLENDER_URL, str(ZIP_FILE), reporthook)
    print("\nDownload complete. Extracting Blender archive...")

    with zipfile.ZipFile(str(ZIP_FILE), 'r') as zip_ref:
        zip_ref.extractall(str(TARGET_DIR))

    print("Extraction complete. Cleaning up zip archive...")
    if ZIP_FILE.exists():
        os.remove(str(ZIP_FILE))

    # Find blender.exe
    for root, dirs, files in os.walk(str(TARGET_DIR)):
        if "blender.exe" in files:
            blender_path = os.path.join(root, "blender.exe")
            print(f"\n✔ Blender successfully installed at: {blender_path}")
            return blender_path

    raise RuntimeError("blender.exe not found after extraction!")

if __name__ == "__main__":
    download_and_extract()
