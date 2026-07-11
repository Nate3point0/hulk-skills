---
name: funnel-auditor
description: >
  On-demand audit skill for Systeme.io funnel pages (or any landing page URL). Covers all four audit pillars: Design/Visual QA, Performance, SEO, and Functionality/UX. Activate this skill whenever Ceepeezee says anything like "audit my funnel", "check the page", "review my site", "QA this landing page", "how does my funnel look", "run the audit", "check my Systeme.io page", or pastes a moto-city.systeme.io URL or any funnel link. Also trigger when Ceepeezee says "run it again" or "check this one too" after a previous audit. This skill should fire anytime a page needs inspection — don't wait for the word "audit" specifically.
---

# Funnel Auditor

You are auditing a Systeme.io funnel page (or any landing page). Your job is to give Ceepeezee a fast, actionable report across four areas: Design, Performance, SEO, and Functionality. The goal is not a comprehensive academic review — it's a punch list of things that are actually broken or noticeably weak, with clear fixes.

## How to run the audit

### Step 1 — Get the URL

If the user didn't provide a URL, ask for it. Reference example: `https://moto-city.systeme.io/sound-arsenal`. The skill works on any funnel page URL.

### Step 2 — Load the page with Claude in Chrome

Use `mcp__Claude_in_Chrome__navigate` to load the URL, then:
- `mcp__Claude_in_Chrome__get_page_text` — full page text for copy/SEO analysis
- `mcp__Claude_in_Chrome__read_page` — DOM structure, elements, links
- `mcp__Claude_in_Chrome__computer` (screenshot) — visual render for design review
- `mcp__Claude_in_Chrome__read_console_messages` — JS errors, warnings
- `mcp__Claude_in_Chrome__read_network_requests` — failed resources, slow loads

Also check mobile: use `mcp__Claude_in_Chrome__resize_window` to set viewport to 390×844 (iPhone 14), screenshot again.

### Step 3 — Run a Lighthouse/performance check (if CLI available)

If the `mcp__workspace__bash` tool is available, run:
```bash
npx lighthouse <URL> --output=json --quiet --chrome-flags="--headless" 2>/dev/null | python3 -c "
import json,sys
d=json.load(sys.stdin)
cats=d.get('categories',{})
for k,v in cats.items():
    print(f'{k}: {round(v[\"score\"]*100)}')
"
```
If Lighthouse isn't available or errors, skip and note it — the Chrome inspection covers most of the same ground.

### Step 4 — Compile the report

Structure it exactly like this:

---

## Funnel Audit — [Page Title or URL]
*Audited: [date]*

### 🎨 Design / Visual QA
Issues found and fixes. Note: layout breaks, alignment problems, font inconsistencies, CTA button visibility, hero image quality, mobile layout problems. If nothing is broken, say so briefly.

### ⚡ Performance
Lighthouse scores if available (Performance, Accessibility, Best Practices, SEO). Otherwise note: load time impression, number of failed network requests, large images, JS errors from console. Flag anything that would noticeably slow the page.

### 🔍 SEO
Check: page title tag (present and descriptive?), meta description (present?), H1 (one, clear, keyword-relevant?), image alt text (missing?), URL slug (clean?). Flag missing or weak items with a one-line fix each.

### ✅ Functionality / UX
Check: all CTAs are clickable and go somewhere, form fields work (if present), no broken images or links, copy is clear and has a hook + benefit + CTA structure, mobile tap targets are adequate. Try clicking the primary CTA if possible.

### 🏆 Priority Fixes
Top 3 things to fix first, ranked by impact. Be specific — "Change H1 from X to Y" beats "improve the headline."

---

## Audit style

- Be direct. If something sucks, say it clearly.
- Skip categories where nothing is wrong — don't pad the report.
- Fixes should be actionable in Systeme.io's page builder (no code required unless unavoidable).
- If the user has the Chrome extension and the CLI available, use both — they give better data than either alone.
- When you find a broken link or failing network request, include the URL so it's easy to track down.
- For Systeme.io pages specifically: note if a section element, button, or form looks like it may not render correctly on mobile due to Systeme.io's builder constraints.
