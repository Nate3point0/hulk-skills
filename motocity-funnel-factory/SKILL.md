---
name: motocity-funnel-factory
description: >
  Complete funnel-ecosystem generator for Ceepeezee (and client builds): produces a
  linktree-style hub page, matching opt-in pages, matching thank-you pages, and
  brand-styled lead magnet PDFs — all as single-file HTML ready to paste into
  Systeme.io Raw HTML blocks, from one shared skeleton with per-funnel accent colors.
  Activate whenever the user says "build my funnel pages", "funnel factory", "new
  funnel page", "add a funnel", "rebrand my pages", "make the thank-you page",
  "turn this lead magnet into a PDF", "client funnel build", "ecosystem build",
  "regenerate my pages", or wants any set of landing/opt-in/thank-you pages that
  must look like one brand. Also fire when a new offer needs to be added to the
  MotoCity hub, or when a client build should reuse this system with new brand
  tokens. First proven run: MotoCity 17-page + 8-PDF ecosystem, July 2026.
version: "1.2"
author: Ceepeezee / City Funk Entertainment
---

# MotoCity Funnel Factory

One skeleton, many funnels. This skill regenerates an entire hybrid Systeme.io
ecosystem — hub + opt-ins + thank-yous + branded PDFs — from copy and color tokens.

## The System

```
brand tokens + page copy ──► scripts/gen_pages.py     ──► N opt-in pages (HTML)
                        ──► scripts/gen_thankyou.py  ──► N thank-you pages (HTML)
markdown lead magnets   ──► scripts/gen_pdfs.py      ──► branded PDFs
hub template            ──► references/hub-page-template.html
```

All HTML output obeys Systeme.io sandbox rules (non-negotiable):
single file, no localStorage/cookies, no iframes, no external images or
stylesheets (no Google Fonts links — system font stack), zero outer padding on
the outermost wrapper, mobile-first at 375px, 44px+ touch targets.

## Workflow

### 1. Gather inputs (ask once)
- Funnel list: name, URL slug, accent color (or auto-assign distinct accents)
- Copy per funnel: headline, subhead, bullets, offer, CTA, FAQ (optional)
- Brand tokens: read references/MOTOCITY-BRAND-STYLE-GUIDE.md for MotoCity;
  for clients, collect: primary/accent hex, dark bg hex, logo wordmark text
- Links: booking calendar, affiliate links (MUST get disclosure), socials, email

### 2. Generate opt-in pages
Edit the PAGES dict in scripts/gen_pages.py (copy + colors per funnel), run it.
Every page ships with: sticky offer bar, kicker, gradient headline, hero card,
bullets/steps/pricing/FAQ components, a dashed "YOUR SYSTEME.IO FORM HERE" slot
(native form element goes there — NEVER rebuild capture in HTML), unified footer
(wordmark, socials, email, legal links, FTC disclosure on affiliate pages).

### 3. Generate thank-you pages
Edit the TY dict in scripts/gen_thankyou.py. Each thank-you page needs a
"money move": order bump, affiliate CTA, booking calendar, or cross-sell to a
sibling funnel. Include the native download-button slot for the lead magnet.

### 4. Generate lead magnet PDFs
scripts/gen_pdfs.py converts markdown guides to brand PDFs (black #0A0A0A pages,
gold #C5A05A heads, silver body, covers, page numbers, footers). It auto-inserts
the FTC disclosure before any "Built with Systeme.io"/affiliate section.
Base-14 fonts only — the sanitizer maps emoji/arrows to latin-1-safe glyphs.

### 5. Hub page
references/hub-page-template.html is the accordion hub. When adding a funnel,
add a door/sub-door with: title, subtitle, one-line description, freebie label
that EXACTLY names the real lead magnet, pill (LIVE/New/Enter/Soon), and accent
glow class. Keep one group open by default. Affiliate CTA keeps its disclosure.

### 6. Verify (every build, before delivery)
- grep outputs for localStorage, iframe, `<img ` (must be zero)
- headline doesn't clip at 375px (letter-spacing needs matching text-indent)
- all UPDATE-ME markers surfaced to the user as a punch list
- deliver with the human-touch checklist (see references/MOTOCITY-LAUNCH-CHECKLIST.md)

## Hybrid split (never violate)
Native Systeme.io: forms, file hosting/download buttons, email automations,
tags, order bumps, checkout. Custom HTML: layout, styling, CTAs that link out.

## Step 7 — Hybrid block split (THE deployment format)
Full-page HTML is for previewing only. For deployment, run
scripts/gen_hybrid.py — it splits every page at its interaction point into
block-A-top.html + block-B-bottom.html (pages with no form stay single-block)
and writes ASSEMBLY-GUIDE.md with per-page hex values.

Assembly recipe (see references/HYBRID-ASSEMBLY-GUIDE.md for the full table):
1. One Section per page; Section background color = page BG hex (this makes
   transparent HTML blocks + native elements read as one seamless page).
2. Raw HTML = Block A (ends with the form headline), padding 0/0/0/0.
3. Native elements between blocks: opt-ins get Input fields (First name,
   Email) + Button (action: Submit form → auto-advances to funnel step 2);
   thank-yous get Button (action: Download file, PDF attached).
   Button style: accent-light bg, #0C0C0C bold text, radius 12, full width.
4. Raw HTML = Block B (starts with the trust line + rest + footer).
5. Funnel = Step 1 opt-in → Step 2 thank-you; automation on step 1: tag
   [funnel]-lead + welcome email with backup PDF link.
6. Raw HTML never renders in editor Preview — verify on the live URL, mobile.

## Client packaging
This is a sellable service: "Complete Funnel Ecosystem Build". Swap brand
tokens, drop in client copy, rerun all three scripts — hours, not weeks.
The MotoCity live hub is the demo.
