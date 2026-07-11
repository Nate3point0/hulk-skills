# Install Checklist

## First-time setup

1. Copy `scripts/ingest_watcher.py` to a persistent location on the server
   (e.g. alongside any existing inbox/classification scripts).
2. Edit the constants at the top of the script for the real deployment:
   - `HULK_STORAGE` — the storage volume root
   - `HULK_INBOX` — where source folders live
   - `BRAINVAULT_INBOX` — where markdown/text should land for indexing
   - Extension sets (`MARKDOWN_EXTS`, `CODE_EXTS`, `DOC_EXTS`) if the
     user's file types differ from the defaults
3. Copy `scripts/launchd_template.plist` to `~/Library/LaunchAgents/`,
   renamed appropriately (e.g. `com.<system>.ingest.plist`), and update:
   - The Python interpreter path (`ProgramArguments[0]`) — use whatever
     venv/interpreter the rest of the system's background services use
   - The script path (`ProgramArguments[1]`)
   - Log file paths (`StandardOutPath`, `StandardErrorPath`)
4. Load the service:
   ```bash
   launchctl load ~/Library/LaunchAgents/<plist-name>.plist
   launchctl list | grep <label>
   ```
5. Confirm the default source folder exists and drop a real test file in:
   ```bash
   ls <HULK_INBOX>/FROM-<SOURCE>/_drop/
   ```
6. Tail the log and confirm the test file gets classified and moved within
   one polling interval (default 15s):
   ```bash
   tail -f <path-to-log>/ingest.log
   ```
7. Confirm the existing indexer (if one exists) picks up anything routed
   to the knowledge-base inbox and actually embeds it — query the vector
   store directly for content from the test file, don't just trust the
   indexer service is "running."
8. Confirm retrieval wiring per `references/rag_bridge_pattern.md` — this
   is the step most often skipped, and the reason "I imported files but my
   AI doesn't use them" complaints happen.

## Onboarding a new source (after first-time setup is done)

No script edits, no plist edits, no restart:

```bash
mkdir -p <HULK_INBOX>/FROM-<NEW_SOURCE_NAME>/_drop
```

Drop files in on the next polling cycle and they'll be classified and
routed identically to every other source, tagged with that source's name
in the destination path so provenance is never lost.

## Common failure points to check if something seems broken

- **Watcher not running**: `launchctl list | grep <label>` — if it's not
  listed, the plist didn't load (check for XML typos, wrong interpreter
  path) or it crashed on startup (check the error log).
- **Files stuck in `_drop/`**: confirms watcher isn't running or errored
  mid-scan. Check the log for exceptions.
- **Files routed but not embedded**: the routing (this skill) and the
  embedding (a separate indexer service) are different systems — confirm
  the indexer is actually watching the destination folder, not just that
  the ingest watcher moved files there successfully.
- **Embedded but AI "doesn't know"**: this is a retrieval-wiring gap, not
  an ingestion gap — see `references/rag_bridge_pattern.md`.
- **Large fraction of files land in "unsorted"**: audit before assuming
  it's fine. Build artifacts, binaries, and cache files are expected here;
  real content with an unusual extension is not, and means the classifier
  needs another extension added.
