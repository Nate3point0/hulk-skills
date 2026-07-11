---
name: hulkinbox-intake
description: Use this skill for anything involving HulkInbox — the file drop zone and intake system for the Hulk server. Triggers on: HulkInbox, iPhone shortcut, Send to Hulk, file intake, drop zone, Google Drive sync, iOS Share Sheet, mobile to server, device to Hulk, file ingestion, brain dump, data intake.
---

# HulkInbox Intake System

## What HulkInbox Is
A Google Drive folder acting as the universal drop zone — any device, any app, any content type can land here. The watcher script picks it up, routes it into BrainVault, and the server processes it.

## HulkInbox Location
```
Google Drive: My Drive / HulkInbox/
Local path on Hulk: ~/My Drive (motocityfix@gmail.com)/HulkInbox/
```

**Important**: HulkInbox lives OUTSIDE the BrainVault vault folder. It's the loading dock, not the library.

## Folder Structure
```
HulkInbox/
├── PROMPTS/       # AI prompts, Claude instructions, agent configs
├── NOTES/         # Quick text notes, ideas, brain dumps
├── FILES/         # Documents, PDFs, code files, spreadsheets
├── AUDIO/         # Voice memos (to be transcribed)
├── LINKS/         # URLs saved from browser or apps
└── IMAGES/        # Screenshots, photos to be processed
```

## iOS "Send to Hulk" Shortcut

### What it does
Routes content from any iOS app through the Share Sheet into the correct HulkInbox subfolder via Google Drive.

### Shortcut Logic
```
Trigger: Share Sheet from any app
↓
Detect content type:
  - URL → HulkInbox/LINKS/
  - Text/Note → HulkInbox/NOTES/
  - PDF/Doc → HulkInbox/FILES/
  - Audio → HulkInbox/AUDIO/
  - Image → HulkInbox/IMAGES/
↓
Generate filename: [TYPE]-YYYYMMDD-HHMMSS.[ext]
↓
Save to Google Drive / HulkInbox / [subfolder]/
↓
(Optional) Send confirmation notification
```

### Shortcut Setup Steps
1. Open iOS Shortcuts app
2. New Shortcut → Add to Share Sheet
3. Action: "Get Type of Input"
4. Branch on type → save to correct Google Drive subfolder
5. Use "Save File" action pointing to Google Drive/HulkInbox/[subfolder]/
6. Add to Share Sheet: Settings → Shortcuts → Show in Share Sheet

## Watcher (CURRENT — verified 2026-05-22)

> The old `hulk_watcher.py` (prefix-based routing into AI-PROMPTS/SOPs/etc.) is
> RETIRED. The live system is the autonomous layer below. Don't trust older docs.

- **Script:** `/Users/nate-gpt/hulk/autonomous-layer/watcher.py` (Python `watchdog`, native FSEvents — confirmed working even on the Google Drive mount)
- **Config:** `/Users/nate-gpt/hulk/autonomous-layer/config.yml`
- **LaunchAgent:** `com.hulk.watcher` — restart with `launchctl kickstart -k gui/$(id -u)/com.hulk.watcher`
- **Logs:** `~/hulk-system/logs/watcher.stdout.log` and `watcher.stderr.log`

### Watched paths (roles)
- **canonical** = `/Volumes/HULK-STORAGE/HULK-INBOX` — classified + moved into taxonomy
- **feeders** = Google Drive `HulkInbox/{NOTES,FILES,IMAGES,LINKS,AUDIO,PROMPTS}` — files RELOCATED into canonical, then classified. (`_processed` is deliberately NOT a feeder.) This is the iPhone "Send to Hulk" path.
- **observed** = `/Volumes/HULK-STORAGE/OBSIDIAN-VAULT/00-INBOX` — dedupe-hash audit only; never moved

### Routing = config-driven classifier (by extension, NOT filename prefix)
Destination root: `/Volumes/HULK-STORAGE/HULK-KNOWLEDGE-CENTER/BrainVault`
```
.md/.docx/.pdf/.xlsx/.pptx → 10-Knowledge
.py/.js/.ts/.go/.rs/.sh    → 20-Projects
.mov/.mp4/.wav/.heic/...   → 30-Archive
screenshots                → 30-Archive
unknown / default          → 50-Review (human triage)
duplicates                 → 40-Quarantine (never deleted)
```
Safety: `destructive_ops: false`, writes confined to BrainVault, kill-switch `/tmp/hulk.stop`.

## Multi-Device Intake Flow

### From iPhone
Share Sheet → Google Drive → HulkInbox → watcher → BrainVault

### From MacBook Pro (M4)
Drag to Google Drive folder → HulkInbox → watcher → BrainVault
OR: Direct add to BrainVault (already synced via Google Drive)

### From Claude Code (on Hulk)
Script outputs → drop directly to BrainVault/00-Inbox/ (skip HulkInbox)

### From AI Proxy Conversations
Auto-logged to BrainVault/00-Inbox/ directly by proxy.py

## Google Drive Sync Notes
- Google Account: motocityfix@gmail.com
- Do NOT use iCloud (consistently full)
- Sync client must be running on Hulk for watcher path to be valid
- Verify sync path: `ls ~/My\ Drive\ \(motocityfix@gmail.com\)/HulkInbox/`

## Brain Dump Protocol
For massive data extraction sessions (past files, old projects, notes):

1. **Organize first** — sort files by rough category before dropping
2. **Name them right** — add prefix before dropping so watcher routes correctly
3. **Batch by type** — do all PROMPTS, then all SOPs, etc.
4. **Don't rush the sync** — Google Drive needs time; large batches stagger

### Quick rename script for brain dumps
```bash
# Add prefix to all .md files in a folder
for f in ~/Desktop/old-notes/*.md; do
  mv "$f" "$(dirname $f)/TOPIC-$(basename $f)"
done
```

## Processing Queue Status
Check what's pending in HulkInbox:
```bash
ls -la ~/My\ Drive\ \(motocityfix@gmail.com\)/HulkInbox/
ls -la ~/My\ Drive\ \(motocityfix@gmail.com\)/HulkInbox/_processed/
```

Check watcher log:
```bash
tail -50 ~/hulk-system/logs/watcher.stdout.log
```
