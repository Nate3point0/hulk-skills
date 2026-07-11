---
name: hulk-health-check
description: Run a fast read-only audit across the Hulk Mac Mini stack — LaunchAgents (proxy, watcher, orchestrator, command-center, etc.), Tailscale peers, the iPhone→Drive→BrainVault inbox pipeline, disk/memory/load, brew outdated formulae split into safe vs risky, and the scheduled risky-upgrade maintenance LaunchAgent. Surfaces issues as a green/yellow/red scoreboard and offers one-click fixes for the safe ones. Use whenever Ceepeezee wants to spot-check the server. Triggers on "hulk health check", "check hulk", "audit hulk", "is hulk ok", "weekly check", "scan hulk", "run health check", "system check", "everything working?", "hulk status", "is the system good", "make sure hulk is healthy", "what is broken on hulk".
---

# Hulk Health Check

A read-only sweep of the Hulk Mac Mini that produces a compact scoreboard.
Designed to replace the manual "is everything okay?" dance. Runs in well under a minute.

## When activated

1. **Run the scan** — bundled script, structured output:
   ```
   /bin/zsh /Users/nate-gpt/.claude/skills/hulk-health-check/check.sh
   ```
   Output is `CATEGORY STATUS key=value` lines under six headers: `SERVICES`,
   `NETWORK`, `INBOX`, `RESOURCES`, `UPDATES`, `MAINTENANCE`. Statuses are
   `OK`, `WARN`, `FAIL`, `INFO`.

2. **Render a scoreboard for the user.** One line per category with an emoji
   (✅ OK / ⚠️ WARN / ❌ FAIL / ℹ️ INFO) and the most relevant facts. Do NOT
   paste the raw script output — translate it into something scannable.

   Example shape (don't copy verbatim — adapt to what the scan actually shows):
   ```
   HULK HEALTH — 2026-05-26 22:14 PDT

   ✅ SERVICES     proxy 200, ollama 200, watcher OK, all com.hulk.* loaded
   ⚠️ NETWORK      MacBook offline (last seen 14m); iPhone + Mac Mini active
   ✅ INBOX        Drive feeders clean; last enqueue 01:12 (Telegram .txt)
   ✅ RESOURCES    HULK-STORAGE 58% used / 392G free; load 2.3
   ℹ️ UPDATES     4 brew outdated (0 safe, 4 risky — covered by 03:00 maintenance)
   ✅ MAINTENANCE risky-upgrade scheduled at 03:00 (one-shot)

   Action items:
   - Reconnect Tailscale on the MacBook (off-Hulk task)
   ```

3. **Highlight anything red or yellow first.** If everything is green, say so
   plainly — don't manufacture noise.

## Auto-fix (do these without asking, only on a clear signal)

- LaunchAgent loaded but `last_exit != 0` and *not* currently running: try one
  `launchctl kickstart -k gui/$(id -u)/<label>`, then re-run the scan to confirm.
- A *single* unambiguously stale `.DS_Store` in an otherwise-empty drop folder
  the user has asked to clean up.
- Dead symlinks under `~/Desktop` or other tidy targets.

## Ask first (these touch shared infra)

- Restarting `com.hulk.proxy` (1–2s blip — usually fine, but confirm).
- Anything that bounces Tailscale (drops the Termius session).
- `brew upgrade` of `ollama`, `tailscale`, `python@*`, `node@*` — these belong
  in the scheduled `com.hulk.maintenance.risky-upgrade` LaunchAgent at 03:00.
  If that LaunchAgent is missing, offer to recreate it from
  `/Volumes/HULK-STORAGE/00-SYSTEM/maintenance/risky-upgrade.sh`.
- Rescuing a stuck file in a Drive feeder (use `cp` then `rm` of the Drive
  source — the watcher's `_relocate_to_canonical` is fixed but a stuck file
  needs a manual nudge because `touch` on a Drive virtual file doesn't fire
  FSEvents).

## Never

- Delete user data in `/Volumes/HULK-STORAGE/HULK-INBOX/`, `HulkInbox/_processed/`,
  or anywhere under BrainVault.
- Empty a Drive feeder folder wholesale.
- Touch the Tailscale admin console (web-only).
- Modify `~/hulk/autonomous-layer/config.yml` without showing the diff and
  asking — that file controls the watcher's safety guardrails.

## What "good" looks like

- Every `com.hulk.*` LaunchAgent either has a live PID *or* shows `last_exit=0`
  (idle is fine for the cron-style ones).
- `proxy_health=200` AND `ollama=200`.
- `drive_feeders_clean=true`.
- Mac Mini + iPhone show as `connected` on Tailscale.
- `RESOURCES` mount usage under 80%.
- `brew_outdated_total` may be nonzero — what matters is whether the **risky**
  ones are covered by a scheduled maintenance LaunchAgent.

## Cadence

Ceepeezee runs this manually — every other day or weekly. **Don't auto-schedule
it without being asked.** If they want a hands-off daily report, offer to wire
up a LaunchAgent that writes the scan output to
`/Volumes/HULK-STORAGE/HULK-KNOWLEDGE-CENTER/BrainVault/99-System/health-YYYY-MM-DD.md`
so it shows up in Obsidian.

## Files

- `check.sh` — the read-only scan script (no flags; just run it).
- Scan reads: `launchctl list`, `tailscale status`, `vm_stat`, `df`, `uptime`,
  `brew outdated`, `~/hulk-system/logs/watcher.stderr.log`, the Drive
  `HulkInbox/` mount, and `~/Library/LaunchAgents/com.hulk.maintenance.*`.

## Related skills

- `hulk-server-ops` — how the FastAPI proxy, Ollama, LaunchAgents, and ports
  are laid out. Load if a deep fix is needed.
- `hulkinbox-intake` — the autonomous-layer watcher + Drive feeders.
- `brainvault-routing` — vault structure for routed files.
