import os
import sys
from dotenv import load_dotenv

load_dotenv()

GITHUB_TOKEN = os.getenv("GITHUB_TOKEN", "")
OLLAMA_URL = os.getenv("OLLAMA_URL", "http://localhost:11434")
OLLAMA_MODEL = os.getenv("OLLAMA_MODEL", "gemma3:4b")
PARTICIPANTS_SOURCE = os.getenv("PARTICIPANTS_SOURCE", "participants.csv")
START_DATE = os.getenv("START_DATE", "2026-10-01")
END_DATE = os.getenv("END_DATE", "2026-10-31")
USERS_PER_MINUTE = int(os.getenv("USERS_PER_MINUTE", "20"))
REFRESH_SECONDS = int(os.getenv("REFRESH_SECONDS", "15"))
CACHE_PATH = os.getenv("CACHE_PATH", "cache.json")

if not GITHUB_TOKEN or GITHUB_TOKEN == "your_token_here":
    print("ERROR: Set a valid GITHUB_TOKEN in .env")
    sys.exit(1)
