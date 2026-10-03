import time
import logging
from datetime import datetime, timezone

import requests

import config
from participants import load_participants
from cache_manager import read_cache, update_prs, update_participants, mark_user_fetched

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [fetcher] %(levelname)s %(message)s",
)
log = logging.getLogger(__name__)

GITHUB_API = "https://api.github.com"
HEADERS = {
    "Accept": "application/vnd.github+json",
    "Authorization": f"Bearer {config.GITHUB_TOKEN}",
}

# cache repo topics so we don't re-fetch
_repo_topic_cache = {}


def fetch_repo_has_hacktoberfest(repo_full_name):
    if repo_full_name in _repo_topic_cache:
        return _repo_topic_cache[repo_full_name]
    url = f"{GITHUB_API}/repos/{repo_full_name}/topics"
    try:
        resp = requests.get(url, headers=HEADERS, timeout=15)
        if resp.status_code == 200:
            topics = resp.json().get("names", [])
            result = "hacktoberfest" in topics
        else:
            result = False
    except requests.RequestException:
        result = False
    _repo_topic_cache[repo_full_name] = result
    return result


def fetch_merged_status(repo_full_name, pr_number):
    url = f"{GITHUB_API}/repos/{repo_full_name}/pulls/{pr_number}"
    try:
        resp = requests.get(url, headers=HEADERS, timeout=15)
        if resp.status_code == 200:
            data = resp.json()
            return data.get("merged_at") is not None, data.get("merged_at")
    except requests.RequestException:
        pass
    return False, None


def check_rate_limit(response):
    remaining = int(response.headers.get("X-RateLimit-Remaining", 999))
    if remaining < 3:
        reset_ts = int(response.headers.get("X-RateLimit-Reset", 0))
        wait = max(reset_ts - int(time.time()), 5)
        log.warning("Rate limit near zero, sleeping %d seconds", wait)
        time.sleep(wait)


def fetch_prs_for_user(username):
    query = f"author:{username} type:pr created:{config.START_DATE}..{config.END_DATE}"
    url = f"{GITHUB_API}/search/issues"
    params = {"q": query, "per_page": 100, "sort": "created", "order": "desc"}
    try:
        resp = requests.get(url, headers=HEADERS, params=params, timeout=20)
        check_rate_limit(resp)
        if resp.status_code == 403:
            log.warning("Rate limited for user %s, skipping", username)
            return {}
        if resp.status_code != 200:
            log.warning("GitHub search error %d for %s", resp.status_code, username)
            return {}
        items = resp.json().get("items", [])
    except requests.RequestException as exc:
        log.warning("Network error fetching PRs for %s: %s", username, exc)
        return {}

    pr_updates = {}
    for item in items:
        pr_url = item.get("pull_request", {}).get("html_url", item.get("html_url", ""))
        repo_full = "/".join(pr_url.split("/")[3:5]) if "github.com" in pr_url else ""
        if not repo_full:
            continue
        pr_number = item["number"]
        pr_key = f"{repo_full}/{pr_number}"

        state = item["state"]
        is_merged = False
        merged_at = None
        if state == "closed":
            is_merged, merged_at = fetch_merged_status(repo_full, pr_number)

        labels = [lbl["name"] for lbl in item.get("labels", [])]
        hacktoberfest_label = any(
            "hacktoberfest" in lbl.lower() for lbl in labels
        )
        repo_hacktoberfest = fetch_repo_has_hacktoberfest(repo_full)

        body = item.get("body") or ""
        pr_updates[pr_key] = {
            "github_username": username,
            "repo": repo_full,
            "pr_number": pr_number,
            "title": item.get("title", ""),
            "body_snippet": body[:500],
            "url": pr_url,
            "state": "merged" if is_merged else state,
            "is_merged": is_merged,
            "created_at": item.get("created_at"),
            "merged_at": merged_at,
            "closed_at": item.get("closed_at"),
            "labels": labels,
            "hacktoberfest_accepted": hacktoberfest_label,
            "repo_has_hacktoberfest_topic": repo_hacktoberfest,
            "summary": None,
            "fetched_at": datetime.now(timezone.utc).isoformat(),
        }

    return pr_updates


def run():
    log.info("Fetcher started (polling %d users/min)", config.USERS_PER_MINUTE)
    sleep_per_user = 60.0 / config.USERS_PER_MINUTE

    while True:
        participants = load_participants(config.PARTICIPANTS_SOURCE)
        if not participants:
            log.warning("No participants found, retrying in 30s")
            time.sleep(30)
            continue

        update_participants(config.CACHE_PATH, participants)
        usernames = list(participants.keys())
        log.info("Polling %d participants", len(usernames))

        for username in usernames:
            log.info("Fetching PRs for %s", username)
            pr_updates = fetch_prs_for_user(username)
            if pr_updates:
                update_prs(config.CACHE_PATH, pr_updates)
                log.info("Found %d PRs for %s", len(pr_updates), username)
            mark_user_fetched(config.CACHE_PATH, username)
            time.sleep(sleep_per_user)

        log.info("Cycle complete, restarting")


if __name__ == "__main__":
    run()
