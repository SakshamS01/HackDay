import time
import logging

import requests

import config
from cache_manager import read_cache, set_pr_summary

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [summarizer] %(levelname)s %(message)s",
)
log = logging.getLogger(__name__)


def generate_summary(repo, title, body_snippet):
    prompt = (
        "Summarize this GitHub pull request in one plain-English sentence "
        "for a non-technical audience.\n"
        f"Repo: {repo}\n"
        f"Title: {title}\n"
        f"Description: {body_snippet}\n"
        "Reply with only the summary sentence, nothing else."
    )
    payload = {
        "model": config.OLLAMA_MODEL,
        "prompt": prompt,
        "stream": False,
    }
    try:
        resp = requests.post(
            f"{config.OLLAMA_URL}/api/generate",
            json=payload,
            timeout=120,
        )
        if resp.status_code == 200:
            text = resp.json().get("response", "").strip()
            if text:
                return text
    except requests.RequestException as exc:
        log.warning("Ollama request failed: %s", exc)
    return None


def run():
    log.info("Summarizer started (model: %s)", config.OLLAMA_MODEL)

    while True:
        cache = read_cache(config.CACHE_PATH)
        prs = cache.get("pull_requests", {})

        unsummarized = [
            (key, data) for key, data in prs.items()
            if data.get("summary") is None
        ]

        if not unsummarized:
            time.sleep(5)
            continue

        unsummarized.sort(key=lambda x: x[1].get("created_at", ""))
        log.info("Found %d PRs to summarize", len(unsummarized))

        for pr_key, pr_data in unsummarized:
            log.info("Summarizing %s", pr_key)
            summary = generate_summary(
                pr_data.get("repo", ""),
                pr_data.get("title", ""),
                pr_data.get("body_snippet", ""),
            )
            if summary is None:
                summary = pr_data.get("title", "No summary available")
                log.warning("Fallback to title for %s", pr_key)

            set_pr_summary(config.CACHE_PATH, pr_key, summary)
            log.info("Summarized: %s", summary[:80])

        time.sleep(5)


if __name__ == "__main__":
    run()
