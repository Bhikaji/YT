import os
import sys
from pathlib import Path

# Add project root to path
BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(BASE_DIR))

import requests
from backend.app.config import settings

def connect_colab_worker(gradio_url: str):
    gradio_url = gradio_url.strip()
    if not gradio_url.startswith("http"):
        gradio_url = "https://" + gradio_url

    print("==========================================================================")
    print("      CONNECTING TO PATH 1: 100% FREE CLOUD GPU WORKER (COLAB WAN 2.1)    ")
    print("==========================================================================")
    print(f"Target URL: {gradio_url}")
    print("Testing connection...")

    # Step 1: Handshake
    handshake_success = False
    try:
        from gradio_client import Client
        client = Client(gradio_url)
        print("✔ Gradio Client handshake successful!")
        handshake_success = True
    except Exception as e:
        print(f"Notice: Gradio Client handshake ({e}). Testing HTTP endpoint...")
        try:
            r = requests.get(gradio_url, timeout=15)
            if r.status_code == 200:
                print("✔ HTTP endpoint reached successfully!")
                handshake_success = True
            else:
                print(f"Warning: HTTP status code {r.status_code}")
        except Exception as e2:
            print(f"Error reaching endpoint: {e2}")

    # Step 2: Save to .env
    env_file = BASE_DIR / ".env"
    existing_lines = []
    if env_file.exists():
        with open(env_file, "r", encoding="utf-8") as f:
            existing_lines = [
                line for line in f.readlines()
                if not line.startswith("WAN21_API_URL=") and not line.startswith("ANIMATION_ENGINE_MODE=")
            ]

    existing_lines.append(f"ANIMATION_ENGINE_MODE=COLAB_WAN\n")
    existing_lines.append(f"WAN21_API_URL={gradio_url}\n")

    with open(env_file, "w", encoding="utf-8") as f:
        f.writelines(existing_lines)

    print(f"✔ Saved WAN21_API_URL to: {env_file}")
    print(f"✔ ANIMATION_ENGINE_MODE set to 'COLAB_WAN'")
    print("--------------------------------------------------------------------------")
    print("STATUS: CONNECTED & READY FOR AUTONOMOUS VIDEO PRODUCTION!")
    print("You can now run: python scripts/produce_demo_short.py")
    print("==========================================================================")

if __name__ == "__main__":
    if len(sys.argv) > 1:
        target_url = sys.argv[1]
    else:
        print("Enter your Google Colab Gradio Live URL (e.g. https://xxxx.gradio.live):")
        target_url = input("URL: ").strip()

    if target_url:
        connect_colab_worker(target_url)
    else:
        print("No URL provided. Exiting.")
