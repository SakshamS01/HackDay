import csv
import io
import logging
import requests

log = logging.getLogger(__name__)


def extract_github_username(value):
    value = value.strip().rstrip("/")
    if "github.com/" in value:
        return value.split("github.com/")[-1].split("/")[0].lower()
    return value.lower()


def load_participants(source):
    """Return {github_username: display_name} from a CSV file or URL."""
    raw = ""
    if source.startswith("http"):
        try:
            resp = requests.get(source, timeout=15)
            resp.raise_for_status()
            raw = resp.text
        except requests.RequestException as exc:
            log.warning("Failed to fetch participant sheet: %s", exc)
            return {}
    else:
        try:
            with open(source, encoding="utf-8") as fh:
                raw = fh.read()
        except FileNotFoundError:
            log.warning("Participant file not found: %s", source)
            return {}

    participants = {}
    reader = csv.DictReader(io.StringIO(raw))
    for row in reader:
        username_raw = row.get("github_username", "").strip()
        display = row.get("display_name", "").strip()
        if not username_raw:
            continue
        username = extract_github_username(username_raw)
        if not username:
            continue
        participants[username] = display or username
    return participants
