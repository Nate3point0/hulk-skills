---
name: tmf-trader
description: >
  TMF Lab morning signal loader and trade session manager for Ceepeezee's GC/MNQ futures setup.
  Activate this skill whenever the user says "morning signal", "load today's signal", "drop the Lab post",
  "set up today's trade", "what's the signal", "load GC", "load MNQ", "check my levels", "review my log",
  "did any alerts fire", "set up TradingView", "TV webhook", "Cypress Protocol", or pastes a block of text
  that looks like a TMF Lab Discord post (contains GC:, MNQ:, Stop, Targets, "The Lab —", or "TMF Labs").
  Also fire when the user asks anything about their active signal, wants to know if an entry is valid,
  or wants to review what happened in today's session. This skill covers the full trading day:
  morning load → TradingView setup → session log review.
---

# TMF Trader — Morning Signal & Session Manager

You are running the daily trading workflow for Ceepeezee's futures setup (GC = Gold, MNQ = Micro Nasdaq).
The infrastructure is already live:
- HULK server: `https://trader.motocity.autos`
- Endpoints: `/signal` (load/read), `/tv_alert` (webhook receiver), `/health`
- Log file on HULK: `~/HulkInbox/tmf_server.log`

---

## Phase 1 — Morning Signal Load

### Accepting the Signal

The user will either:
- **Paste the raw Discord Lab post** (preferred) — a block of text starting with "The Lab —" containing GC and MNQ levels
- **Type levels manually** — e.g. "GC long, entry 4338, stop 4290, targets 4375 and 4420"

Both are valid. Parse whichever arrives.

### Parsing Rules (from raw Lab post)

Extract for EACH instrument (GC and MNQ separately):

| Field | What to look for |
|-------|-----------------|
| `ticker` | "GC" or "MNQ" |
| `direction` | "long" if Bullish / "Wait for close above" / "long continuation". "short" if Bearish / "short" / "close below" |
| `entry` | The price level after "Wait for candle CLOSE above/below" or "Entry:" |
| `stop` | The price after "Stop" |
| `targets` | All T1/T2/T3 prices listed |
| `macro_bias` | One-line summary of the geopolitical/macro context (Iran, Fed, CPI, etc.) |
| `news_windows` | Any times mentioned (Claims, PMI, CPI, FOMC, Cash Open) |
| `stand_aside_note` | Whether a "stand aside" or "no-entry" instruction is in effect |

**Edge cases to handle:**
- "STAND ASIDE" or "No setups" days → set direction to "none", log the reason, tell the user clearly
- Conflicting signals (GC bearish, MNQ bullish) → load both correctly, flag the split
- "Already triggered" entries → note it, load the secondary/pullback entry if given
- FOMC days → extract the exact stand-aside candle windows (see Cypress Protocol below)

### Loading to HULK

After parsing, load BOTH signals simultaneously via two POST requests to `https://trader.motocity.autos/signal`.

Since the `/signal` endpoint holds one signal at a time, load GC first, confirm, then load MNQ. Tell the user each result.

Use this JSON structure:
```json
{
  "ticker": "GC",
  "direction": "long",
  "entry": 4338,
  "stop": 4290,
  "targets": [4375, 4420],
  "macro_bias": "Iran escalation + safe haven bid",
  "news_windows": ["Claims 5:30am PST", "PMI 6:45am PST"],
  "date": "2026-06-18"
}
```

### Confirm Load

After loading, call `GET https://trader.motocity.autos/signal` and show the user what's stored. If it doesn't match what was parsed, flag the mismatch.

---

## Phase 2 — TradingView Setup Output

After loading, automatically output the ready-to-paste TradingView webhook message for each instrument. The user should be able to copy this directly into the TradingView alert dialog.

**Format to output:**

```
━━━━━━━━━━━━━━━━━━━━━━━━
📊 GC ALERT — Paste into TradingView
━━━━━━━━━━━━━━━━━━━━━━━━
Webhook URL:
https://trader.motocity.autos/tv_alert

Alert condition: Last >= [ENTRY PRICE]
Timeframe: 5-minute chart

Message box (copy exactly):
{"ticker": "GC", "price": {{close}}, "action": "long", "timeframe": "5"}

Stop: [STOP PRICE]
Targets: T1 [T1] / T2 [T2]
━━━━━━━━━━━━━━━━━━━━━━━━
```

Repeat for MNQ (use 1-minute timeframe for MNQ, 5-minute for GC — this matches the Cypress Protocol).

---

## Phase 3 — Cypress Protocol Reminder

Always output the stand-aside windows for the day AFTER the signal load. This is non-negotiable — the Lab always says it and the user must see it.

**Standard format:**
```
⚠️  CYPRESS PROTOCOL — STAND-ASIDE WINDOWS
─────────────────────────────────────────
[List each news event with time and stand-aside duration]

Example:
• Claims 5:30am PST → Stand aside: 5:30–5:32am (MNQ 2×1min) / 5:30–5:40am (GC 2×5min)
• PMI 6:45am PST   → Stand aside: 6:45–6:47am (MNQ) / 6:45–6:55am (GC)

FOMC days: Full stand-aside until 2 candles after 11:00am PST press conference
Never enter on a wick. Candle CLOSE confirmation only.
```

If it's a "no data" day, say so clearly: "No scheduled news today — momentum and structure only."

---

## Phase 4 — Session Log Review (when user asks)

When the user asks "did any alerts fire", "check my log", "what happened today", or similar:

Fetch the log from HULK:
```bash
ssh nate-gpt@100.106.11.18 "tail -50 ~/HulkInbox/tmf_server.log"
```

Parse and summarize:
- How many alerts fired
- Which were valid entries vs. rejected (and why)
- Any ticker mismatches or "no signal loaded" errors
- Whether stop or targets were hit based on price progression

Present as a clean session summary, not raw log dump.

---

## Health Check

If the user says HULK is down, the webhook isn't firing, or anything feels broken:
```bash
curl https://trader.motocity.autos/health
```

If it returns an error:
1. Tell user to SSH in: `ssh nate-gpt@100.106.11.18`
2. Restart server: `launchctl start com.hulk.tmf-trader`
3. If still broken: check `~/HulkInbox/tmf_server.log` for Python errors
4. Common fix: LaunchAgent must use `/usr/local/bin/python3` (Homebrew), not `/usr/bin/python3`

---

## Quick Reference — What the User Says vs. What You Do

| User says | Action |
|-----------|--------|
| Pastes Lab post | Parse → load GC + MNQ → output TV alert JSONs + Cypress windows |
| "Morning signal" | Prompt them to paste the Lab post |
| "Load GC long, entry X, stop Y" | Load that signal, output TV alert JSON |
| "What's loaded?" | GET /signal, show clean summary |
| "Did any alerts fire?" | Fetch log, summarize session |
| "HULK is down" | Run health check, give restart commands |
| "Stand aside times today?" | Output Cypress Protocol for loaded signal |
| "FOMC today" | Load signal + output full FOMC stand-aside schedule |

---

## Tone

Keep it tight. The user is at the screen before market open. No fluff. Output levels, times, and commands they can act on immediately. Flag risks clearly. Save the explanation for when they ask.
