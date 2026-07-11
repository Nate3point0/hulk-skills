---
name: design-master
description: >
  Master skill for consistent, system-first design in Claude Artifacts.
  Enforces DESIGN.md design tokens, brainstorm-before-build workflow,
  three-surface iteration (Tweaks → Comments → Chat), and stack-specific
  export for Systeme.io, HULK, and BrainVault. Activates on any build,
  design, prototype, calculator, dashboard, or widget request.
triggers:
  - build
  - design
  - create
  - prototype
  - landing page
  - calculator
  - dashboard
  - widget
  - artifact
  - DESIGN.md
  - skillify
  - export to Systeme.io
version: "1.0"
author: Ceepeezee
---

# Claude Design Master Skill

## Trigger Conditions

Activate this skill whenever the user:
- Says "build", "design", "create", "make", "prototype", or "generate" any visual output (landing page, calculator, dashboard, funnel, widget, tool, quiz, app, chart, component)
- Mentions "artifact", "HTML artifact", "React artifact", "live preview"
- Asks to "extract a DESIGN.md", "set up design system", "make it consistent"
- Wants to export something to Systeme.io, Vercel, or any hosting
- Says "skillify", "save as skill", "reuse this design"
- Mentions "DESIGN.md", "design tokens", "brand system"
- Wants to iterate on an existing artifact

---

## Phase 0: Pre-Flight Checklist

Before writing a single line of output, run this checklist silently and surface any gaps as a single compact question block (never one question at a time):

```
DESIGN.md status:     [ ] Ready / [ ] Need to create / [ ] Will extract from reference
Audience:             [ ] Defined / [ ] Missing
Goal / CTA:           [ ] Defined / [ ] Missing  
Output format:        [ ] HTML Artifact / [ ] React Artifact / [ ] SVG / [ ] Markdown
Mobile-first:         [ ] Confirmed / [ ] Will add by default
Accessibility:        [ ] WCAG AA baseline / [ ] Needs audit
Icon library:         [ ] Lucide only (default) / [ ] Other
Edge cases:           [ ] Empty inputs / negatives / long text covered
Iteration surface:    [ ] Tweaks → Comments → Chat sequence planned
Export path:          [ ] Systeme.io raw HTML / [ ] Vercel / [ ] HULK / [ ] Standalone
```

If DESIGN.md is not ready → jump to **Phase 1** first.  
If DESIGN.md exists → skip to **Phase 2**.

---

## Phase 1: Build or Extract DESIGN.md

### Option A — Extract from reference (screenshot, URL, or existing brand)

Prompt Claude uses internally:
```
Analyze this [screenshot / URL / description] and extract a complete DESIGN.md.
Include:
1. Color palette with HEX codes (primary, secondary, accent, background, text, muted)
2. Typography scale (font families, sizes H1–H4, body, caption; weights; line heights)
3. Spacing scale (base unit and multipliers — prefer 4px base)
4. Component inventory (buttons, cards, inputs, nav — with variants and states)
5. Layout rules (grid system, max-width, responsive breakpoints)
6. Icon style (Lucide icons default; filled vs outline; no external image dependencies)
7. Accessibility baseline (WCAG AA contrast ratios; keyboard nav; aria-label rules)
8. Density modes (compact / comfortable / spacious definitions)
Output as clean markdown. Label it DESIGN.md.
```

### Option B — Build fresh from brief

Ask the user (single question block):
```
To create your DESIGN.md I need 3 things:
1. Brand colors (even rough: "dark navy, gold accent, white bg" works)
2. Vibe/tone (minimal, bold, playful, corporate, techy, warm)  
3. One reference (a site you like, a screenshot, or "derive from [niche]")
```

Then generate the DESIGN.md using this template:

