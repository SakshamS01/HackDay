import json
import os
import tempfile
import time
import logging

log = logging.getLogger(__name__)

EMPTY_CACHE = {"last_updated": None, "participants": {}, "pull_requests": {}}


def read_cache(path):
    if not os.path.exists(path):
        return json.loads(json.dumps(EMPTY_CACHE))
    for attempt in range(5):
        try:
            with open(path, "r", encoding="utf-8") as fh:
                return json.load(fh)
        except (json.JSONDecodeError, OSError) as exc:
            if attempt < 4:
                time.sleep(0.05)
            else:
                log.warning("Cache read failed, returning empty: %s", exc)
                return json.loads(json.dumps(EMPTY_CACHE))


def write_cache(path, data):
    dir_name = os.path.dirname(path) or "."
    for attempt in range(6):
        tmp_path = None
        try:
            fd, tmp_path = tempfile.mkstemp(dir=dir_name, suffix=".tmp")
            with os.fdopen(fd, "w", encoding="utf-8") as fh:
                json.dump(data, fh, indent=2, ensure_ascii=False)
            os.replace(tmp_path, path)
            return
        except OSError as exc:
            if tmp_path and os.path.exists(tmp_path):
                try:
                    os.remove(tmp_path)
                except OSError:
                    pass
            # Fallback: direct atomic write if replace is blocked by Windows lock
            if attempt >= 2:
                try:
                    with open(path, "w", encoding="utf-8") as fh:
                        json.dump(data, fh, indent=2, ensure_ascii=False)
                    return
                except OSError:
                    pass
            time.sleep(0.1 * (attempt + 1))
    log.error("Cache write failed after retries")


def update_prs(path, pr_dict):
    """Merge a dict of {pr_key: pr_data} into the cache."""
    cache = read_cache(path)
    for key, data in pr_dict.items():
        existing = cache["pull_requests"].get(key, {})
        # preserve existing summary if present
        if existing.get("summary") and not data.get("summary"):
            data["summary"] = existing["summary"]
        existing.update(data)
        cache["pull_requests"][key] = existing
    write_cache(path, cache)


def update_participants(path, participants):
    """Merge participants into the cache."""
    cache = read_cache(path)
    from datetime import datetime, timezone
    now = datetime.now(timezone.utc).isoformat()
    for username, display_name in participants.items():
        cache["participants"][username] = {
            "display_name": display_name,
            "last_fetched": cache["participants"].get(username, {}).get("last_fetched"),
        }
    cache["last_updated"] = now
    write_cache(path, cache)


def set_pr_summary(path, pr_key, summary):
    cache = read_cache(path)
    if pr_key in cache["pull_requests"]:
        cache["pull_requests"][pr_key]["summary"] = summary
        write_cache(path, cache)


def mark_user_fetched(path, username):
    cache = read_cache(path)
    from datetime import datetime, timezone
    now = datetime.now(timezone.utc).isoformat()
    if username in cache["participants"]:
        cache["participants"][username]["last_fetched"] = now
    cache["last_updated"] = now
    write_cache(path, cache)
