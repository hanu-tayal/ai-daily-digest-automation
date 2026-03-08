#!/usr/bin/env python3
"""Convert AI digest summary to MP3 audio for commute listening.

Uses edge-tts (Microsoft, free, no API key). Output: output/YYYY-MM-DD-summary.mp3

Run: python scripts/text_to_speech_digest.py [--date YYYY-MM-DD]
"""

from __future__ import annotations

import argparse
import re
from datetime import datetime, timezone
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
DIGEST_DIR = PROJECT_ROOT / "output"


def markdown_to_speech_text(md: str) -> str:
    """Convert markdown to plain text suitable for TTS."""
    text = md

    # Remove links but keep the link text: [text](url) -> text
    text = re.sub(r"\[([^\]]+)\]\([^\)]+\)", r"\1", text)

    # Remove bold/italic markers
    text = re.sub(r"\*\*([^\*]+)\*\*", r"\1", text)
    text = re.sub(r"\*([^\*]+)\*", r"\1", text)

    # Convert headers to natural pauses (add period, TTS will pause)
    text = re.sub(r"^#{1,6}\s+", "", text, flags=re.MULTILINE)
    text = re.sub(r"^---\s*$", "\n\n", text, flags=re.MULTILINE)

    # Remove "Link:" lines (we already have the title)
    text = re.sub(r"^\*\*Link:\*\*\s*https?://[^\s]+\s*$", "", text, flags=re.MULTILINE)

    # Remove "How to Use This" section and everything after
    if "## How to Use This" in text:
        text = text.split("## How to Use This")[0]
    # Remove sources footnote in narrative
    if "*Sources:" in text:
        text = text.split("*Sources:")[0].strip()

    # Remove "Key Takeaways" header but keep content
    text = text.replace("## Key Takeaways (30-Second Version)", "Key takeaways.")

    # Clean up extra whitespace
    text = re.sub(r"\n{3,}", "\n\n", text)
    text = re.sub(r" +", " ", text)
    text = text.strip()

    return text


def main() -> None:
    parser = argparse.ArgumentParser(description="Convert digest summary to MP3")
    parser.add_argument("--date", type=str, default=None, help="Date (YYYY-MM-DD). Default: today.")
    parser.add_argument("--voice", type=str, default="en-US-GuyNeural", help="edge-tts voice. Try en-US-JennyNeural for female.")
    parser.add_argument(
        "--sync-to",
        type=str,
        default=None,
        help="Copy MP3 to this folder (e.g. OneDrive, Google Drive, iCloud). Example: C:\\Users\\You\\OneDrive\\AI-Digest",
    )
    args = parser.parse_args()

    if args.date:
        try:
            digest_date = datetime.strptime(args.date, "%Y-%m-%d")
        except ValueError:
            raise SystemExit("Invalid --date. Use YYYY-MM-DD.")
    else:
        digest_date = datetime.now(timezone.utc)

    # Prefer narrative (extracted, synthesized) over bullet-point summary
    narrative_path = DIGEST_DIR / f"{digest_date.strftime('%Y-%m-%d')}-narrative.md"
    summary_path = DIGEST_DIR / f"{digest_date.strftime('%Y-%m-%d')}-notebooklm.md"
    if narrative_path.exists():
        summary_path = narrative_path
    elif not summary_path.exists():
        raise SystemExit(f"Summary not found. Run summarize_ai_digest.py or create narrative.")

    md = summary_path.read_text(encoding="utf-8")
    speech_text = markdown_to_speech_text(md)

    # edge-tts is async; use sync wrapper
    try:
        import asyncio
        import edge_tts
    except ImportError:
        raise SystemExit("Install edge-tts: pip install edge-tts")

    out_path = DIGEST_DIR / f"{digest_date.strftime('%Y-%m-%d')}-summary.mp3"

    async def generate():
        communicate = edge_tts.Communicate(speech_text, args.voice)
        await communicate.save(str(out_path))

    asyncio.run(generate())

    if args.sync_to:
        import shutil
        sync_dir = Path(args.sync_to)
        sync_dir.mkdir(parents=True, exist_ok=True)
        dest = sync_dir / out_path.name
        shutil.copy2(out_path, dest)
        print(f"Synced to {dest} (will appear on your phone via cloud sync)")

    print(f"Wrote {out_path}")
    print("Transfer to your phone and listen during your commute.")


if __name__ == "__main__":
    main()