```markdown
# DESIGN.md — [Project Name]

## Color Tokens
| Token | HEX | Usage |
|-------|-----|-------|
| --color-primary | #XXXXXX | CTAs, headings, links |
| --color-secondary | #XXXXXX | Secondary buttons, accents |
| --color-accent | #XXXXXX | Highlights, badges |
| --color-bg | #XXXXXX | Page background |
| --color-surface | #XXXXXX | Card / panel backgrounds |
| --color-text | #XXXXXX | Body copy |
| --color-muted | #XXXXXX | Captions, placeholders |
| --color-error | #XXXXXX | Error states |
| --color-success | #XXXXXX | Success states |

## Typography Scale
| Role | Family | Size | Weight | Line Height |
|------|--------|------|--------|-------------|
| H1 | [Family] | 48px / 3rem | 700 | 1.1 |
| H2 | [Family] | 36px / 2.25rem | 600 | 1.2 |
| H3 | [Family] | 24px / 1.5rem | 600 | 1.3 |
| H4 | [Family] | 20px / 1.25rem | 500 | 1.4 |
| Body | [Family] | 16px / 1rem | 400 | 1.6 |
| Small | [Family] | 14px / 0.875rem | 400 | 1.5 |
| Caption | [Family] | 12px / 0.75rem | 400 | 1.4 |

## Spacing Scale (4px base)
4 · 8 · 12 · 16 · 24 · 32 · 48 · 64 · 96 · 128

## Component Rules
### Buttons
- Primary: --color-primary bg, white text, 8px radius, 16px 32px padding
- Secondary: transparent bg, --color-primary border+text
- Ghost: no border, --color-primary text, hover bg opacity 10%
- Sizes: sm (12px/28px) · md (16px/40px) · lg (18px/52px)

### Cards
- Background: --color-surface
- Border: 1px solid rgba(0,0,0,0.08)
- Border radius: 12px
- Shadow: 0 2px 8px rgba(0,0,0,0.06)
- Padding: 24px (comfortable) / 16px (compact) / 32px (spacious)

### Inputs
- Height: 44px (mobile tap target)
- Border: 1px solid --color-muted
- Focus: 2px solid --color-primary outline
- Error: 1px solid --color-error, inline message below
- Label: above input, --color-text, 14px

### Hero Variants
- type-only: centered text + CTA, no image
- split-image: 50/50 text left, image right
- centered-screenshot: text + product screenshot below
- video-bg: full-bleed video, text overlay

## Density Modes
- compact: spacing × 0.75
- comfortable: spacing × 1.0 (default)
- spacious: spacing × 1.25

## Icon System
- Library: Lucide icons only
- NO external image URLs
- Fallback: emoji if Lucide doesn't have the icon
- Size: 20px inline, 24px standalone, 32px feature icons

## Accessibility Baseline
- Minimum contrast: 4.5:1 text, 3:1 UI elements (WCAG AA)
- All interactive elements: keyboard focusable
- Dynamic content: aria-live regions
- Images: alt text required
- Forms: label + aria-describedby for errors
- Touch targets: minimum 44×44px

## Layout
- Max content width: 1200px
- Grid: 12-column, 24px gutter
- Breakpoints: mobile <768px · tablet 768–1024px · desktop >1024px
- Section padding: 80px top/bottom desktop, 48px mobile
```

After generating, tell the user:
> "DESIGN.md is ready. Reference this at the start of any session: *'Use DESIGN.md for all artifacts — do not deviate from these tokens unless I ask.'* Save it to BrainVault tagged by niche."

---

## Phase 2: Brainstorm-First Workflow

**Never jump straight to code.** Always do a brainstorm pass first.

### Step 1 — Goal framing
Restate what you heard in one sentence:
> "You want a [output type] for [audience] with the goal of [single CTA/outcome]."

### Step 2 — Brainstorm outline (before any code)
Generate a structured outline:
```
SECTIONS / COMPONENTS:
1. [Section name] — [purpose] — [variant from DESIGN.md]
2. ...

KEY INTERACTIONS:
- [Describe any dynamic behavior]

EDGE CASES I'LL HANDLE:
- [Empty states, error states, long text, mobile layout]

CALCULATION LOGIC (if applicable):
- [Describe formula / logic flow]

WHAT I'LL LEAVE OUT (and why):
- [Scope control]
```

Then ask: "Does this look right, or do you want to adjust anything before I build?"

