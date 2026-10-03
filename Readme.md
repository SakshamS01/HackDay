# 🎃 GDG Nagpur Hacktoberfest Live Dashboard

A live, projector-ready dashboard that tracks pull requests made by attendees of **Hacktoberfest 2026 × GDG Cloud Nagpur** — with every contribution summarised in plain English by **Gemma 4 running locally via Ollama**.

Attendees register their GitHub username, and the dashboard shows PRs opened, merged, and pending in near real time. Instead of cryptic titles like `Update README.md`, the audience sees *"Fixed a broken install link in the Ollama Windows guide."*

> Built for the Contributor Showcase segment, so the whole room can watch their contributions land.

---

## ✨ Features

- **Live PR tracking** for all registered attendees during Hacktoberfest
- **Open / merged / closed status** for every pull request
- **AI summaries** — Gemma 4 writes a one-line, human-readable summary of each PR
- **Fully local AI** — no cloud LLM API keys; summaries run on your laptop through Ollama
- **Leaderboard** ranked by merged PRs, then open PRs
- **Live feed** of the latest contributions
- **Celebration effects** when a new PR gets merged 🎈
- **Hacktoberfest status** — highlights PRs with the `hacktoberfest-accepted` label or in repos with the `hacktoberfest` topic
- **Rate-limit friendly** — rotates through attendees instead of hammering the GitHub API
- **Resilient** — everything is cached, so slow Wi-Fi or a slow model never blanks the screen

---

## 🖼️ Screenshot

<!-- Replace with a real screenshot after your first run -->
![Dashboard screenshot](docs/screenshot.png)

---

## 🧠 How It Works

```
participants.csv / Google Sheet
            │
            ▼
       fetcher.py ──────────► GitHub Search API
            │                  (PRs by each attendee)
            ▼
       cache.json ◄────────── summarizer.py ──► Ollama (Gemma 4, local)
            │
            ▼
         app.py  (Streamlit dashboard, auto-refresh)
```

1. **`fetcher.py`** reads the participant list and polls GitHub for each attendee's PRs created within the event date range. It rotates through users so it stays within GitHub's search rate limit.
2. **`summarizer.py`** sends each *new* PR's title, repo name, and the start of its description to Gemma via the local Ollama API, and stores a one-sentence summary. Each PR is summarised only once.
3. **`app.py`** reads `cache.json` and renders the dashboard, refreshing automatically.

The fetcher and the dashboard run as separate processes, so the UI stays responsive even when GitHub or Gemma is slow.

---

## 📋 Prerequisites

