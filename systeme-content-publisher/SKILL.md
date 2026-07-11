---
name: systeme-content-publisher
description: >
  End-to-end Systeme.io campaign publisher for Ceepeezee: write a blog post + matching
  newsletter, push the newsletter as a REAL draft via the official Systeme.io MCP, and
  physically publish the blog post via Claude in Chrome on the live dashboard. Activate
  whenever the user says "publish a blog and newsletter", "new campaign", "blog + email
  combo", "push this to my blog", "make a newsletter draft", "run the content publisher",
  or wants any written content to actually LAND in Systeme.io instead of staying in chat.
  Includes verified image specs, the affiliate link pattern, TipTap email HTML rules, and
  every Chrome-automation gotcha learned from the first live run (June 2026).
---

# Systeme.io Content Publisher

Publishes a matched blog post + newsletter pair into Ceepeezee's real Systeme.io account.
Proven end-to-end on 2026-06-09 (post live at motocity.autos/blog/, draft #4917339).

## Core rules (non-negotiable)

1. **Drafts only for email.** Create/update newsletters via MCP — NEVER send. Ceepeezee always pulls the trigger.
2. **One CTA per asset** (Marcus Campbell: One Page, One Purpose, One Action).
3. **Affiliate pattern:** any systeme.io URL + `?sa=sa0180716782ce4535d7f0b3ef221c7f646590fe91`. Always add the affiliate disclosure line at the end of monetized posts.
4. **GLF structure:** social hook → blog post (converts via affiliate/lead CTA) → newsletter drives existing list to the post.
5. Newsletter targeting: match interest tags (Interest-AI, Interest-Money, Interest-Detail, Interest-Cars, MotoCity-Hub). Never blast car content to music subscribers or vice versa.

## Step 1 — Write the pair

- Blog post: 500–800 words, commercial-intent keyword in title + slug, ALL-CAPS or h2 section headers, one hyperlinked CTA phrase, disclosure footer.
- Newsletter: short (150–250 words), {first_name} greeting, one CTA link → the blog post URL, P.S. line. Subject = curiosity + specificity.

## Step 2 — Newsletter via official MCP

Tool: `mcp__systeme-io-official__create_newsletter` (or `update_newsletter` with id).

Body shape (nested!):
```json
{"data": {"type": "regular", "content": {"subject": "...", "previewText": "...", "bodyHtml": "<p style=\"margin-top: 0; margin-bottom: 0\">Hey {first_name},</p>..."}}}
```

TipTap bodyHtml rules: only p/h2/h3/h4/ul/ol/figure top-level; every `<p>` needs explicit margin style; blank lines are `<p><br></p>`; links `a[href]` https only; substitutions limited to {email} {first_name} {surname}. No div/table/script.

REST fallback: `python3 ~/hulk/systeme_newsletter.py` — endpoint is `/api/mailing/newsletters` (NOT /api/newsletters). Gated pipeline: `python3 ~/hulk/newsletter_factory.py "<topic>"` → Kimi grade → Telegram approve.

API cannot delete newsletters — dashboard only.

## Step 3 — Blog via Claude in Chrome

Login URL that works: `https://systeme.io/en/login` (app.systeme.io/blogs 404s; use `https://systeme.io/dashboard/blogs`).

1. Sites → Blogs. Existing blog: **MotoCity Blog** → `https://www.motocity.autos/blog` (id 477391). Don't create new blogs per post.
2. Posts → + Create → fill Title / Short description / URL Path → Save (creates draft).
3. Open post → editor → drag **Text** element into dropzone → type body.
4. Back in Posts list → ⋯ → Settings to verify/fix Title, description, slug. → ⋯ → Activate → "Activate now" to publish.

### Chrome gotchas (cost 20 minutes on first run — read this)

- **Synthesized typing randomly drops characters** ("Here's"→"Here'", "it"→"i", slug mangling). For ANY form field: use `read_page`/`find` to get the ref, then **`form_input` to set the value** — it's atomic and typo-proof. Only use `type` for the long body inside the page editor (no form_input target), then ALWAYS proofread with `get_page_text` and patch.
- First `type` into the text element may not fully replace the lorem placeholder — check for a leftover "Lorem ipsum..." tail and missing opening sentences; fix with cmd+Up / cmd+Down + Backspace repeat.
- Hyperlinking a phrase: click before first word → shift+click after last word → floating toolbar → link icon → set URL via form_input on the "Type in URL" field → check "Open link in a new tab" → Confirm → **Save** (top right), verify with JS: `document.querySelectorAll('a[href*="sa="]')`.
- New blogs ship with **3 lorem ipsum posts already PUBLISHED** — delete all 3 (⋯ → Delete → Confirm), with user permission.
- Save button gives no toast from the editor; click it, then Exit and trust the posts list.

## Step 4 — Images (verified specs)

| Asset | Size | Format | Weight |
|---|---|---|---|
| Blog featured image (post Settings → Image; doubles as social OG) | 1200×630 (1.91:1) | JPG/PNG | <300KB |
| Inline blog images (Image element, retina) | 1200px wide | JPG/PNG | <300KB |
| Newsletter hero | 1200×600 shown at 600 wide | JPG/PNG only (no WebP/SVG) | <200KB |

- Upload via any editor with "Optimize uploaded images" checked; reuse from "Your images" tab; copy URL for email use.
- Email images need absolute hosted URLs: `<figure style="text-align: center;"><img src="https://..." width="600"></figure>`.
- Inline blog images can be clickable: image settings → Action when image clicked → Open URL → affiliate link.
- Canva MCP is connected — generate 1200×630 + 1200×600 pairs there.

## Step 5 — Wrap-up checklist

- [ ] Post Activated (green check) and loads at live URL
- [ ] CTA href contains `?sa=` (verify via JS)
- [ ] Newsletter draft points at the LIVE post URL (update_newsletter)
- [ ] Test send to djscrtch1@gmail.com before real send; check {first_name} + links on phone
- [ ] Recipients = matching interest tags; send Tue–Thu 9–11am
- [ ] Offer Reddit/TikTok/Reels hooks pointing at the blog post (never raw affiliate link on social)
- [ ] Track: affiliate dashboard clicks/signups + newsletter open/click stats