### Step 3 — Build with explicit constraints
After approval, open the build prompt with:
```
Build this as [HTML/React] Artifact.
Reference DESIGN.md for all tokens — do not deviate.
Mobile-first and responsive.
Keyboard navigable, aria-labels on all dynamic content, WCAG AA contrast.
Icons: Lucide only. No external image URLs.
Edge cases: handle empty inputs, long text overflow, error states.
```

---

## Phase 3: Three-Surface Iteration Protocol

After every build, remind the user of the iteration hierarchy:

```
┌─────────────────────────────────────────────────────┐
│           ITERATION SURFACE DECISION TREE           │
├─────────────────┬───────────────────────────────────┤
│ Tweaks Panel    │ Reorder sections, swap variants,  │
│ (0 tokens)      │ density, spacing, accent intensity│
├─────────────────┼───────────────────────────────────┤
│ Inline Comment  │ Padding, single icon, single       │
│ (low tokens)    │ color, text overflow, one element │
├─────────────────┼───────────────────────────────────┤
│ Chat Re-prompt  │ New section, conceptual pivot,    │
│ (high tokens)   │ new page intent, broken logic     │
└─────────────────┴───────────────────────────────────┘
Rule: Exhaust Tweaks → Comments before Chat. 
Every unnecessary chat re-prompt costs 3–5x.
```

---

## Phase 4: Prompt Templates (Copy-Paste Ready)

### Template A — Landing Page
```
Create a landing page artifact for [PRODUCT/NICHE].
AUDIENCE: [target user]
GOAL: [single CTA]
TONE: [professional/playful/aggressive/minimal]
SECTIONS:
1. Hero: [headline + subheadline + CTA + optional social proof count]
2. Problem: 3 pain points with Lucide icons
3. Solution: 3 features with icons and micro-copy
4. Social Proof: testimonial cards or logo bar
5. Pricing: 3-tier table or single CTA
6. FAQ: 5 accordion items
7. Footer: minimal links + CTA repeat
DESIGN SYSTEM: [paste DESIGN.md or say "use DESIGN.md on file"]
Before building, outline your section plan for approval.
```

### Template B — Calculator / Estimator
```
Build an HTML Artifact for a [X] calculator.
USER STORY: [who uses it and why]
INPUTS: [each input: label, type, valid range]
OUTPUTS: [result display, breakdown, comparisons]
EDGE CASES: zero inputs, negative numbers, max caps, empty state
DESIGN: clean, minimal, mobile-first, [primary color] accent
Show results in real-time as user types. No submit button.
Include Reset button. Inline error messages (no alerts).
Before writing code, describe calculation logic and UI flow.
```

### Template C — Data Dashboard
```
I have this data: [paste CSV or describe structure].
Build a React Artifact: [bar/line/pie/scatter] chart.
REQUIREMENTS:
- Labels, legend, tooltips
- [filter/sort/search] if dataset is large
- Color palette: [HEX list or "use DESIGN.md"]
- Stack on mobile, scroll if needed
- Export: "Download as PNG" or "Copy data" button
Confirm data structure and chart type before building.
```

### Template D — DESIGN.md Extraction
```
Analyze this [screenshot / URL / Figma] and extract a DESIGN.md.
Include:
1. Color palette with HEX (primary, secondary, accent, bg, text, muted)
2. Typography scale (families, sizes H1–caption, weights, line heights)
3. Spacing scale (base unit + multipliers)
4. Component inventory (buttons, cards, inputs, nav — variants + states)
5. Layout rules (grid, max-width, breakpoints)
6. Icon style (library if identifiable; filled vs outline)
7. Accessibility notes (contrast ratios where calculable)
Output as clean markdown I can save as DESIGN.md and reuse as SKILL.md.
```

### Template E — AI-Powered Micro-App
```
Build an AI-powered artifact that [core function].
USER FLOW:
1. User [types/uploads/selects]
2. AI [what it does with input]
3. Output shows [result format]
AI RULES:
- Only use artifact content (no general training data)
- When uncertain: [fallback behavior]
- Do not: [prohibited behavior]
DESIGN: clean form or chat UI, loading states, error handling, mobile-first
Lucide icons. No external images.
```

