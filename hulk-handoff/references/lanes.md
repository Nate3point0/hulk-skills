# Handoff Lanes — When to Use What

## Lane A: Dispatch → Hulk (Primary)

**Use when:**
- The task is well-defined: "implement X from @TODO.md"
- You don't need to watch it run
- You're on the go and can't keep a terminal open
- The output is a file, a deployment, or a code change

**How it works:**
1. Open Claude mobile app
2. Go to the Dispatch thread
3. Paste the generated Dispatch Prompt
4. Hulk picks it up and processes autonomously
5. (Future) Telegram bot notifies you when done

**Pro tips:**
- Always reference filenames in the Dispatch prompt — Hulk needs anchors
- Tell Hulk exactly where to log results (BrainVault path)
- If the task has multiple phases, break them into separate Dispatch messages

---

## Lane B: Termius SSH → Hulk (Active Sprint)

**Use when:**
- You need to run tests interactively
- Debugging a live issue
- Installing dependencies or configuring services
- You want to watch logs in real time

**How it works:**
1. Open Termius on iPhone or MacBook
2. Connect to saved Hulk host (100.106.11.18)
3. Run: `tmux new-session -A -s hulk-work`
4. Navigate to project folder and run commands manually

**Stability hacks:**
- **Mosh**: Enable in Termius settings — survives network drops and mobile switching
- **Location Tracking**: Enable in Termius iPhone settings — prevents iOS from killing background SSH after 30 seconds
- **tmux**: Always use it — if connection drops, your session stays alive on Hulk; reconnect and attach

---

## Lane C: Both (Parallel)

**Use when:**
- Task is urgent and complex
- You want Dispatch to do the build while you monitor via SSH
- You're testing something that might need manual intervention

**How it works:**
- Send Dispatch prompt for the main build task
- SSH in via Termius to tail logs: `tail -f ~/logs/hulk.log`
- If Hulk gets stuck, intervene directly in the SSH session

---

## Lane D: Future — Telegram Bot Notifications

**Status:** Not yet active. Set up when ready.

**What it will do:**
- Push notification to your phone when Hulk finishes a task
- Alert if Hulk errors out and needs attention
- Optional: send progress updates mid-task

**Setup (when ready):**
1. Create a Telegram bot via @BotFather
2. Get your bot token and chat ID
3. Add to Hulk's FastAPI server as a notification endpoint
4. Call it at the end of any Dispatch task:
   ```python
   import requests
   requests.post(f"https://api.telegram.org/bot{TOKEN}/sendMessage",
     json={"chat_id": CHAT_ID, "text": "✅ Task complete: [task name]"})
   ```

Until Telegram is active, check back manually via Termius or Claude mobile.
