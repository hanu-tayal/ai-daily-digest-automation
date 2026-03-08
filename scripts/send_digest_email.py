#!/usr/bin/env python3
"""Send daily digest email with link to MP3.

Requires RESEND_API_KEY env var. Sign up at resend.com (free tier: 100 emails/day).

Run: RESEND_API_KEY=re_xxx python scripts/send_digest_email.py [--date YYYY-MM-DD]
"""

from __future__ import annotations

import argparse
import os
from datetime import datetime, timezone
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
DIGEST_DIR = PROJECT_ROOT / "output"

# GitHub raw URL base (set REPO_RAW to your repo's raw output path after publishing)
REPO_RAW = os.environ.get("REPO_RAW", "https://raw.githubusercontent.com/OWNER/REPO/main/output")


def main() -> None:
    parser = argparse.ArgumentParser(description="Send digest email with MP3 link")
    parser.add_argument("--date", type=str, default=None, help="Date (YYYY-MM-DD). Default: today.")
    parser.add_argument("--to", type=str, default=None, help="Recipient email. Default: from env DIGEST_EMAIL.")
    args = parser.parse_args()

    api_key = os.environ.get("RESEND_API_KEY")
    to_email = args.to or os.environ.get("DIGEST_EMAIL", "hanutayal@gmail.com")

    if not api_key:
        raise SystemExit("Set RESEND_API_KEY. Sign up at resend.com")

    if args.date:
        try:
            digest_date = datetime.strptime(args.date, "%Y-%m-%d")
        except ValueError:
            raise SystemExit("Invalid --date. Use YYYY-MM-DD.")
    else:
        digest_date = datetime.now(timezone.utc)

    mp3_name = f"{digest_date.strftime('%Y-%m-%d')}-summary.mp3"
    mp3_path = DIGEST_DIR / mp3_name
    if not mp3_path.exists():
        raise SystemExit(f"MP3 not found: {mp3_path}. Run text_to_speech_digest.py first.")

    mp3_url = f"{REPO_RAW}/{mp3_name}"
    date_str = digest_date.strftime("%A, %B %d, %Y")

    subject = f"AI Digest — {digest_date.strftime('%Y-%m-%d')}"
    html = f"""
    <p>Your AI digest is ready.</p>
    <p><strong>Listen on your phone:</strong></p>
    <p><a href="{mp3_url}">Download MP3 ({mp3_name})</a></p>
    <p>Or open this link on your phone to stream/download:</p>
    <p><a href="{mp3_url}">{mp3_url}</a></p>
    <p>— AI Digest (GitHub Actions)</p>
    """

    try:
        import resend
    except ImportError:
        raise SystemExit("Install resend: pip install resend")

    resend.api_key = api_key
    r = resend.Emails.send(
        {
            "from": "AI Digest <onboarding@resend.dev>",
            "to": [to_email],
            "subject": subject,
            "html": html,
        }
    )
    print(f"Sent to {to_email}. Id: {r.get('id', 'ok')}")


if __name__ == "__main__":
    main()
