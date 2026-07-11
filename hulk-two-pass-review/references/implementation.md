# Implementation Reference

Full source for the three deliverables. Generate these exactly when the user asks to deploy or regenerate.

---

## File 1: `hulk_two_pass_review.py`

```python
"""
hulk_two_pass_review.py
=======================
Drop this into your existing Hulk FastAPI proxy (main.py or proxy.py).
Adds a /review endpoint that:
  1. Sends the prompt to Claude (via OpenRouter) — the WRITER
  2. Sends Claude's output to Kimi K2 — the REVIEWER
  3. Returns both responses in one payload

Mounting (add to main.py):
  from hulk_two_pass_review import router as review_router
  app.include_router(review_router)
"""

import os
import httpx
import asyncio
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional

router = APIRouter()

OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")
OPENROUTER_BASE = "https://openrouter.ai/api/v1/chat/completions"

DEFAULT_WRITER = "anthropic/claude-sonnet-4-5"
DEFAULT_REVIEWER = "moonshotai/kimi-k2"

REVIEW_PROMPTS = {
    "security": (
        "You are an adversarial security reviewer. Analyze the code below for: "
        "auth flaws, injection vulnerabilities, data exposure, race conditions, "
        "and insecure defaults. Be direct. Flag every issue, even minor ones. "
        "Format: CRITICAL / HIGH / MEDIUM / LOW severity buckets."
    ),
    "logic": (
        "You are a logic and correctness reviewer. Check for: off-by-one errors, "
        "edge cases not handled, incorrect assumptions, broken control flow, "
        "and algorithmic bugs. Show the failing input for each issue you find."
    ),
    "performance": (
        "You are a performance reviewer. Identify: N+1 queries, unnecessary loops, "
        "memory leaks, blocking I/O in async contexts, and missed caching opportunities. "
        "Estimate impact (latency / memory) for each issue."
    ),
    "general": (
        "You are an independent code reviewer from a different company than the author. "
        "You have no attachment to this code. Review for: correctness, maintainability, "
        "edge cases, error handling, and anything that would fail in production. "
        "Be honest. Grade it: APPROVE / APPROVE WITH NOTES / REQUEST CHANGES."
    ),
}


class ReviewRequest(BaseModel):
    prompt: str
    write_model: Optional[str] = DEFAULT_WRITER
    review_model: Optional[str] = DEFAULT_REVIEWER
    review_focus: Optional[str] = "general"
    system_prompt: Optional[str] = None


class ReviewResponse(BaseModel):
    writer_model: str
    reviewer_model: str
    review_focus: str
    written_output: str
    review_output: str
    verdict: Optional[str] = None


async def call_openrouter(model: str, messages: list, system: Optional[str] = None) -> str:
    if not OPENROUTER_API_KEY:
        raise HTTPException(status_code=500, detail="OPENROUTER_API_KEY not set on Hulk")

    payload = {"model": model, "messages": messages}
    if system:
        payload["messages"] = [{"role": "system", "content": system}] + messages

    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "Content-Type": "application/json",
        "HTTP-Referer": "http://100.106.11.18:4000",
        "X-Title": "Hulk Two-Pass Review",
    }

    async with httpx.AsyncClient(timeout=120.0) as client:
        resp = await client.post(OPENROUTER_BASE, json=payload, headers=headers)
        resp.raise_for_status()
        data = resp.json()

    try:
        return data["choices"][0]["message"]["content"]
    except (KeyError, IndexError):
        raise HTTPException(status_code=502, detail=f"Unexpected OpenRouter response: {data}")


def extract_verdict(review_text: str) -> Optional[str]:
    text_upper = review_text.upper()
    if "REQUEST CHANGES" in text_upper:
        return "REQUEST CHANGES"
    elif "APPROVE WITH NOTES" in text_upper:
        return "APPROVE WITH NOTES"
    elif "APPROVE" in text_upper:
        return "APPROVE"
    return None


@router.post("/review", response_model=ReviewResponse)
async def two_pass_review(req: ReviewRequest):
    focus = req.review_focus if req.review_focus in REVIEW_PROMPTS else "general"
    review_system = REVIEW_PROMPTS[focus]

    written_output = await call_openrouter(
        model=req.write_model,
        messages=[{"role": "user", "content": req.prompt}],
        system=req.system_prompt,
    )

    reviewer_content = (
        f"## Original Request\n{req.prompt}\n\n"
        f"## Code / Output to Review\n{written_output}"
    )
    review_output = await call_openrouter(
        model=req.review_model,
        messages=[{"role": "user", "content": reviewer_content}],
        system=review_system,
    )

    return ReviewResponse(
        writer_model=req.write_model,
        reviewer_model=req.review_model,
        review_focus=focus,
        written_output=written_output,
        review_output=review_output,
        verdict=extract_verdict(review_output),
    )


@router.post("/review/batch")
async def batch_review(prompts: list[str], review_focus: str = "general"):
    tasks = [two_pass_review(ReviewRequest(prompt=p, review_focus=review_focus)) for p in prompts]
    results = await asyncio.gather(*tasks, return_exceptions=True)
    return [r if not isinstance(r, Exception) else {"error": str(r)} for r in results]
```