- **Python 3.10+**
- **[Ollama](https://ollama.com)** installed and running
- A **Gemma 4** model pulled in Ollama (the smallest size is recommended for speed)
- A **GitHub personal access token** (fine-grained, no extra permissions needed — public data only)
- *(Optional)* A Google Form + Sheet for attendee registration

> ⚠️ **Pull the Gemma model before the event.** Model downloads are several GB and will be painful on venue Wi-Fi.

---

## 🚀 Installation

### 1. Clone the repository

```bash
git clone https://github.com/<your-username>/gdg-hacktoberfest-dashboard.git
cd gdg-hacktoberfest-dashboard
```

### 2. Create a virtual environment and install dependencies

```bash
python -m venv .venv

# macOS / Linux
source .venv/bin/activate

# Windows
.venv\Scripts\activate

pip install -r requirements.txt
```

`requirements.txt`:

```
streamlit
requests
python-dotenv
```

### 3. Set up Ollama and Gemma

```bash
# Pull a Gemma 4 model (use the exact tag listed in the Ollama library)
ollama pull <gemma-4-model-tag>

# Confirm it's available and note the exact name
ollama list
```

### 4. Create a GitHub token

1. Go to **GitHub → Settings → Developer settings → Personal access tokens → Fine-grained tokens**
2. Generate a new token with **public repository read access only**
3. Copy it into your `.env` file (next step)

### 5. Configure environment variables

Create a `.env` file in the project root:

```env
# GitHub
GITHUB_TOKEN=your_token_here

# Ollama / Gemma
OLLAMA_URL=http://localhost:11434
OLLAMA_MODEL=<gemma-4-model-tag>   # exact name from `ollama list`

# Participants: a local CSV path or a published Google Sheet CSV URL
PARTICIPANTS_SOURCE=participants.csv

# Event date range (PRs created in this window are counted)
START_DATE=2026-10-01
END_DATE=2026-10-31

# Polling behaviour
USERS_PER_MINUTE=20        # stay under GitHub's ~30 search requests/min
REFRESH_SECONDS=15         # how often the dashboard re-reads the cache
```

> 🔒 **Never commit `.env`.** It is listed in `.gitignore`.

---

## 👥 Registering Participants

### Option A: Local CSV

Create `participants.csv`:

```csv
github_username,display_name
octocat,The Octocat
your-username,Your Name
```

### Option B: Google Form (recommended for the event)

1. Create a Google Form asking for **GitHub username** and **display name**, with a consent checkbox (see [Privacy & Consent](#-privacy--consent))
2. Open the linked Google Sheet → **File → Share → Publish to web**
3. Choose the responses sheet and **CSV** format, then copy the URL
4. Set `PARTICIPANTS_SOURCE` in `.env` to that URL

New registrations will appear on the dashboard automatically on the next fetch cycle.

---

## ▶️ Running the Dashboard

Open **two terminals** (with the virtual environment activated in both).

**Terminal 1 — start the fetcher:**

```bash
python fetcher.py
```

**Terminal 2 — start the dashboard:**

```bash
streamlit run app.py
```

The dashboard opens at `http://localhost:8501`. Put the browser in full-screen mode (`F11`) for the projector.

Make sure Ollama is running in the background (`ollama serve` if it isn't already).

---

## 📺 Dashboard Layout

| Section | What it shows |
|---|---|
| **Top counters** | Total PRs, merged, open, active contributors |
| **Leaderboard** | Contributors ranked by merged PRs, then open PRs |
| **Live feed** | Latest PRs with username, repo, status badge, and Gemma summary |
| **Celebrations** | Balloons when a new merge is detected |

Designed for projectors: dark theme, large fonts, high contrast.

---

## ⏱️ Rate Limits

GitHub's search API allows roughly **30 requests per minute** for authenticated users. With ~50 attendees, querying everyone at once would hit the limit.

The fetcher instead **rotates** through attendees at `USERS_PER_MINUTE` (default 20), so each person refreshes every 2–3 minutes. That's effectively real-time on a projector while staying safely within limits.

If a rate limit is hit anyway, the fetcher backs off and the dashboard keeps showing cached data.

---

## 🔐 Privacy & Consent

This event is open to participants aged **13–18** as well as adults, and the dashboard is shown on a projector.

- **Opt-in only.** Only attendees who register their username appear on the dashboard.
- **Include a consent checkbox** in the registration form, e.g. *"I agree to my GitHub username and public PR activity being displayed during the event."*
- **Public data only.** The dashboard reads only public PR information already visible on GitHub.
- **Removal on request.** Anyone can ask to be removed; delete their row from the participant list and their entries disappear on the next refresh.
- **No data kept after the event** beyond aggregate stats, unless organisers decide otherwise.

---

## 🗂️ Project Structure

```
gdg-hacktoberfest-dashboard/
├── app.py              # Streamlit UI + auto-refresh
├── fetcher.py          # GitHub polling with rotation + caching
├── summarizer.py       # Ollama / Gemma calls with per-PR cache
├── participants.csv    # Local participant list (or use a Sheet URL)
├── cache.json          # Generated at runtime — not committed
├── requirements.txt
├── .env                # Secrets — not committed
├── .gitignore
├── docs/
│   └── screenshot.png
└── README.md
```

`.gitignore` should include:

```
.env
cache.json
.venv/
__pycache__/
```

---

## 🛠️ Troubleshooting

| Problem | Fix |
|---|---|
| Dashboard is empty | Check `participants.csv` or the Sheet URL, confirm the date range, and make sure `fetcher.py` is running |
| `403` or rate-limit errors | Lower `USERS_PER_MINUTE`; confirm `GITHUB_TOKEN` is set correctly |
| Summaries never appear | Run `ollama list` and check `OLLAMA_MODEL` matches exactly; confirm Ollama is running |
| Summaries are slow | Use the smallest Gemma 4 size; PR titles are shown until the summary is ready |
| Wrong merged/closed status | Merged status comes from `pull_request.merged_at`; the fetcher falls back to the PR endpoint if it's missing |
| New registrations not showing | Google's published CSV can lag a few minutes; wait one fetch cycle |

---

## 🧪 Testing Before the Event

- Add your own username plus a couple of active open-source contributors to `participants.csv` so the dashboard has real data
- Open a test PR on one of your own repos and watch it appear
- Merge it and confirm the celebration fires
- Disconnect Wi-Fi briefly to confirm the cached view keeps working

---

## 🗺️ Roadmap

- [ ] "First PR ever" badge for first-time contributors
- [ ] Contributions by language / repo chart
- [ ] End-of-event summary export (e.g. *"50 attendees, 63 PRs, 41 merged"*) for the organisers' recap
- [ ] Support for multiple events / chapters via config
- [ ] Docker setup for one-command launch
- [ ] Hindi / Marathi UI option

---

## 🤝 Contributing

Contributions are welcome — this project is part of Hacktoberfest! 🎉

1. Fork the repository
2. Create a branch: `git checkout -b feature/your-feature`
3. Commit your changes: `git commit -m "Add your feature"`
4. Push the branch: `git push origin feature/your-feature`
5. Open a Pull Request describing what you changed and why

Look for issues labelled **`good first issue`** or **`hacktoberfest`** to get started. Please keep PRs meaningful — low-effort or spam PRs will be closed.

---

## 📄 License

This project is licensed under the **MIT License**. See [LICENSE](LICENSE) for details.

---

## 🙏 Acknowledgements

- **GDG Cloud Nagpur** for organising Hacktoberfest 2026 × GDG Cloud Nagpur
- **Hacktoberfest** by DigitalOcean and partners for celebrating open source every October
- **Google Gemma** and **Ollama** for making local AI accessible
- Every attendee who opened their first pull request 💜

---

**Learn. Contribute. Build. Repeat.**
