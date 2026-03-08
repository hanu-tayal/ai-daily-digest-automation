#!/usr/bin/env python3
"""Parse AI digest, prioritize by relevance, and output a NotebookLM-ready summary.

For AI PMs: prioritizes Lenny's, AI x Product, Marily's, Agentic AI Weekly, AI Collective.
Output: profile/ai-daily-digest/YYYY-MM-DD-notebooklm.md

Run: python scripts/summarize_ai_digest.py [--date YYYY-MM-DD]
"""

from __future__ import annotations

import argparse
import re
from datetime import datetime, timezone
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
DIGEST_DIR = PROJECT_ROOT / "output"

# Priority: 1 = highest (AI PM, leadership, agents)
SOURCE_PRIORITY: dict[str, int] = {
    "Lenny's Newsletter": 1,
    "AI x Product": 1,
    "Marily's AI Product Academy": 1,
    "Agentic AI Weekly (Berkeley RDI)": 1,
    "The AI Collective": 2,
    "a16z speedrun": 2,
    "Generative AI for Everyone": 2,
}

# Keywords that boost priority (AI PM, agents, leadership)
BOOST_KEYWORDS = [
    "agent", "pm", "product", "scale", "adoption", "design", "pattern",
    "gtm", "sales", "founder", "leadership", "team", "cursor", "coinbase",
    "notion", "perplexity", "orchestrat", "router",
]


def parse_digest(path: Path) -> list[dict]:
    """Parse digest markdown into list of {title, link, source, date}."""
    text = path.read_text(encoding="utf-8")
    entries: list[dict] = []
    current_source: str | None = None

    for line in text.splitlines():
        if line.startswith("## "):
            current_source = line[3:].strip()
        elif line.strip().startswith("- [") and "](http" in line:
            if current_source is None:
                continue
            match = re.match(r"- \[([^\]]+)\]\((https?://[^\)]+)\)(?:\s*—\s*(\d{4}-\d{2}-\d{2}))?", line)
            if match:
                title = match.group(1).strip()
                link = match.group(2)
                date_str = match.group(3) or ""
                entries.append({
                    "title": title,
                    "link": link,
                    "source": current_source,
                    "date": date_str,
                })

    return entries


def priority_score(entry: dict) -> tuple[int, int]:
    """(source_priority, keyword_boost). Lower is better for sorting."""
    src_prio = SOURCE_PRIORITY.get(entry["source"], 4)
    title_lower = entry["title"].lower()
    boost = 0
    for kw in BOOST_KEYWORDS:
        if kw in title_lower:
            boost -= 1
            break
    return (src_prio, boost)


def build_summary(entries: list[dict], date: datetime) -> str:
    """Build NotebookLM-ready markdown summary."""
    lines = [
        f"# AI Digest Summary — {date.strftime('%B %d, %Y')}",
        "## Prioritized for <1 Hour | NotebookLM-Ready | Commute Listen",
        "",
        "*For AI PM, developer platforms, agentic AI. Prioritized by relevance to product leadership and adoption.*",
        "",
        "---",
        "",
    ]

    # Group by priority tier
    tier1 = [e for e in entries if SOURCE_PRIORITY.get(e["source"], 4) == 1]
    tier2 = [e for e in entries if SOURCE_PRIORITY.get(e["source"], 4) == 2]
    tier3 = [e for e in entries if SOURCE_PRIORITY.get(e["source"], 4) == 3]

    def section(title: str, items: list[dict]) -> list[str]:
        out = [f"## {title}", ""]
        for i, e in enumerate(items[:10], 1):  # Top 10 per tier
            out.append(f"### {i}. {e['title']} | {e['source']}")
            out.append(f"**Link:** {e['link']}")
            out.append("")
            out.append("**Summary:** *Read the article for full context. Key points: AI PM, product, or adoption angle.*")
            out.append("")
        return out

    lines.extend(section("TIER 1: Must-Read (AI PM & Leadership)", tier1))
    lines.extend(section("TIER 2: Technical & Product Depth", tier2))
    lines.extend(section("TIER 3: Market & Strategy", tier3))

    lines.extend([
        "---",
        "",
        "## How to Use This",
        "",
        "**NotebookLM (Podcast):** Upload this file to [NotebookLM](https://notebooklm.google.com). Click \"Generate Audio Overview.\" Choose \"Brief\" (under 2 min) or \"Deep Dive\" (15–30 min). Download the audio and listen on your phone during your commute.",
        "",
        "**Kindle:** Copy into Google Doc → File → Download → EPUB. Send to Kindle via email or Send to Kindle app.",
        "",
        "**Audible:** NotebookLM's Audio Overview is the fastest path. For true Audible, use TTS or record.",
        "",
        "---",
        "",
        f"*Auto-generated from digest. Run `python scripts/summarize_ai_digest.py` to regenerate.*",
    ])

    return "\n".join(lines)


def main() -> None:
    parser = argparse.ArgumentParser(description="Summarize AI digest for NotebookLM")
    parser.add_argument("--date", type=str, default=None, help="Date (YYYY-MM-DD). Default: today.")
    args = parser.parse_args()

    if args.date:
        try:
            digest_date = datetime.strptime(args.date, "%Y-%m-%d")
        except ValueError:
            raise SystemExit("Invalid --date. Use YYYY-MM-DD.")
    else:
        digest_date = datetime.now(timezone.utc)

    digest_path = DIGEST_DIR / f"{digest_date.strftime('%Y-%m-%d')}.md"
    if not digest_path.exists():
        raise SystemExit(f"Digest not found: {digest_path}. Run fetch_ai_digest.py first.")

    entries = parse_digest(digest_path)
    entries.sort(key=priority_score)

    content = build_summary(entries, digest_date)
    out_path = DIGEST_DIR / f"{digest_date.strftime('%Y-%m-%d')}-notebooklm.md"
    out_path.write_text(content, encoding="utf-8")
    print(f"Wrote {out_path}")


if __name__ == "__main__":
    main()
