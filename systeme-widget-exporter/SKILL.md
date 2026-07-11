---
name: systeme-widget-exporter
description: >
  Builds and exports any interactive widget, calculator, quiz, landing page
  section, or tool as a single self-contained HTML file ready to paste into
  a Systeme.io Raw HTML block. Enforces Systeme.io sandbox constraints
  (no localStorage, no cross-origin fetch, no iframes, zero outer padding)
  and outputs a verified copy-paste code block on every build.
triggers:
  - systeme
  - systeme.io
  - raw html block
  - paste into systeme
  - export for systeme
  - html widget
  - embed widget
  - funnel widget
  - lead magnet widget
  - calculator widget
  - quiz widget
version: "1.0"
author: Ceepeezee
---

# systeme-widget-exporter

Builds single-file HTML widgets that drop straight into Systeme.io Raw HTML
blocks with no friction. Every output is verified against Systeme.io's sandbox
rules before delivery.

---

## Systeme.io Sandbox Rules (non-negotiable)

These apply to every build. Do not deviate:

| Rule | Detail |
|------|--------|
| Single file | All CSS and JS inside one HTML file — no external stylesheets, no external scripts except whitelisted CDNs |
| No localStorage | Systeme.io sandboxes storage — use JS variables only |
| No cross-origin fetch | No calls to external APIs unless user explicitly provides a CORS-enabled endpoint |
| No iframes | Systeme.io strips nested iframes |
| No cookies | Session storage only — variables in memory |
| Zero outer padding | Systeme.io adds its own padding; the widget's outermost wrapper must have `margin:0; padding:0` |
| Mobile-first | All widgets must be fully responsive; test at 375px width |
| CDN whitelist | Allowed: cdnjs.cloudflare.com, cdn.jsdelivr.net, unpkg.com |
| No external images | Use CSS gradients, SVG, or emoji — no `<img src="http...">` |

---

## Step 1 — Widget Brief

Ask (once, all together) if not already provided:

```
To build your Systeme.io widget I need:
1. Widget type — calculator · quiz · lead capture · pricing table · countdown · testimonial slider · FAQ accordion · other
2. What it does — one sentence describing the user action and output
3. Inputs — what does the user enter or select?
4. Output / result — what does it show after interaction?
5. Brand — paste your DESIGN.md tokens, or give me: primary color, background color, font style
6. CTA — what happens after the result? (email opt-in · redirect to offer · show next step)
```

---

## Step 2 — Build Prompt (internal)

```
Build a self-contained HTML widget for [widget type].

FUNCTION: [what it does]
INPUTS: [list with types and valid ranges]
OUTPUT: [result display and format]
CTA: [post-result action]

SYSTEME.IO CONSTRAINTS (mandatory):
- Single HTML file: all CSS in <style>, all JS in <script>
- No localStorage, no sessionStorage, no cookies
- No cross-origin fetch (no external API calls)
- No iframes
- Outermost div: margin:0; padding:0; width:100%
- Mobile-first responsive (test at 375px)
- No external image URLs — use CSS, SVG, or emoji only
- Allowed CDNs only: cdnjs.cloudflare.com, cdn.jsdelivr.net, unpkg.com

DESIGN:
- Primary color: [HEX]
- Background: [HEX]
- Font: [system-ui / or specify]
- Button radius: [px]
- All interactive elements: 44px minimum touch target
- WCAG AA contrast on all text

BEHAVIOR:
- Real-time results (no submit button unless required by logic)
- Reset button included
- Inline error messages (never alert() or confirm())
- Empty state handled gracefully
- Long text overflow handled (text-overflow: ellipsis or wrap)
- Zero input / negative input / max cap edge cases handled

OUTPUT REQUIREMENTS:
- Deliver complete HTML in a single fenced code block
- Include a <!-- SYSTEME.IO PASTE INSTRUCTIONS --> comment at the top of the file
- Include <!-- END WIDGET --> at the bottom
```

---

## Step 3 — Paste Instructions (auto-generated with every widget)

Append this block after every completed widget:

