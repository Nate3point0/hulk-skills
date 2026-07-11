#!/usr/bin/env python3
"""
kimi_ingest_watcher.py  (a.k.a. the multi-source ingestion watcher)
--------------------------------------------------------------------
Originally built for Kimi Claw exports, but designed to scale to every
platform you pull files from (Kimi Claw, Notion, Drive, Dropbox, whatever's
next). Rather than hardcoding one source, it watches ANY folder matching:

    HULK-INBOX/FROM-<SOURCE>/_drop/

To onboard a new platform, you don't touch this script — just create:

    HULK-INBOX/FROM-NOTION/_drop/
    HULK-INBOX/FROM-GDRIVE/_drop/
    ...

and drop files in. This script discovers all `FROM-*/_drop/` folders each
poll cycle and routes files the same way regardless of source:

  .md / .txt          -> BrainVault/00-Inbox/          (picked up by the
                                                         existing RAG watcher,
                                                         watch.py, and embedded
                                                         into brainvault.db)
  code files          -> HULK-INBOX/FROM-<SOURCE>/code/
  docs (.pdf/.docx/
        .pptx/.xlsx/
        .csv)         -> HULK-INBOX/FROM-<SOURCE>/documents/
  everything else     -> HULK-INBOX/FROM-<SOURCE>/unsorted/

The source name is preserved in the destination path so you can always
tell where a file originated, even after it's routed.

Files landing under HULK-INBOX/ are still subject to whatever routing/
classification your existing hulk_inbox_watcher.py already does — this
script just makes sure exports get pre-sorted into a sensible subfolder
instead of dumping everything unsorted into BrainVault.

Uses only the Python standard library (no watchdog dependency) via a simple
polling loop, so it will run on any stock Python 3 install on HULK.

State (which files have already been processed) is kept in a small JSON
file next to this script so re-runs / restarts don't reprocess old files.

Run manually (single scan across all sources):
    python3 kimi_ingest_watcher.py

Run as a background loop (default):
    python3 kimi_ingest_watcher.py --daemon

Typical deployment is via the paired launchd plist
(com.hulk.kimi-ingest.plist) which keeps this running across reboots.
"""

import argparse
import json
import shutil
import sys
import time
from datetime import datetime
from pathlib import Path

# ---------------------------------------------------------------------------
# Configuration — adjust these paths if your HULK layout differs.
# ---------------------------------------------------------------------------

HULK_STORAGE = Path("/Volumes/HULK-STORAGE")
HULK_INBOX = HULK_STORAGE / "HULK-INBOX"
BRAINVAULT_INBOX = HULK_STORAGE / "HULK-KNOWLEDGE-CENTER" / "BrainVault" / "00-Inbox"

# If no FROM-<SOURCE> folders exist yet, this default one is created so
# there's always at least a Kimi Claw drop point ready to use.
DEFAULT_SOURCE = "FROM-KIMI-CLAW"

STATE_FILE = Path(__file__).with_name("kimi_ingest_state.json")
LOG_FILE = Path(__file__).with_name("kimi_ingest.log")

POLL_INTERVAL_SECONDS = 15

# Extension -> destination bucket
MARKDOWN_EXTS = {".md", ".markdown", ".txt"}
CODE_EXTS = {
    ".py", ".js", ".ts", ".jsx", ".tsx", ".sh", ".bash", ".zsh",
    ".json", ".yaml", ".yml", ".toml", ".ini", ".cfg",
    ".rb", ".go", ".rs", ".java", ".c", ".cpp", ".h", ".sql",
}
DOC_EXTS = {".pdf", ".docx", ".doc", ".pptx", ".ppt", ".xlsx", ".xls", ".csv"}


# ---------------------------------------------------------------------------
# State handling
# ---------------------------------------------------------------------------

def load_state() -> dict:
    if STATE_FILE.exists():
        try:
            return json.loads(STATE_FILE.read_text())
        except json.JSONDecodeError:
            return {"processed": {}}
    return {"processed": {}}


def save_state(state: dict) -> None:
    STATE_FILE.write_text(json.dumps(state, indent=2))


def log(message: str) -> None:
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    line = f"[{timestamp}] {message}"
    print(line)
    with open(LOG_FILE, "a") as f:
        f.write(line + "\n")