---

## File 2: `test_review.py`

```python
#!/usr/bin/env python3
"""
test_review.py — Quick verification for Hulk's /review endpoint.

Usage:
  python3 test_review.py
  python3 test_review.py --focus security
  python3 test_review.py --url http://localhost:4000
"""

import argparse
import json
import httpx

HULK_URL = "http://100.106.11.18:4000"

TEST_PROMPT = """
Write a Python function that:
1. Accepts a user ID and fetches their profile from a SQLite database
2. Returns a dict with name, email, and last_login
3. Handles the case where the user doesn't exist
4. Includes basic error handling
"""

def run_review(base_url: str, focus: str):
    url = f"{base_url}/review"
    payload = {"prompt": TEST_PROMPT, "review_focus": focus}

    print(f"\n🔵 Sending to {url}")
    print(f"📋 Review focus: {focus}\n{'─' * 60}")

    with httpx.Client(timeout=120.0) as client:
        resp = client.post(url, json=payload)
        resp.raise_for_status()
        data = resp.json()

    print(f"✍️  WRITER: {data['writer_model']}")
    print(f"🔍 REVIEWER: {data['reviewer_model']}")
    print(f"🏷️  VERDICT: {data.get('verdict', 'N/A')}")
    print(f"\n{'═' * 60}\nWRITTEN OUTPUT:\n{'═' * 60}")
    print(data["written_output"])
    print(f"\n{'═' * 60}\nREVIEW OUTPUT:\n{'═' * 60}")
    print(data["review_output"])

    out_file = f"review_result_{focus}.json"
    with open(out_file, "w") as f:
        json.dump(data, f, indent=2)
    print(f"\n💾 Saved to {out_file}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--focus", default="general",
                        choices=["security", "logic", "performance", "general"])
    parser.add_argument("--url", default=HULK_URL)
    args = parser.parse_args()
    run_review(args.url, args.focus)
```

---

## File 3: `HulkReviewDashboard.jsx`

