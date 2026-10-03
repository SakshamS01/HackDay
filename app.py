import html
import time
import streamlit as st

import config
from cache_manager import read_cache

# Must be the very first Streamlit command
st.set_page_config(
    page_title="GDG Cloud Nagpur | Hacktoberfest 2026 Live Contributor Showcase",
    page_icon="https://gdg.community.dev/static/images/favicon.ico",
    layout="wide",
    initial_sidebar_state="collapsed",
)

REFRESH_SECONDS = config.REFRESH_SECONDS

# Custom Google Material Design styles matching https://gdg.community.dev/gdg-cloud-nagpur/
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Google+Sans:wght@400;500;700&family=Roboto:wght@300;400;500;700&display=swap');

html, body, [class*="st-"] {
    font-family: 'Google Sans', 'Roboto', -apple-system, BlinkMacSystemFont, sans-serif !important;
}

.stApp {
    background-color: #f8f9fa !important;
    color: #202124 !important;
}

/* Hide Streamlit chrome for presentation/projector readiness */
#MainMenu {visibility: hidden;}
header[data-testid="stHeader"] {display: none;}
footer {visibility: hidden;}
.block-container {
    padding-top: 1rem !important;
    padding-bottom: 2rem !important;
    max-width: 1400px !important;
}

/* Top Navbar */
.gdg-navbar {
    background: #ffffff;
    border: 1px solid #dadce0;
    padding: 12px 24px;
    border-radius: 12px;
    margin-bottom: 20px;
    display: flex;
    align-items: center;
    justify-content: space-between;
    box-shadow: 0 1px 3px rgba(60,64,67,0.08);
}

.gdg-brand-left {
    display: flex;
    align-items: center;
    gap: 14px;
}

.gdg-logo-svg {
    height: 30px;
    width: auto;
}

.gdg-title-text {
    font-size: 1.25rem;
    font-weight: 700;
    color: #202124;
    letter-spacing: -0.3px;
    display: flex;
    align-items: center;
    gap: 8px;
}

.gdg-chapter-pill {
    background: #e8f0fe;
    color: #1a73e8;
    font-size: 0.8rem;
    font-weight: 700;
    padding: 3px 10px;
    border-radius: 16px;
    border: 1px solid #d2e3fc;
}

.gdg-nav-badges {
    display: flex;
    align-items: center;
    gap: 10px;
}

.live-indicator {
    display: inline-flex;
    align-items: center;
    gap: 6px;
    background: #e6f4ea;
    color: #137333;
    font-size: 0.75rem;
    font-weight: 700;
    padding: 4px 12px;
    border-radius: 20px;
    border: 1px solid #ceead6;
}

.live-dot {
    width: 8px;
    height: 8px;
    background-color: #34a853;
    border-radius: 50%;
    display: inline-block;
    animation: pulse 1.5s infinite;
}

@keyframes pulse {
    0% { transform: scale(0.95); box-shadow: 0 0 0 0 rgba(52, 168, 83, 0.7); }
    70% { transform: scale(1.1); box-shadow: 0 0 0 6px rgba(52, 168, 83, 0); }
    100% { transform: scale(0.95); box-shadow: 0 0 0 0 rgba(52, 168, 83, 0); }
}

