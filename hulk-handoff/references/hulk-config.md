# Hulk Server — Config Reference

## Identity
- **Name:** Hulk
- **Hardware:** Mac Mini 2018 Intel
- **Role:** Primary compute engine, AI proxy, BrainVault host

## Network
- **Tailscale IP:** 100.106.11.18
- **Local network:** accessible via Tailscale mesh from any device
- **Devices on mesh:** Mac Mini (Hulk), MacBook Pro x2, iPhone

## Services & Ports
| Service | Port | Notes |
|---|---|---|
| FastAPI Proxy | 4000 | Routes to OpenRouter, main AI endpoint |
| Ollama | 11434 | Local models: phi3.5, mistral, llama3.2 |
| VAULTMIND Dashboard | 5005 | Browser dashboard |
| SSH | 22 | Standard, use via Termius |

## Key Paths
| Path | Purpose |
|---|---|
| `~/BrainVault/` | Main Obsidian vault |
| `~/BrainVault/00-Inbox/` | Auto-routing inbox for new notes |
| `~/BrainVault/ME/` | Personal context and SOPs |
| `~/BrainVault/AI-PROMPTS/` | Saved prompts and skill files |
| `~/.claude/skills/` | Claude Code skill files |
| `~/logs/` | Server logs (tail for monitoring) |

## Auto-Start Services (LaunchAgents)
- FastAPI proxy on port 4000
- hulk_watcher.py (BrainVault inbox watcher using watchdog)
- Ollama

## Health Check
```bash
hulk-status          # Custom command — shows all service statuses
ping 100.106.11.18   # Quick reachability check
curl localhost:4000/health  # FastAPI health endpoint
```

## tmux Conventions
- Main session: `tmux new-session -A -s hulk-work`
- Always attach with `-A` flag (creates if not exists, attaches if exists)
- Named windows recommended: `tmux rename-window proxy`, `tmux rename-window vault`, etc.

## OpenRouter
- API keys stored in FastAPI proxy config (not OAuth tokens)
- Models routed through OpenRouter, selected per request
- Proxy endpoint: `http://100.106.11.18:4000/v1/chat/completions`

## BrainVault Sync
- Synced via Google Drive (motocityfix@gmail.com)
- hulk_watcher.py monitors 00-Inbox and auto-routes files based on frontmatter tags
- New session logs go to: `~/BrainVault/00-Inbox/YYYY-MM-DD-[topic].md`