```jsx
import { useState } from "react";

const HULK_URL = "http://100.106.11.18:4000";

const FOCUS_OPTIONS = [
  { value: "general", label: "General", icon: "⚖️", color: "#64748b" },
  { value: "security", label: "Security", icon: "🔐", color: "#ef4444" },
  { value: "logic", label: "Logic", icon: "🧠", color: "#8b5cf6" },
  { value: "performance", label: "Performance", icon: "⚡", color: "#f59e0b" },
];

const VERDICT_STYLES = {
  "APPROVE": { bg: "#052e16", border: "#16a34a", text: "#4ade80", label: "✅ APPROVED" },
  "APPROVE WITH NOTES": { bg: "#1c1917", border: "#d97706", text: "#fbbf24", label: "⚠️ APPROVED WITH NOTES" },
  "REQUEST CHANGES": { bg: "#1c0a0a", border: "#dc2626", text: "#f87171", label: "🔴 CHANGES REQUESTED" },
};

function CodeBlock({ content, label, model, color }) {
  const [copied, setCopied] = useState(false);
  const copy = () => { navigator.clipboard.writeText(content); setCopied(true); setTimeout(() => setCopied(false), 1500); };

  return (
    <div style={{ background: "#0a0a0f", border: `1px solid ${color}33`, borderRadius: "8px", overflow: "hidden", display: "flex", flexDirection: "column", flex: 1, minHeight: 0 }}>
      <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center", padding: "10px 14px", background: `${color}18`, borderBottom: `1px solid ${color}33` }}>
        <div>
          <span style={{ color, fontFamily: "monospace", fontSize: "11px", fontWeight: 700, letterSpacing: "0.08em" }}>{label}</span>
          <span style={{ color: "#475569", fontSize: "10px", marginLeft: "10px", fontFamily: "monospace" }}>{model}</span>
        </div>
        <button onClick={copy} style={{ background: "transparent", border: `1px solid ${color}44`, color: copied ? "#4ade80" : color, padding: "3px 10px", borderRadius: "4px", cursor: "pointer", fontSize: "10px", fontFamily: "monospace" }}>
          {copied ? "COPIED" : "COPY"}
        </button>
      </div>
      <div style={{ padding: "14px", overflowY: "auto", flex: 1, fontFamily: "'JetBrains Mono', monospace", fontSize: "12px", lineHeight: "1.7", color: "#94a3b8", whiteSpace: "pre-wrap", wordBreak: "break-word" }}>
        {content || <span style={{ color: "#334155", fontStyle: "italic" }}>Waiting...</span>}
      </div>
    </div>
  );
}

export default function HulkReviewDashboard() {
  const [prompt, setPrompt] = useState("");
  const [focus, setFocus] = useState("general");
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState(null);
  const [error, setError] = useState(null);
  const [phase, setPhase] = useState(null);
  const selectedFocus = FOCUS_OPTIONS.find(f => f.value === focus);

  const runReview = async () => {
    if (!prompt.trim()) return;
    setLoading(true); setError(null); setResult(null); setPhase("writing");
    try {
      const writeTimer = setTimeout(() => setPhase("reviewing"), 4000);
      const resp = await fetch(`${HULK_URL}/review`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ prompt, review_focus: focus }),
      });
      clearTimeout(writeTimer);
      if (!resp.ok) throw new Error(`Hulk returned ${resp.status}: ${await resp.text()}`);
      setResult(await resp.json());
      setPhase(null);
    } catch (e) { setError(e.message); setPhase(null); }
    finally { setLoading(false); }
  };

  const verdict = result?.verdict ? VERDICT_STYLES[result.verdict] : null;

  return (
    <div style={{ minHeight: "100vh", background: "#050508", color: "#e2e8f0", fontFamily: "'JetBrains Mono', monospace", display: "flex", flexDirection: "column", padding: "20px", gap: "16px", boxSizing: "border-box" }}>
      <div style={{ display: "flex", alignItems: "center", gap: "12px" }}>
        <div style={{ width: "36px", height: "36px", background: "linear-gradient(135deg, #22c55e, #16a34a)", borderRadius: "8px", display: "flex", alignItems: "center", justifyContent: "center", fontSize: "18px", boxShadow: "0 0 20px #22c55e44" }}>⚙</div>
        <div>
          <div style={{ fontSize: "14px", fontWeight: 700, color: "#f8fafc", letterSpacing: "0.05em" }}>HULK TWO-PASS REVIEW</div>
          <div style={{ fontSize: "10px", color: "#475569" }}>Claude writes · Kimi K2 reviews · You decide</div>
        </div>
        <div style={{ marginLeft: "auto", display: "flex", alignItems: "center", gap: "6px" }}>
          <div style={{ width: "7px", height: "7px", borderRadius: "50%", background: "#22c55e", boxShadow: "0 0 6px #22c55e" }} />
          <span style={{ fontSize: "10px", color: "#22c55e" }}>HULK LIVE</span>
        </div>
      </div>

      <div style={{ background: "#0d0d14", border: "1px solid #1e293b", borderRadius: "8px", overflow: "hidden" }}>
        <div style={{ padding: "8px 14px", borderBottom: "1px solid #1e293b", fontSize: "10px", color: "#475569", letterSpacing: "0.08em" }}>PROMPT</div>
        <textarea value={prompt} onChange={e => setPrompt(e.target.value)} placeholder="Describe what you want written — code, function, module, API route, script..." style={{ width: "100%", minHeight: "100px", background: "transparent", border: "none", outline: "none", color: "#cbd5e1", fontFamily: "'JetBrains Mono', monospace", fontSize: "12px", lineHeight: "1.7", padding: "12px 14px", resize: "vertical", boxSizing: "border-box" }} />
      </div>

      <div style={{ display: "flex", gap: "10px", alignItems: "center", flexWrap: "wrap" }}>
        <span style={{ fontSize: "10px", color: "#475569", letterSpacing: "0.08em" }}>REVIEW FOCUS:</span>
        <div style={{ display: "flex", gap: "6px" }}>
          {FOCUS_OPTIONS.map(opt => (
            <button key={opt.value} onClick={() => setFocus(opt.value)} style={{ background: focus === opt.value ? `${opt.color}22` : "transparent", border: `1px solid ${focus === opt.value ? opt.color : "#1e293b"}`, color: focus === opt.value ? opt.color : "#475569", padding: "5px 12px", borderRadius: "4px", cursor: "pointer", fontSize: "11px", fontFamily: "monospace" }}>
              {opt.icon} {opt.label}
            </button>
          ))}
        </div>
        <button onClick={runReview} disabled={loading || !prompt.trim()} style={{ marginLeft: "auto", background: loading ? "#0f2010" : "linear-gradient(135deg, #16a34a, #15803d)", border: "none", color: loading ? "#4ade80" : "#fff", padding: "8px 24px", borderRadius: "6px", cursor: loading ? "not-allowed" : "pointer", fontSize: "12px", fontWeight: 700, letterSpacing: "0.05em" }}>
          {loading ? (phase === "writing" ? "✍️ Writing..." : "🔍 Reviewing...") : "▶ RUN REVIEW"}
        </button>
      </div>

      {loading && (
        <div style={{ display: "flex", gap: "20px", padding: "10px 14px", background: "#0d0d14", borderRadius: "6px", border: "1px solid #1e293b" }}>
          {["writing", "reviewing"].map((p, i) => (
            <div key={p} style={{ display: "flex", alignItems: "center", gap: "8px" }}>
              <div style={{ width: "8px", height: "8px", borderRadius: "50%", background: phase === p ? "#22c55e" : "#1e293b", boxShadow: phase === p ? "0 0 8px #22c55e" : "none" }} />
              <span style={{ fontSize: "11px", color: phase === p ? "#22c55e" : "#334155" }}>{i === 0 ? "Claude writing" : "Kimi K2 reviewing"}</span>
            </div>
          ))}
        </div>
      )}

      {error && <div style={{ padding: "12px 14px", background: "#1c0a0a", border: "1px solid #dc262644", borderRadius: "6px", color: "#f87171", fontSize: "12px" }}>⚠️ {error}</div>}

      {verdict && <div style={{ padding: "10px 16px", background: verdict.bg, border: `1px solid ${verdict.border}`, borderRadius: "6px", color: verdict.text, fontSize: "12px", fontWeight: 700, letterSpacing: "0.08em", textAlign: "center" }}>{verdict.label}</div>}

      {result && (
        <div style={{ display: "flex", gap: "14px", flex: 1, minHeight: "400px" }}>
          <CodeBlock content={result.written_output} label="WRITTEN OUTPUT" model={result.writer_model} color="#3b82f6" />
          <CodeBlock content={result.review_output} label={`REVIEW · ${result.review_focus.toUpperCase()}`} model={result.reviewer_model} color={selectedFocus.color} />
        </div>
      )}

      <div style={{ display: "flex", justifyContent: "space-between", fontSize: "9px", color: "#1e293b", paddingTop: "4px" }}>
        <span>HULK · 100.106.11.18:4000</span>
        <span>WRITER: {result?.writer_model || "anthropic/claude-sonnet-4-5"} · REVIEWER: {result?.reviewer_model || "moonshotai/kimi-k2"}</span>
      </div>
    </div>
  );
}
```