```
<!-- =====================================================
     SYSTEME.IO PASTE INSTRUCTIONS
     =====================================================
     1. In Systeme.io editor: Add Element → Raw HTML
     2. Paste this entire file contents into the HTML box
     3. Set element padding: Desktop → 0 / 0 / 0 / 0
                             Mobile  → 0 / 0 / 0 / 0
     4. Preview on mobile before publishing
     5. If using a CTA redirect: update the href on line [X]
     ===================================================== -->
```

---

## Widget Templates

### Calculator / Estimator
```
Build a Systeme.io-ready HTML calculator for [X].
USER: [who uses it · why]
INPUTS: [label · type · range for each]
FORMULA: [describe calculation logic]
OUTPUT: shows [result] broken down as [format]
EDGE CASES: zero · negative · empty · max cap
DESIGN: [primary HEX] accent · [bg HEX] background · system-ui font
Real-time results. Reset button. Inline errors. Single HTML file.
Systeme.io constraints: no localStorage, no external fetch, zero outer padding.
Deliver as a complete HTML code block with paste instructions comment.
```

### Quiz / Score Funnel
```
Build a Systeme.io-ready HTML quiz for [topic].
QUESTIONS: [number] questions · [multiple choice / slider / yes-no]
SCORING: [describe scoring logic and result segments]
RESULT SEGMENTS: [segment name · score range · message · CTA for each]
CTA: [redirect to URL / show opt-in form / display offer]
DESIGN: [primary HEX] · [bg HEX] · clean, minimal
Single HTML file. No localStorage. Progress bar included. Mobile-first.
Deliver as complete HTML code block with paste instructions comment.
```

### Lead Capture Widget
```
Build a Systeme.io-ready HTML lead capture widget.
OFFER: [what the user gets]
FIELDS: [name (optional) · email (required) · other]
SUBMIT ACTION: [POST to Systeme.io form URL: INSERT_FORM_ACTION_URL]
SUCCESS STATE: [message or redirect URL]
DESIGN: [primary HEX] · [bg HEX] · [tone: minimal/bold]
Single HTML file. Native form POST. No JS fetch. Mobile-first.
Deliver as complete HTML code block with paste instructions comment.
```

### Countdown Timer
```
Build a Systeme.io-ready HTML countdown timer.
TARGET DATE: [ISO date string or "X days from page load"]
DISPLAY: days · hours · minutes · seconds
EXPIRED STATE: [message or hide timer]
DESIGN: [primary HEX] · large digits · [bg HEX]
Single HTML file. No localStorage (recalculate on each load). Mobile-first.
Deliver as complete HTML code block with paste instructions comment.
```

### Pricing Table
```
Build a Systeme.io-ready HTML pricing table.
TIERS: [name · price · billing · features list · CTA label · CTA URL for each]
HIGHLIGHT: [which tier is "most popular"]
TOGGLE: [monthly/annual toggle if needed]
DESIGN: [primary HEX] · [bg HEX] · [card style from DESIGN.md]
Single HTML file. No external dependencies. Mobile: stack vertically.
Deliver as complete HTML code block with paste instructions comment.
```

### FAQ Accordion
```
Build a Systeme.io-ready HTML FAQ accordion.
QUESTIONS: [paste Q&A pairs]
BEHAVIOR: one open at a time · smooth animation · first item open by default
DESIGN: [primary HEX] · [bg HEX] · [border/divider style]
Single HTML file. Pure CSS/JS. Mobile-first.
Deliver as complete HTML code block with paste instructions comment.
```

---

## Step 4 — Post-Build Checklist

Run silently and fix before delivering:

```
[ ] Outermost wrapper: margin:0; padding:0; width:100%
[ ] No localStorage / sessionStorage references
[ ] No cross-origin fetch / XHR calls
[ ] No iframes
[ ] No external image src URLs
[ ] CDNs used (if any) are on whitelist
[ ] Mobile tested at 375px (no horizontal scroll, no overflow)
[ ] All touch targets ≥ 44px
[ ] Error states handled inline (no alert())
[ ] Empty/zero input handled
[ ] Reset button present (if form/calculator)
[ ] Paste instructions comment block at top of output
```

---

## Step 5 — Revenue Packaging (optional, offer after delivery)

> "Want me to package this widget as a sellable digital asset?
> I can add: a product description, a prompt card (so buyers can customize it),
> and a Systeme.io store listing template — ready to upload and sell."
