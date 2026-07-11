---
name: hulk-two-pass-review
description: >
  Implements an adversarial two-pass AI code review system on the Hulk self-hosted FastAPI proxy
  (Mac Mini, Tailscale IP: 100.106.11.18, port 4000). Claude writes code → a second independent
  model (Kimi K2 via OpenRouter) reviews it cold — solving the "AI grading its own homework"
  problem without any paid third-party plugins.

  Activate this skill whenever the user says: "add review to Hulk", "two-pass review", "adversarial
  review", "have Kimi review Claude's code", "cross-model review", "code review endpoint", or any
  variant of wanting a second AI model to check code that a first model generated. Also activate
  when the user wants to deploy, modify, or extend the /review endpoint on their Hulk proxy, or
  asks about multi-model review workflows. If the user asks about getting better code quality from
  their AI setup, or about the "sycophancy problem" in AI coding tools, this skill is relevant.
---

# Hulk Two-Pass Review Skill

This skill builds and deploys an adversarial two-pass code review system on the Hulk infrastructure.
The architecture mirrors what Cursor 3 + Codex plugin achieves commercially — but runs entirely on
your self-hosted stack with zero extra subscriptions.

## How It Works

```
User Prompt
    │
    ▼
Pass 1 ─► Claude (anthropic/claude-sonnet-4-5)   ─► writes code/output
    │
    ▼
Pass 2 ─► Kimi K2 (moonshotai/kimi-k2)           ─► reviews cold, no context share
    │
    ▼
Single JSON response: written_output + review_output + verdict
```

The key insight: the reviewer never sees the writing session. It only gets the original prompt + the
finished output. This prevents the model from anchoring on the writer's reasoning — it evaluates
purely on result quality.

---

## What Gets Deployed

Three deliverables, always generated together:

| File | Purpose |
|---|---|
| `hulk_two_pass_review.py` | FastAPI router — drop into existing proxy |
| `test_review.py` | CLI verification script |
| `HulkReviewDashboard.jsx` | React split-pane UI for review visualization |

---

## Generating the Files

When the user asks to implement or regenerate this system, produce all three files as described in
`references/implementation.md`. Always generate them as a complete set — partial delivery leads to
integration confusion.

Key generation rules:
- The FastAPI router must use `APIRouter`, not mount directly to `app` — the user has an existing proxy
- OpenRouter auth reads from `os.getenv("OPENROUTER_API_KEY")` — never hardcode keys
- Default writer: `anthropic/claude-sonnet-4-5` | Default reviewer: `moonshotai/kimi-k2`
- Both models are overridable per-request via the request body
- The dashboard connects to `http://100.106.11.18:4000` — make this visible and easy to change

---

## Review Focus Modes

Four modes ship by default. Each injects a different system prompt to the reviewer:

| Mode | What It Tests |
|---|---|
| `general` | Correctness, maintainability, error handling, production readiness. Verdicts: APPROVE / APPROVE WITH NOTES / REQUEST CHANGES |
| `security` | Auth flaws, injection, data exposure, race conditions, insecure defaults. Severity buckets: CRITICAL / HIGH / MEDIUM / LOW |
| `logic` | Off-by-one errors, unhandled edge cases, broken control flow, algorithmic bugs |
| `performance` | N+1 queries, blocking I/O in async, memory leaks, missed caching |

The user can add custom modes by extending the `REVIEW_PROMPTS` dict in `hulk_two_pass_review.py`.

---

## Deployment Steps

When deploying for the first time, walk the user through these steps:

**1. Transfer the file to Hulk**
```bash
scp hulk_two_pass_review.py user@100.106.11.18:~/hulk-proxy/
```

**2. Mount the router — add 2 lines to `main.py`**
```python
from hulk_two_pass_review import router as review_router
app.include_router(review_router)
```

**3. Restart the server**
```bash
# If using uvicorn with --reload, it picks up automatically
# Otherwise:
pkill -f uvicorn && uvicorn main:app --host 0.0.0.0 --port 4000 --reload
```

**4. Verify**
```bash
python3 test_review.py --focus security
# Expect: written_output + review_output + a verdict field in the response
```

If the user's proxy structure differs from the above (e.g., different filename or app structure),
read their existing `main.py` via SSH before generating the mount instructions.

---

## API Reference

### `POST /review`

```json
{
  "prompt": "Write a function that...",
  "write_model": "anthropic/claude-sonnet-4-5",
  "review_model": "moonshotai/kimi-k2",
  "review_focus": "security",
  "system_prompt": null
}
```

All fields except `prompt` are optional — defaults are pre-configured.

**Response:**
```json
{
  "writer_model": "anthropic/claude-sonnet-4-5",
  "reviewer_model": "moonshotai/kimi-k2",
  "review_focus": "security",
  "written_output": "...",
  "review_output": "...",
  "verdict": "REQUEST CHANGES"
}
```

### `POST /review/batch`

Accepts a list of prompts. Runs all in parallel via `asyncio.gather`. Returns a list of review
responses (or `{"error": "..."}` per failed item). Use for bulk review jobs.

---

## Customization Guide

**Swap models anytime** — pass different model slugs per-request. Any OpenRouter model works.
Common alternatives:
- Writer: `openai/gpt-4o`, `google/gemini-2.0-flash`
- Reviewer: `mistralai/mistral-large`, `deepseek/deepseek-r1`

**Add a new review focus:**
```python
REVIEW_PROMPTS["accessibility"] = (
    "You are an accessibility reviewer. Check for: missing ARIA labels, "
    "keyboard navigation gaps, color contrast issues, and screen reader incompatibility."
)
```

**Hook into BrainVault** — the test script saves results as JSON. Route those files to
`~/BrainVault/00-Inbox/` using the HulkInbox watcher for automatic intake.

---

## Troubleshooting

| Symptom | Likely Cause | Fix |
|---|---|---|
| `OPENROUTER_API_KEY not set` | Env var missing on Hulk | Add to `~/.zshrc` or LaunchAgent plist |
| `502` from OpenRouter | Model slug wrong or quota hit | Check slug at openrouter.ai/models |
| Long-running loops | Both models taking time | Normal — `/review` can take 30-90s, use `timeout=120` |
| Verdict is `None` | Reviewer didn't use the exact phrase | Check review_output — verdict extraction is keyword-based |
| Dashboard CORS error | Hulk CORS not configured | Add `fastapi.middleware.cors.CORSMiddleware` to `main.py` |

For CORS, add to `main.py`:
```python
from fastapi.middleware.cors import CORSMiddleware
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])
```

---

## Reference Files

- `references/implementation.md` — Full source code for all three deliverables
- `references/openrouter-models.md` — Recommended model pairings and cost estimates

Read `references/implementation.md` when regenerating files or when the user asks for the source.
Read `references/openrouter-models.md` when the user wants to swap models or asks about cost.
