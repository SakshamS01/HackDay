import csv
import re
import os

SOURCE_CSV = "2026-10-02-hacktoberfest-hack-day-nagpur-x-gdgc-nagpur-registrations-export.csv"

def extract_username(val):
    if not val:
        return None
    val = val.strip().strip('"\'')
    # Look for github.com/username
    m = re.search(r'github\.com/([a-zA-Z0-9_\-]+)', val, re.IGNORECASE)
    if m:
        u = m.group(1).strip()
        if u.lower() not in ['settings', 'features', 'pulls', 'issues', 'explore', 'orgs', 'topics', '']:
            return u
    # Or just username
    m2 = re.match(r'^[a-zA-Z0-9_\-]+$', val)
    if m2 and val.lower() not in ['none', 'na', 'no', 'nil', 'https']:
        return val
    return None

strict_participants = {}
missing = []

with open(SOURCE_CSV, encoding="utf-8", errors="ignore") as f:
    reader = csv.DictReader(f)
    for i, row in enumerate(reader, 1):
        fn = row.get("first_name", "").strip()
        ln = row.get("last_name", "").strip()
        display_name = f"{fn} {ln}".strip()
        gh_raw = row.get("Github Profile Url", "").strip()
        
        username = extract_username(gh_raw)
        if username:
            strict_participants[username.lower()] = display_name or username
        else:
            missing.append((i, display_name, gh_raw))

print(f"Total valid attendees extracted strictly from CSV: {len(strict_participants)}")
print(f"Rows without valid GitHub URL: {len(missing)}")
for row in missing:
    print("  Row:", row)

# Write strictly to participants.csv
with open("participants.csv", "w", newline="", encoding="utf-8") as f:
    writer = csv.writer(f)
    writer.writerow(["github_username", "display_name"])
    for u, name in strict_participants.items():
        writer.writerow([u, name])

print("Written strictly to participants.csv!")
