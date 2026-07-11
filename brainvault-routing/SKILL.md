---
name: brainvault-routing
description: Use this skill for anything involving the BrainVault Obsidian vault — folder structure, frontmatter injection, file routing, naming conventions, watcher behavior, or vault organization. Triggers on: BrainVault, Obsidian, vault, frontmatter, 00-Inbox, ME, SOPs, TOPICS, AI-PROMPTS, SETUP, note routing, markdown capture.
---

# BrainVault Routing & Structure

## Vault Location
```
~/My Drive (motocityfix@gmail.com)/ObsidianVault/BrainVault/
```
Synced via Google Drive to all devices.

## Folder Structure
```
BrainVault/
├── 00-Inbox/          # Auto-drop zone — all AI logs and unprocessed files land here
├── ME/                # Personal context, identity, goals, North Star docs
├── SOPs/              # Standard operating procedures, repeatable workflows
├── TOPICS/            # Research, concepts, domain knowledge
├── AI-PROMPTS/        # Saved prompts, agent instructions, Claude context blocks
└── SETUP/             # Infrastructure docs, configs, server architecture notes
```

## Routing Logic (Filename-Based)
The watcher routes files based on filename prefixes and keywords:

| Filename Pattern | Routes To |
|-----------------|-----------|
| `PROMPT-*`, `prompt-*` | `AI-PROMPTS/` |
| `SOP-*`, `sop-*`, `workflow-*` | `SOPs/` |
| `ME-*`, `bio-*`, `goal-*`, `northstar*` | `ME/` |
| `SETUP-*`, `config-*`, `infra-*` | `SETUP/` |
| `TOPIC-*`, `research-*`, `concept-*` | `TOPICS/` |
| Everything else / unmatched | `00-Inbox/` (default) |

## Frontmatter Injection
Every file entering the vault gets frontmatter injected:

```yaml
---
date_added: 2024-01-15
source: hulk_watcher | iphone_shortcut | manual | proxy_log
tags: []
status: inbox
routed_to: 00-Inbox
---
```

### Source Tags
- `hulk_watcher` — dropped into HulkInbox folder and picked up by watcher
- `iphone_shortcut` — came from iOS Share Sheet via HulkInbox
- `proxy_log` — auto-logged by FastAPI proxy from AI conversation
- `manual` — directly added to vault

## Proxy Auto-Logging
The FastAPI proxy logs every AI conversation to `00-Inbox/` with this format:

```
AI-LOG-YYYYMMDD-HHMMSS-[conversation-id].md
```

Frontmatter includes:
```yaml
---
date: 2024-01-15T14:32:00
model: claude-3-haiku
conversation_id: abc123
source: proxy_log
tokens_used: 847
cost_usd: 0.0002
status: inbox
---
```

## Key Files in ME/
- `HULK-NORTHSTAR.md` — the directional document; what you're building and where you're headed
- `CONTEXT-BLOCK.md` — the ready-to-paste Claude context block for cold-starting sessions

## Naming Conventions
- Use UPPERCASE prefix for routing signals: `PROMPT-`, `SOP-`, `SETUP-`
- Use kebab-case after prefix: `SOP-ollama-coldstart.md`
- Dates in filenames: `YYYYMMDD` format
- No spaces in filenames — use hyphens

## Watcher Script (hulk_watcher.py)
Watches HulkInbox for new files and routes them into the vault.

### What it does
1. Detects new file in HulkInbox
2. Reads filename to determine target folder
3. Injects frontmatter
4. Copies to correct BrainVault subfolder
5. Optionally deletes from HulkInbox after successful routing

### Trigger it manually
```bash
python3 ~/hulk_watcher.py
```

### Run as daemon
```bash
nohup python3 ~/hulk_watcher.py > ~/logs/watcher.log 2>&1 &
```

## HulkInbox Location
```
~/My Drive (motocityfix@gmail.com)/HulkInbox/
```
(Separate from vault — acts as the drop zone, not stored inside BrainVault)

### HulkInbox Subfolder Structure
```
HulkInbox/
├── PROMPTS/       # AI prompts from iPhone or other devices
├── NOTES/         # Quick notes and ideas
├── FILES/         # Documents, PDFs, code files
├── AUDIO/         # Voice memos
└── LINKS/         # URLs and references
```

## Adding to Vault — Manual Quick Add
For files you want to route manually without the watcher:
1. Name the file with the correct prefix
2. Drop into HulkInbox (watcher picks up) OR
3. Drop directly into the correct BrainVault subfolder

## Obsidian Sync Notes
- Synced via Google Drive (iCloud consistently full — do not use iCloud)
- Google account: motocityfix@gmail.com
- Changes sync across: Hulk (Mac Mini), MacBook Pro M4, iPhone, iPad