### Template F — Accessibility Color Audit
```
Audit and fix this palette for WCAG AA:
Primary: [HEX] · Secondary: [HEX] · Background: [HEX] · Text: [HEX] · Accent: [HEX]
1. Test every text-on-background combination
2. For each: contrast ratio, WCAG requirement, pass/fail
3. For fails: minimum adjustment to pass while preserving brand feel
4. Output: fixed HEX codes + before/after ratios + safe-combination matrix
```

### Template G — Systeme.io Widget Export
```
Build a self-contained HTML artifact for [widget type].
REQUIREMENTS:
- Single HTML file (no external CSS/JS dependencies except CDN if needed)
- All styles inline or in <style> tag
- Works when pasted into Systeme.io Raw HTML block
- No padding on outer wrapper (Systeme adds its own)
- Mobile-first, responsive
- No iframes, no cookies, no localStorage (Systeme sandbox restrictions)
DESIGN: [paste DESIGN.md tokens or describe brand]
After building, output the final HTML in a code block ready to copy-paste.
```

---

## Phase 5: Stack Integration Rules

### → Systeme.io
- Export as single HTML file
- Paste into Raw HTML element
- Desktop padding: outer 40→0, inner 10→0
- Mobile padding: top 5→0, bottom 5→0
- No localStorage, no cross-origin fetches
- Test on mobile before publishing

### → BrainVault / Obsidian
- Save every DESIGN.md in `/BrainVault/design-systems/[niche]/DESIGN.md`
- Tag: `#design-system #[niche] #[date]`
- Every working DESIGN.md becomes a SKILL.md candidate
- Log: prompt used + output quality score

### → HULK Server (FastAPI proxy)
- Use Claude Design for UI prototype only
- Hand off to HULK for: backend logic, data persistence, API calls
- Workflow: `DESIGN.md → Claude Design prototype → Claude Code → HULK endpoint`
- Pass the artifact HTML as the frontend; HULK serves as the API

### → Revenue (Systeme.io Store)
- Every artifact built = potential sellable template
- Document: the prompt that built it + the DESIGN.md used
- Package: HTML file + DESIGN.md + prompt instructions
- List on Systeme.io store as "done-for-you" template

---

## Phase 6: Failure Mode Prevention

| Failure | Root Cause | Prevention |
|---------|-----------|------------|
| Generic output | No DESIGN.md, vague goal | Always run Phase 0 checklist |
| Burned token budget | Chat-prompting layout tweaks | Show iteration surface tree after every build |
| Broken mobile layout | No responsive instruction | "mobile-first" is hardcoded in every template |
| Text overflow | No edge case instruction | All templates include long-text edge case |
| Broken external images | Referenced external URLs | Lucide-only rule; no external image URLs |
| Accessibility fails | No WCAG instruction | WCAG AA baseline in every build prompt |
| Lost iteration | No version history | Remind: screenshot before major changes |
| AI hallucinating | General training data leak | "Only use artifact content" constraint |

---

## Phase 7: Skillify Output

After any artifact reaches "battle-tested" status:

1. Save the DESIGN.md as `/skills/[niche]-design-system/SKILL.md`
2. Document: what this design system is for, niche, tone, and use cases
3. Reference it in future sessions: "Load [niche] SKILL.md as design system"
4. This makes every successful build a reusable template across projects

---

## Quick Reference Card

```
SESSION START:
  1. DESIGN.md ready? → if no, Phase 1
  2. Brief Claude: "Reference DESIGN.md. Do not deviate."
  3. Brainstorm first. No code until plan approved.

DURING BUILD:
  4. Tweaks panel → inline comment → chat (in that order)
  5. Screenshot before any major pivot

AFTER BUILD:
  6. Export for destination (Systeme / HULK / standalone)
  7. Save prompt + DESIGN.md to BrainVault
  8. If sellable → package and list on Systeme.io store

ALWAYS:
  ✓ Mobile-first    ✓ Lucide icons only    ✓ WCAG AA
  ✓ Edge cases      ✓ Inline errors        ✓ No external images
```
