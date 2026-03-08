#!/usr/bin/env python3
"""Fetch AI newsletter content from RSS feeds and write a daily digest.

Pulls latest posts from Substack newsletters (Lenny, a16z, AI Collective, etc.)
and writes them to profile/ai-daily-digest/YYYY-MM-DD.md.

Run locally: python scripts/fetch_ai_digest.py
Also runs daily via GitHub Actions (.github/workflows/fetch-ai-digest.yml).
"""

from __future__ import annotations

import argparse
import logging
from datetime import datetime, timezone
from pathlib import Path

import feedparser

# RSS feeds — high-signal only (AI PM, product, agents). Low-value removed.
RSS_FEEDS: list[tuple[str, str]] = [
    ("Lenny's Newsletter", "https://lenny.substack.com/feed"),
    ("a16z speedrun", "https://speedrun.substack.com/feed"),
    ("The AI Collective", "https://aicollective.substack.com/feed"),
    ("Agentic AI Weekly (Berkeley RDI)", "https://berkeleyrdi.substack.com/feed"),
    ("Generative AI for Everyone", "https://boringbot.substack.com/feed"),
    ("AI x Product", "https://productishand03.substack.com/feed"),
    ("Marily's AI Product Academy", "https://marily.substack.com/feed"),
]

# Max entries per feed to avoid huge digests
MAX_ENTRIES_PER_FEED = 5

# Project root (script lives in scripts/)
PROJECT_ROOT = Path(__file__).resolve().parent.parent
DIGEST_DIR = PROJECT_ROOT / "output"


def parse_entry_date(entry: feedparser.FeedParserDict) -> datetime | None:
    """Parse published/updated date from RSS entry."""
    for key in ("published_parsed", "updated_parsed"):
        parsed = entry.get(key)
        if parsed:
            try:
                return datetime(*parsed[:6], tzinfo=timezone.utc)
            except (TypeError, ValueError):
                pass
    return None


def fetch_feed(name: str, url: str) -> list[dict]:
    """Fetch RSS feed and return list of entry dicts with title, link, date, source."""
    entries: list[dict] = []
    try:
        feed = feedparser.parse(url)
        if feed.bozo and not getattr(feed, "entries", None):
            logging.warning("Feed %s (%s) failed to parse", name, url)
            return entries

        for i, entry in enumerate(feed.entries):
            if i >= MAX_ENTRIES_PER_FEED:
                break
            title = entry.get("title", "(no title)")
            link = entry.get("link", "")
            date = parse_entry_date(entry)
            entries.append({
                "title": title,
                "link": link,
                "date": date,
                "source": name,
            })
    except Exception as e:
        logging.warning("Error fetching %s (%s): %s", name, url, e)

    return entries


def build_digest(date: datetime) -> str:
    """Fetch all feeds and build markdown digest for the given date."""
    all_entries: list[dict] = []
    for name, url in RSS_FEEDS:
        all_entries.extend(fetch_feed(name, url))

    # Sort by date descending (newest first), entries without date go last
    def sort_key(e: dict) -> tuple[bool, datetime]:
        has_date = e["date"] is not None
        dt = e["date"] or datetime.min.replace(tzinfo=timezone.utc)
        return (not has_date, -dt.timestamp())

    all_entries.sort(key=sort_key)

    # Build markdown
    lines = [
        f"# AI Daily Digest — {date.strftime('%Y-%m-%d')}",
        "",
        f"*Auto-generated from RSS feeds. Last run: {datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M UTC')}*",
        "",
        "---",
        "",
    ]

    current_source: str | None = None
    for entry in all_entries:
        if entry["source"] != current_source:
            current_source = entry["source"]
            lines.append(f"## {current_source}")
            lines.append("")

        date_str = entry["date"].strftime("%Y-%m-%d") if entry["date"] else ""
        lines.append(f"- [{entry['title']}]({entry['link']})" + (f" — {date_str}" if date_str else ""))
        lines.append("")

    return "\n".join(lines)


def main() -> None:
    """Run the digest fetcher."""
    logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")

    parser = argparse.ArgumentParser(description="Fetch AI newsletter RSS and write daily digest")
    parser.add_argument(
        "--date",
        type=str,
        default=None,
        help="Date for digest (YYYY-MM-DD). Default: today UTC.",
    )
    parser.add_argument(
        "--output",
        type=str,
        default=None,
        help="Output file path. Default: output/YYYY-MM-DD.md",
    )
    args = parser.parse_args()

    if args.date:
        try:
            digest_date = datetime.strptime(args.date, "%Y-%m-%d").replace(tzinfo=timezone.utc)
        except ValueError:
            logging.error("Invalid --date. Use YYYY-MM-DD.")
            raise SystemExit(1)
    else:
        digest_date = datetime.now(timezone.utc)

    content = build_digest(digest_date)

    if args.output:
        out_path = Path(args.output)
    else:
        DIGEST_DIR.mkdir(parents=True, exist_ok=True)
        out_path = DIGEST_DIR / f"{digest_date.strftime('%Y-%m-%d')}.md"

    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(content, encoding="utf-8")
    logging.info("Wrote digest to %s", out_path)


if __name__ == "__main__":
    main()