.gemma-sponsor-badge {
    background: linear-gradient(135deg, #1a73e8 0%, #4285f4 50%, #34a853 100%);
    color: #ffffff;
    font-size: 0.78rem;
    font-weight: 600;
    padding: 4px 12px;
    border-radius: 20px;
    display: inline-flex;
    align-items: center;
    gap: 6px;
    box-shadow: 0 1px 3px rgba(26,115,232,0.3);
}

.hf-fest-badge {
    background: #feefe3;
    color: #c5221f;
    font-size: 0.75rem;
    font-weight: 700;
    padding: 4px 12px;
    border-radius: 20px;
    border: 1px solid #fad2cf;
}

/* Chapter Hero Section */
.gdg-hero-card {
    background: #ffffff;
    border: 1px solid #dadce0;
    border-radius: 16px;
    padding: 24px 30px;
    margin-bottom: 24px;
    box-shadow: 0 1px 3px rgba(60,64,67,0.06);
    position: relative;
    overflow: hidden;
}

.gdg-hero-card::before {
    content: '';
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    height: 4px;
    background: linear-gradient(90deg, #4285f4 0%, #ea4335 25%, #fbbc04 50%, #34a853 75%, #4285f4 100%);
}

.gdg-hero-title {
    font-size: 2.1rem;
    font-weight: 700;
    color: #202124;
    margin: 0 0 6px 0;
    line-height: 1.2;
}

.gdg-hero-meta {
    font-size: 0.95rem;
    color: #5f6368;
    display: flex;
    align-items: center;
    flex-wrap: wrap;
    gap: 16px;
    margin-bottom: 12px;
}

.gdg-hero-desc {
    font-size: 0.98rem;
    color: #3c4043;
    line-height: 1.5;
    margin-bottom: 16px;
    max-width: 1050px;
}

.gdg-hero-actions {
    display: flex;
    align-items: center;
    gap: 12px;
    flex-wrap: wrap;
}

.btn-gdg-primary {
    background: #1a73e8;
    color: #ffffff !important;
    font-weight: 600;
    font-size: 0.88rem;
    padding: 8px 18px;
    border-radius: 8px;
    text-decoration: none;
    display: inline-flex;
    align-items: center;
    gap: 6px;
}

.btn-gdg-secondary {
    background: #ffffff;
    color: #1a73e8 !important;
    font-weight: 600;
    font-size: 0.88rem;
    padding: 8px 18px;
    border-radius: 8px;
    text-decoration: none;
    display: inline-flex;
    align-items: center;
    gap: 6px;
    border: 1px solid #dadce0;
}

/* Stat Cards */
.stat-card {
    background: #ffffff;
    border: 1px solid #dadce0;
    border-radius: 14px;
    padding: 18px 20px;
    box-shadow: 0 1px 3px rgba(60,64,67,0.06);
    position: relative;
    overflow: hidden;
    height: 100%;
    transition: transform 0.15s ease;
}

.stat-card:hover {
    transform: translateY(-2px);
    box-shadow: 0 4px 12px rgba(60,64,67,0.12);
}

.stat-card-blue { border-top: 4px solid #1a73e8; }
.stat-card-green { border-top: 4px solid #34a853; }
.stat-card-yellow { border-top: 4px solid #fbbc04; }
.stat-card-red { border-top: 4px solid #ea4335; }

.stat-label {
    font-size: 0.8rem;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 0.5px;
    color: #5f6368;
    margin-bottom: 6px;
    display: flex;
    justify-content: space-between;
    align-items: center;
}

.stat-value {
    font-size: 2.4rem;
    font-weight: 700;
    line-height: 1.1;
    color: #202124;
}

.stat-subtext {
    font-size: 0.8rem;
    color: #5f6368;
    margin-top: 6px;
}

/* Section Header */
.section-header-block {
    margin: 24px 0 14px 0;
    padding-bottom: 8px;
    border-bottom: 2px solid #e8eaed;
}

.section-title {
    font-size: 1.35rem;
    font-weight: 700;
    color: #202124;
    display: flex;
    align-items: center;
    gap: 8px;
    margin: 0 0 4px 0;
}

.section-subtitle {
    font-size: 0.85rem;
    color: #5f6368;
}

/* PR Feed Card */
.gdg-pr-card {
    background: #ffffff;
    border: 1px solid #dadce0;
    border-radius: 12px;
    padding: 16px 20px;
    margin-bottom: 14px;
    box-shadow: 0 1px 2px rgba(60,64,67,0.05);
    transition: border-color 0.2s ease, box-shadow 0.2s ease;
}

.gdg-pr-card:hover {
    border-color: #1a73e8;
    box-shadow: 0 3px 10px rgba(60,64,67,0.12);
}

.pr-top-row {
    display: flex;
    align-items: center;
    justify-content: space-between;
    flex-wrap: wrap;
    gap: 8px;
    margin-bottom: 8px;
}

.contributor-profile {
    display: flex;
    align-items: center;
    gap: 10px;
}

.contributor-avatar {
    width: 36px;
    height: 36px;
    border-radius: 50%;
    border: 1px solid #dadce0;
    object-fit: cover;
    background: #f1f3f4;
}

.contributor-name-box {
    display: flex;
    flex-direction: column;
}

.contributor-name {
    font-size: 0.95rem;
    font-weight: 700;
    color: #202124;
    line-height: 1.2;
}

.contributor-handle {
    font-size: 0.78rem;
    color: #5f6368;
}

.pr-badges-row {
    display: flex;
    align-items: center;
    gap: 8px;
    flex-wrap: wrap;
}

.status-chip {
    font-size: 0.75rem;
    font-weight: 700;
    padding: 3px 10px;
    border-radius: 12px;
    letter-spacing: 0.3px;
    display: inline-flex;
    align-items: center;
    gap: 4px;
}

.chip-merged {
    background: #e6f4ea;
    color: #137333;
    border: 1px solid #ceead6;
}

.chip-open {
    background: #e8f0fe;
    color: #1a73e8;
    border: 1px solid #d2e3fc;
}

.chip-closed {
    background: #f1f3f4;
    color: #5f6368;
    border: 1px solid #dadce0;
}

.repo-pill {
    background: #f8f9fa;
    border: 1px solid #dadce0;
    color: #1a73e8;
    font-size: 0.8rem;
    font-weight: 600;
    padding: 3px 10px;
    border-radius: 6px;
    text-decoration: none;
    display: inline-flex;
    align-items: center;
    gap: 4px;
}

.pr-title {
    font-size: 1.05rem;
    font-weight: 600;
    color: #202124;
    margin: 8px 0 10px 0;
    line-height: 1.35;
}

/* Gemma AI Summary Box */
.gemma-summary-container {
    background: #f8fafd;
    border: 1px solid #d2e3fc;
    border-left: 4px solid #1a73e8;
    border-radius: 8px;
    padding: 12px 16px;
    margin-top: 10px;
}

.gemma-summary-header {
    display: flex;
    align-items: center;
    gap: 6px;
    font-size: 0.75rem;
    font-weight: 700;
    color: #1a73e8;
    text-transform: uppercase;
    letter-spacing: 0.5px;
    margin-bottom: 5px;
}

.gemma-summary-text {
    font-size: 0.93rem;
    color: #202124;
    line-height: 1.5;
}

/* Leaderboard Card & Table */
.gdg-leaderboard-container {
    background: #ffffff;
    border: 1px solid #dadce0;
    border-radius: 14px;
    padding: 6px 16px;
    box-shadow: 0 1px 3px rgba(60,64,67,0.06);
}

.leaderboard-item {
    display: flex;
    align-items: center;
    padding: 12px 6px;
    border-bottom: 1px solid #f1f3f4;
}

.leaderboard-item:last-child {
    border-bottom: none;
}

.rank-circle {
    width: 32px;
    height: 32px;
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
    font-weight: 700;
    font-size: 0.9rem;
    margin-right: 12px;
    flex-shrink: 0;
}

.rank-top-1 { background: #fef7e0; color: #b06000; border: 1.5px solid #fbbc04; }
.rank-top-2 { background: #f1f3f4; color: #3c4043; border: 1.5px solid #bdc1c6; }
.rank-top-3 { background: #feefe3; color: #b06000; border: 1.5px solid #f6aea9; }
.rank-top-other { background: #ffffff; color: #5f6368; border: 1px solid #dadce0; }

.leaderboard-user {
    flex: 1;
    display: flex;
    align-items: center;
    gap: 10px;
}

.user-text-col {
    display: flex;
    flex-direction: column;
}

.user-realname {
    font-size: 0.93rem;
    font-weight: 700;
    color: #202124;
}

.user-username {
    font-size: 0.78rem;
    color: #5f6368;
}

.stats-badges-col {
    display: flex;
    align-items: center;
    gap: 6px;
    text-align: right;
}

.badge-merged-count {
    background: #e6f4ea;
    color: #137333;
    font-size: 0.78rem;
    font-weight: 700;
    padding: 3px 8px;
    border-radius: 12px;
    border: 1px solid #ceead6;
}

.badge-open-count {
    background: #e8f0fe;
    color: #1a73e8;
    font-size: 0.78rem;
    font-weight: 700;
    padding: 3px 8px;
    border-radius: 12px;
    border: 1px solid #d2e3fc;
}

.badge-total-count {
    background: #f1f3f4;
    color: #5f6368;
    font-size: 0.78rem;
    font-weight: 700;
    padding: 3px 8px;
    border-radius: 12px;
}

/* Chapter Info & Footer */
.gdg-footer-card {
    background: #ffffff;
    border: 1px solid #dadce0;
    border-radius: 12px;
    padding: 16px 24px;
    margin-top: 24px;
    font-size: 0.85rem;
    color: #5f6368;
    display: flex;
    align-items: center;
    justify-content: space-between;
    flex-wrap: wrap;
    gap: 12px;
}
</style>
""", unsafe_allow_html=True)


def load_data():
    from participants import load_participants
    participants = load_participants("participants.csv")
    
    cache = read_cache("cache.json")
    raw_prs = list(cache.get("pull_requests", {}).values())
    
    # Strictly allow ONLY PRs authored by participants in participants.csv
    prs = [
        p for p in raw_prs
        if p.get("github_username", "").lower() in participants
    ]
    return prs, participants


def compute_metrics(prs, participants):
    total = len(prs)
    merged = sum(1 for p in prs if p.get("is_merged"))
    open_count = sum(1 for p in prs if p.get("state") == "open")
    
    # Active contributors with registered activity or attendee list
    active_contributors = len(set(p.get("github_username") for p in prs if p.get("github_username")))
    total_participants = max(active_contributors, len(participants))
    return total, merged, open_count, active_contributors, total_participants


def build_leaderboard(prs, participants):
    stats = {}
    for user in participants:
        stats[user.lower()] = {"merged": 0, "open": 0, "total": 0}

    for pr in prs:
        user = pr.get("github_username", "").lower()
        if user not in stats:
            continue
        stats[user]["total"] += 1
        if pr.get("is_merged"):
            stats[user]["merged"] += 1
        elif pr.get("state") == "open":
            stats[user]["open"] += 1

    ranked = sorted(
        stats.items(),
        key=lambda x: (x[1]["merged"], x[1]["open"], x[1]["total"], x[0]),
        reverse=True,
    )

    display_rows = []
    for i, (user, counts) in enumerate(ranked, 1):
        disp = participants.get(user, user)
        display_name = disp.get("display_name", user) if isinstance(disp, dict) else str(disp)
        display_rows.append({
            "rank": i,
            "username": user,
            "display_name": display_name,
            "merged": counts["merged"],
            "open": counts["open"],
            "total": counts["total"],
        })
    return display_rows


def render_navbar():
    st.markdown("""
<div class="gdg-navbar">
    <div class="gdg-brand-left">
        <svg class="gdg-logo-svg" viewBox="0 0 192 116" fill="none" xmlns="http://www.w3.org/2000/svg">
            <path d="M57.6 115.2L0 57.6L57.6 0L76.8 19.2L38.4 57.6L76.8 96L57.6 115.2Z" fill="#EA4335"/>
            <path d="M134.4 115.2L115.2 96L153.6 57.6L115.2 19.2L134.4 0L192 57.6L134.4 115.2Z" fill="#4285F4"/>
            <path d="M96 28.8L115.2 48L76.8 86.4L57.6 67.2L96 28.8Z" fill="#FBBC04"/>
            <path d="M96 86.4L115.2 67.2L134.4 86.4L115.2 105.6L96 86.4Z" fill="#34A853"/>
        </svg>
        <div class="gdg-title-text">
            <span>Google Developer Groups</span>
            <span class="gdg-chapter-pill">GDG Cloud Nagpur</span>
        </div>
    </div>
    <div class="gdg-nav-badges">
        <div class="live-indicator">
            <span class="live-dot"></span>
            <span>LIVE SYNC</span>
        </div>
        <div class="hf-fest-badge">
            🎃 Hacktoberfest 2026
        </div>
        <div class="gemma-sponsor-badge">
            <svg width="14" height="14" viewBox="0 0 24 24" fill="currentColor">
                <path d="M12 2L15.09 8.26L22 9.27L17 14.14L18.18 21.02L12 17.77L5.82 21.02L7 14.14L2 9.27L8.91 8.26L12 2Z"/>
            </svg>
            <span>Powered by Gemma 3:4b</span>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)


def render_hero():
    st.markdown("""
<div class="gdg-hero-card">
    <h1 class="gdg-hero-title">GDG Cloud Nagpur</h1>
    <div class="gdg-hero-meta">
        <span>📍 Nagpur, Maharashtra, India</span>
        <span>•</span>
        <span>👥 4,441 Chapter Members</span>
        <span>•</span>
        <span>🚀 Hacktoberfest 2026 Showcase</span>
        <span>•</span>
        <span>⚡ Local AI Sponsor: Google Gemma 3:4b</span>
    </div>
    <div class="gdg-hero-desc">
        Welcome to the <strong>Hacktoberfest 2026 Live Contributor Showcase</strong> at GDG Cloud Nagpur. 
        All pull requests made by registered community attendees are tracked here in real time. 
        Every contribution is automatically analyzed and summarized into clear, plain English by <strong>Gemma 3:4b</strong> running locally.
    </div>
    <div class="gdg-hero-actions">
        <a href="https://gdg.community.dev/gdg-cloud-nagpur/" target="_blank" class="btn-gdg-primary">
            <span>Visit Chapter Page</span>
            <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <path d="M7 17L17 7M17 7H7M17 7V17"/>
            </svg>
        </a>
        <a href="https://github.com" target="_blank" class="btn-gdg-secondary">
            <svg width="16" height="16" viewBox="0 0 24 24" fill="currentColor">
                <path d="M12 0C5.37 0 0 5.37 0 12c0 5.31 3.435 9.795 8.205 11.385.6.105.825-.255.825-.57 0-.285-.015-1.23-.015-2.235-3.015.555-3.795-.735-4.035-1.41-.135-.345-.72-1.41-1.23-1.695-.42-.225-1.02-.78-.015-.795.945-.015 1.62.87 1.845 1.23 1.08 1.815 2.805 1.305 3.495.99.105-.78.42-1.305.765-1.605-2.67-.3-5.46-1.335-5.46-5.925 0-1.305.465-2.385 1.23-3.225-.12-.3-.54-1.53.12-3.18 0 0 1.005-.315 3.3 1.23.96-.27 1.98-.405 3-.405s2.04.135 3 .405c2.295-1.56 3.3-1.23 3.3-1.23.66 1.65.24 2.88.12 3.18.765.84 1.23 1.905 1.23 3.225 0 4.605-2.805 5.625-5.475 5.925.435.375.81 1.095.81 2.22 0 1.605-.015 2.895-.015 3.3 0 .315.225.69.825.57A12.02 12.02 0 0024 12c0-6.63-5.37-12-12-12z"/>
            </svg>
            <span>GitHub Contributor Hub</span>
        </a>
        <span style="color:#5f6368;font-size:0.84rem;margin-left:auto;">
            🔄 Auto-refreshing every 15s • Projector Ready (Press F11)
        </span>
    </div>
</div>
""", unsafe_allow_html=True)


def render_stat_cards(total, merged, open_count, contributors, total_participants):
    col1, col2, col3, col4 = st.columns(4)

    merged_rate = f"{(merged / total * 100):.0f}%" if total > 0 else "0%"

    with col1:
        st.markdown(f"""
<div class="stat-card stat-card-blue">
    <div class="stat-label">
        <span>Total Pull Requests</span>
        <span style="color:#1a73e8;">🔀</span>
    </div>
    <div class="stat-value">{total}</div>
    <div class="stat-subtext">Submitted across registered repos</div>
</div>
""", unsafe_allow_html=True)

    with col2:
        st.markdown(f"""
<div class="stat-card stat-card-green">
    <div class="stat-label">
        <span>Merged Contributions</span>
        <span style="color:#34a853;">✅</span>
    </div>
    <div class="stat-value" style="color:#137333;">{merged}</div>
    <div class="stat-subtext">{merged_rate} acceptance rate</div>
</div>
""", unsafe_allow_html=True)

    with col3:
        st.markdown(f"""
<div class="stat-card stat-card-yellow">
    <div class="stat-label">
        <span>Under Review</span>
        <span style="color:#f9ab00;">⏳</span>
    </div>
    <div class="stat-value" style="color:#b06000;">{open_count}</div>
    <div class="stat-subtext">Awaiting maintainer merge</div>
</div>
""", unsafe_allow_html=True)

    with col4:
        st.markdown(f"""
<div class="stat-card stat-card-red">
    <div class="stat-label">
        <span>Active Contributors</span>
        <span style="color:#ea4335;">👥</span>
    </div>
    <div class="stat-value" style="color:#c5221f;">{contributors} <span style="font-size:1.1rem;color:#5f6368;font-weight:400;">/ {total_participants}</span></div>
    <div class="stat-subtext">Registered GDG attendees</div>
</div>
""", unsafe_allow_html=True)


def render_live_feed(prs, participants):
    st.markdown("""
<div class="section-header-block">
    <h2 class="section-title">
        <svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="#1a73e8" stroke-width="2">
            <circle cx="12" cy="12" r="10"></circle>
            <polyline points="12 6 12 12 16 14"></polyline>
        </svg>
        <span>Live Contributions Feed</span>
    </h2>
    <div class="section-subtitle">Real-time plain-English summaries by Gemma 3:4b running locally</div>
</div>
""", unsafe_allow_html=True)

    sorted_prs = sorted(prs, key=lambda x: x.get("created_at", ""), reverse=True)

    if not sorted_prs:
        st.info("No pull requests recorded yet. Waiting for attendee contributions...")
        return

    # Render PR cards without indentation so markdown doesn't parse it as code
    cards_html = []
    for pr in sorted_prs[:25]:
        state = pr.get("state", "open")
        if pr.get("is_merged"):
            state = "merged"

        if state == "merged":
            chip_class = "chip-merged"
            chip_label = "✓ MERGED"
        elif state == "open":
            chip_class = "chip-open"
            chip_label = "● OPEN"
        else:
            chip_class = "chip-closed"
            chip_label = "✕ CLOSED"

        user = html.escape(pr.get("github_username", ""))
        disp = participants.get(user.lower(), {})
        display_name = html.escape(disp.get("display_name", user) if isinstance(disp, dict) else user)
        repo = html.escape(pr.get("repo", ""))
        pr_num = html.escape(str(pr.get("pr_number", "")))
        url = html.escape(pr.get("url", "#"))
        title = html.escape(pr.get("title", ""))
        summary = pr.get("summary")

        avatar_url = f"https://avatars.githubusercontent.com/{user}?s=72"

        if summary:
            escaped_summary = html.escape(summary)
            summary_markup = (
                f'<div class="gemma-summary-container">'
                f'<div class="gemma-summary-header">'
                f'<svg width="13" height="13" viewBox="0 0 24 24" fill="#1a73e8"><path d="M12 2L15.09 8.26L22 9.27L17 14.14L18.18 21.02L12 17.77L5.82 21.02L7 14.14L2 9.27L8.91 8.26L12 2Z"/></svg>'
                f'<span>Gemma 3:4b Plain-English Summary</span>'
                f'</div>'
                f'<div class="gemma-summary-text">{escaped_summary}</div>'
                f'</div>'
            )
        else:
            summary_markup = (
                f'<div class="gemma-summary-container" style="border-left-color: #bdc1c6;">'
                f'<div class="gemma-summary-header" style="color: #5f6368;">'
                f'<span>Analyzing with Gemma 3:4b...</span>'
                f'</div>'
                f'<div class="gemma-summary-text" style="color: #80868b; font-style: italic;">Generating concise summary in background...</div>'
                f'</div>'
            )

        card = (
            f'<div class="gdg-pr-card">'
            f'<div class="pr-top-row">'
            f'<div class="contributor-profile">'
            f'<img class="contributor-avatar" src="{avatar_url}" onerror="this.src=\'https://github.githubassets.com/images/modules/logos_page/GitHub-Mark.png\'" alt="{user}"/>'
            f'<div class="contributor-name-box">'
            f'<span class="contributor-name">{display_name}</span>'
            f'<span class="contributor-handle">@{user}</span>'
            f'</div>'
            f'</div>'
            f'<div class="pr-badges-row">'
            f'<a class="repo-pill" href="{url}" target="_blank">'
            f'<span>{repo}#{pr_num}</span>'
            f'<svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M18 13v6a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V8a2 2 0 0 1 2-2h6"></path><polyline points="15 3 21 3 21 9"></polyline><line x1="10" y1="14" x2="21" y2="3"></line></svg>'
            f'</a>'
            f'<span class="status-chip {chip_class}">{chip_label}</span>'
            f'</div>'
            f'</div>'
            f'<div class="pr-title">{title}</div>'
            f'{summary_markup}'
            f'</div>'
        )
        cards_html.append(card)

    st.markdown("".join(cards_html), unsafe_allow_html=True)


def render_leaderboard(rows):
    st.markdown("""
<div class="section-header-block">
    <h2 class="section-title">
        <svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="#fbbc04" stroke-width="2">
            <path d="M6 9H4.5a2.5 2.5 0 0 1 0-5H6"></path>
            <path d="M18 9h1.5a2.5 2.5 0 0 0 0-5H18"></path>
            <path d="M4 22h16"></path>
            <path d="M10 14.66V17c0 .55-.45 1-1 1H7v2h10v-2h-2c-.55 0-1-.45-1-1v-2.34c3.27-.4 5.8-3.05 5.99-6.36L20 4H4l.01 4.3c.2 3.31 2.72 5.96 5.99 6.36z"></path>
        </svg>
        <span>Attendee Leaderboard</span>
    </h2>
    <div class="section-subtitle">Ranked by Merged PRs, then Open PRs</div>
</div>
""", unsafe_allow_html=True)

    if not rows:
        st.info("No contributors yet.")
        return

    items_html = []
    for row in rows[:15]:
        rank = row["rank"]
        if rank == 1:
            rank_class = "rank-top-1"
            rank_display = "🥇"
        elif rank == 2:
            rank_class = "rank-top-2"
            rank_display = "🥈"
        elif rank == 3:
            rank_class = "rank-top-3"
            rank_display = "🥉"
        else:
            rank_class = "rank-top-other"
            rank_display = str(rank)

        user = html.escape(row["username"])
        display_name = html.escape(row["display_name"])
        avatar_url = f"https://avatars.githubusercontent.com/{user}?s=64"

        item = (
            f'<div class="leaderboard-item">'
            f'<div class="rank-circle {rank_class}">{rank_display}</div>'
            f'<div class="leaderboard-user">'
            f'<img class="contributor-avatar" src="{avatar_url}" onerror="this.src=\'https://github.githubassets.com/images/modules/logos_page/GitHub-Mark.png\'" alt="{user}"/>'
            f'<div class="user-text-col">'
            f'<span class="user-realname">{display_name}</span>'
            f'<span class="user-username">@{user}</span>'
            f'</div>'
            f'</div>'
            f'<div class="stats-badges-col">'
            f'<span class="badge-merged-count" title="Merged Pull Requests">{row["merged"]} Merged</span>'
            f'<span class="badge-open-count" title="Open Pull Requests">{row["open"]} Open</span>'
            f'<span class="badge-total-count" title="Total Pull Requests">{row["total"]} Total</span>'
            f'</div>'
            f'</div>'
        )
        items_html.append(item)

    full_leaderboard_html = (
        f'<div class="gdg-leaderboard-container">'
        f'{"".join(items_html)}'
        f'</div>'
    )
    st.markdown(full_leaderboard_html, unsafe_allow_html=True)

    # GDG Chapter community highlight card
    st.markdown("""
<div style="background:#ffffff; border:1px solid #dadce0; border-radius:14px; padding:18px; margin-top:20px; box-shadow:0 1px 3px rgba(60,64,67,0.06);">
    <div style="display:flex; align-items:center; gap:10px; margin-bottom:8px;">
        <svg width="20" height="20" viewBox="0 0 24 24" fill="#1a73e8">
            <path d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm1 15h-2v-6h2v6zm0-8h-2V7h2v2z"/>
        </svg>
        <span style="font-weight:700; color:#202124; font-size:0.95rem;">About GDG Cloud Nagpur</span>
    </div>
    <div style="font-size:0.85rem; color:#5f6368; line-height:1.5;">
        Google Developer Groups (GDG) Cloud Nagpur is an active community for developers, students, and engineers in Central India exploring Google Cloud, Android, Web, and Gemini/Gemma models.
    </div>
    <div style="margin-top:12px; padding-top:12px; border-top:1px solid #e8eaed; display:flex; justify-content:space-between; align-items:center;">
        <span style="font-size:0.8rem; color:#1a73e8; font-weight:700;">✨ Sponsor: Google Gemma 3:4b</span>
        <span style="font-size:0.8rem; color:#5f6368;">Nagpur, India</span>
    </div>
</div>
""", unsafe_allow_html=True)


def render_footer():
    st.markdown("""
<div class="gdg-footer-card">
    <div>
        <strong>GDG Cloud Nagpur × Hacktoberfest 2026</strong> • Official Contributor Showcase
    </div>
    <div>
        Local AI Powered by <strong>Gemma 3:4b (Ollama)</strong> • Designed with Google Material Guidelines
    </div>
</div>
""", unsafe_allow_html=True)


def check_celebration(merged_count):
    if "prev_merged" not in st.session_state:
        st.session_state.prev_merged = merged_count
        return
    if merged_count > st.session_state.prev_merged:
        st.balloons()
    st.session_state.prev_merged = merged_count


@st.cache_resource
def init_background_workers():
    """Start background fetcher and summarizer threads automatically (for Streamlit Cloud & local)."""
    import threading

    if config.GITHUB_TOKEN:
        try:
            import fetcher
            t1 = threading.Thread(target=fetcher.run, daemon=True, name="FetcherDaemon")
            t1.start()
        except Exception as e:
            print("Notice: background fetcher thread:", e)

        try:
            import summarizer
            t2 = threading.Thread(target=summarizer.run, daemon=True, name="SummarizerDaemon")
            t2.start()
        except Exception as e:
            print("Notice: background summarizer thread:", e)
    return True


def main():
    init_background_workers()

    render_navbar()

    if not config.GITHUB_TOKEN:
        st.warning(
            "🔑 **GitHub Token Missing**: Please add `GITHUB_TOKEN` to your Streamlit Cloud Secrets "
            "(in App Settings -> Secrets) or `.env` file to enable live polling."
        )

    render_hero()

    prs, participants = load_data()
    total, merged, open_count, contributors, total_participants = compute_metrics(prs, participants)

    render_stat_cards(total, merged, open_count, contributors, total_participants)

    check_celebration(merged)

    # 2-Column layout: Left Feed (60%), Right Leaderboard & Community (40%)
    col_left, col_right = st.columns([13, 9])

    with col_left:
        render_live_feed(prs, participants)

    with col_right:
        leaderboard = build_leaderboard(prs, participants)
        render_leaderboard(leaderboard)

    render_footer()

    # Auto refresh timer
    time.sleep(REFRESH_SECONDS)
    st.rerun()


main()
