# HULK Handoff

**Trigger:** At end of session when switching devices or resuming work later

**Platforms:** macOS, iOS, cross-device (via iCloud, Telegram, email)

**MCP Required:** No

## What It Does

End-of-session handoff coach for multi-device HULK workflows. Captures session context, code changes, decisions made, next steps, and outstanding questions. Generates a handoff document that syncs to your other devices — you pick up exactly where you left off without re-explaining.

## How to Use

1. Near end of session, say: "Create a HULK handoff"
2. Claude summarizes: what you worked on, code committed, decisions made, blockers, next 3 steps
3. Claude saves to a timestamped file and syncs via iCloud or Telegram
4. Pick up on your iPad/iPhone/other Mac with full context

## Notes

- Handoff format: Markdown with sections for context, commits, blockers, and next steps
- Sync options: iCloud Drive (automatic), Telegram bot (manual trigger), email (fallback)
- Session length: best used after 2+ hour sessions or when context is complex
- Information density: capture enough to skip re-reading docs, not so much it's overwhelming
- Decision log: include why you chose A over B — helps you debug decisions later
- Blocker tracking: list what's stuck and what you need help with
- Next session: first message should reference last handoff (Claude will find it)
- Privacy: don't include credentials or sensitive data; use placeholders

---

**Created:** Nate (Ceepeezee), July 2026
**Last updated:** July 2026
**Status:** Production