# ---------------------------------------------------------------------------
# Classification
# ---------------------------------------------------------------------------

def classify(path: Path, source_dir: Path) -> Path:
    """Return the destination directory for a given file, scoped to its source."""
    ext = path.suffix.lower()
    if ext in MARKDOWN_EXTS:
        return BRAINVAULT_INBOX
    if ext in CODE_EXTS:
        return source_dir / "code"
    if ext in DOC_EXTS:
        return source_dir / "documents"
    return source_dir / "unsorted"


def discover_source_dirs() -> list[Path]:
    """Find every HULK-INBOX/FROM-<SOURCE>/ folder. Creates the default
    Kimi Claw one if nothing exists yet, so first run always works."""
    HULK_INBOX.mkdir(parents=True, exist_ok=True)
    sources = sorted(d for d in HULK_INBOX.glob("FROM-*") if d.is_dir())
    if not sources:
        default = HULK_INBOX / DEFAULT_SOURCE
        default.mkdir(parents=True, exist_ok=True)
        sources = [default]
    return sources


def ensure_dirs(source_dirs: list[Path]) -> None:
    BRAINVAULT_INBOX.mkdir(parents=True, exist_ok=True)
    for source_dir in source_dirs:
        (source_dir / "_drop").mkdir(parents=True, exist_ok=True)
        (source_dir / "code").mkdir(parents=True, exist_ok=True)
        (source_dir / "documents").mkdir(parents=True, exist_ok=True)
        (source_dir / "unsorted").mkdir(parents=True, exist_ok=True)


# ---------------------------------------------------------------------------
# Core scan/route logic
# ---------------------------------------------------------------------------

def scan_once(state: dict, source_dirs: list[Path]) -> int:
    """Scan every source's _drop/ folder once, route any new files."""
    processed = state.setdefault("processed", {})
    routed = 0

    for source_dir in source_dirs:
        drop_dir = source_dir / "_drop"
        if not drop_dir.exists():
            continue

        for path in sorted(drop_dir.rglob("*")):
            if path.is_dir():
                continue

            key = str(path.resolve())
            mtime = path.stat().st_mtime

            # Skip if we've already handled this exact file+mtime
            if processed.get(key) == mtime:
                continue

            dest_dir = classify(path, source_dir)
            dest_path = dest_dir / path.name

            # Avoid clobbering an existing file with the same name
            if dest_path.exists():
                stem, suffix = path.stem, path.suffix
                ts = datetime.now().strftime("%Y%m%d-%H%M%S")
                dest_path = dest_dir / f"{stem}__{ts}{suffix}"

            try:
                shutil.move(str(path), str(dest_path))
                processed[key] = mtime
                routed += 1
                log(f"[{source_dir.name}] Routed {path.name} -> {dest_dir}")
            except Exception as e:
                log(f"[{source_dir.name}] ERROR moving {path}: {e}")

    if routed:
        save_state(state)

    return routed


def run_daemon() -> None:
    source_dirs = discover_source_dirs()
    ensure_dirs(source_dirs)
    log(f"ingest watcher started. Watching: {[d.name for d in source_dirs]}")
    state = load_state()
    try:
        while True:
            source_dirs = discover_source_dirs()  # pick up newly added sources
            ensure_dirs(source_dirs)
            count = scan_once(state, source_dirs)
            if count:
                log(f"Batch complete: {count} file(s) routed.")
            time.sleep(POLL_INTERVAL_SECONDS)
    except KeyboardInterrupt:
        log("ingest watcher stopped by user.")


def run_once() -> None:
    source_dirs = discover_source_dirs()
    ensure_dirs(source_dirs)
    state = load_state()
    count = scan_once(state, source_dirs)
    log(f"One-shot scan complete: {count} file(s) routed across "
        f"{len(source_dirs)} source(s): {[d.name for d in source_dirs]}")


# ---------------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(description="Kimi Claw ingestion watcher")
    parser.add_argument(
        "--daemon", action="store_true",
        help="Run continuously, polling every %d seconds (default: single scan)"
        % POLL_INTERVAL_SECONDS,
    )
    args = parser.parse_args()

    if args.daemon:
        run_daemon()
    else:
        run_once()


if __name__ == "__main__":
    sys.exit(main())
