# AI Daily Digest Automation

A self-contained workflow that turns high-signal AI and product newsletters into a daily reading and listening pipeline.

## What it does

- Fetches recent posts from a curated set of RSS feeds
- Builds a daily markdown digest
- Prioritizes the digest into a NotebookLM-ready summary
- Converts the summary or narrative into MP3 for commute listening
- Optionally emails a link to the generated MP3
- Includes a GitHub Actions workflow for scheduled runs

## What I personally built

- RSS ingestion and digest generation in Python
- Relevance prioritization and summary formatting for AI/product content
- Text-to-speech generation for audio playback
- Email delivery flow using Resend
- Scheduled automation with GitHub Actions

## Repo structure

```text
.
├── .github/workflows/fetch-ai-digest.yml
├── examples/
├── output/
├── requirements.txt
└── scripts/
```

## Setup

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## Usage

### 1. Fetch a digest

```bash
python scripts/fetch_ai_digest.py
```

### 2. Build a prioritized summary

```bash
python scripts/summarize_ai_digest.py
```

### 3. Generate audio

```bash
python scripts/text_to_speech_digest.py
```

### 4. Optional: send email with MP3 link

```bash
export RESEND_API_KEY=re_xxx
export DIGEST_EMAIL=you@example.com
export REPO_RAW=https://raw.githubusercontent.com/YOUR_GITHUB_USERNAME/ai-daily-digest-automation/main/output
python scripts/send_digest_email.py
```

## Sample outputs

The `examples/` folder includes a real generated set:

- `2026-03-07.md`
- `2026-03-07-notebooklm.md`
- `2026-03-07-narrative.md`
- `2026-03-07-summary.mp3`

## GitHub Actions

The included workflow runs the digest pipeline on a schedule. Before enabling it, update any required secrets and verify the output path matches your repo setup.

## Dependencies

- `feedparser`
- `edge-tts`
- `resend`

## Notes

- Generated files are written to `output/`
- If you want email delivery to point at GitHub-hosted files, set `REPO_RAW` to your repo's raw output path
- The workflow can be adapted to commit generated output back to the repository
