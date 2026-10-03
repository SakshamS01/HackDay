import os
from dotenv import load_dotenv

load_dotenv()


def get_secret(key, default=""):
    # 1. Check OS environment variable (.env)
    val = os.getenv(key)
    if val:
        return val
    # 2. Check Streamlit Cloud st.secrets
    try:
        import streamlit as st
        if hasattr(st, "secrets") and key in st.secrets:
            return str(st.secrets[key])
    except Exception:
        pass
    return default


GITHUB_TOKEN = get_secret("GITHUB_TOKEN", "")
OLLAMA_URL = get_secret("OLLAMA_URL", "http://localhost:11434")
OLLAMA_MODEL = get_secret("OLLAMA_MODEL", "gemma3:4b")
PARTICIPANTS_SOURCE = get_secret("PARTICIPANTS_SOURCE", "participants.csv")
START_DATE = get_secret("START_DATE", "2026-10-01")
END_DATE = get_secret("END_DATE", "2026-10-31")
USERS_PER_MINUTE = int(get_secret("USERS_PER_MINUTE", "20"))
REFRESH_SECONDS = int(get_secret("REFRESH_SECONDS", "15"))
CACHE_PATH = get_secret("CACHE_PATH", "cache.json")
GEMINI_API_KEY = get_secret("GEMINI_API_KEY", "")
