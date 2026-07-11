---
name: hulk-product-spinup
description: >
  Turn any HULK money idea into a finished, sellable digital product (prompt pack)
  ready to upload to Gumroad. Use when the user wants to "spin up a pack", "turn this
  idea into a product", "build a prompt pack for [niche]", "make a sellable pack",
  "package this idea", "new money product", "monetize this idea", or names a niche and
  wants a product fast. Produces: production .md, branded HTML, Gumroad PDF, .txt bonus,
  and a complete GUMROAD_UPLOAD_GUIDE (listing copy, 20 tags, price, SEO). Also rebuilds
  the master bundle and updates IDEAS.md. This is Ceepeezee's idea-to-revenue assembly line.
---

# HULK Product Spin-Up

Ceepeezee's repeatable pipeline for converting an idea into a packaged digital product.
A finished product = the same proven file set every time. Run this whenever a new idea
needs to become something sellable. More ideas are always coming — keep the rhythm.

## ⚠️ RULE #0 — Build OUTSIDE the watched inbox

NEVER write build files into `/Volumes/HULK-STORAGE/HULK-INBOX/**`. The autonomous-layer
watcher (`~/hulk/autonomous-layer/watcher.py`) relocates any `.md`/`.txt`/`.html`/`.py`
dropped there into the BrainVault taxonomy — it will eat an in-progress build mid-process.

**Always build in:** `/Volumes/HULK-STORAGE/PRODUCT-BUILD/prompt-packs/<slug>/`
(verified safe, persists). See memory `hulk-inbox-watcher`.

## What "done" looks like (the deliverable set)

Per product, in its folder:
- `<Name>_Production.md` — source content (the prompts)
- `<Name>.html` — branded HTML (auto-generated)
- `<Name>_Gumroad.pdf` — THE deliverable to upload (auto-generated, must be >1 page)
- `<Name>.txt` — plain-text bonus (auto-generated)
- `GUMROAD_UPLOAD_GUIDE.md` — listing copy, 20 tags, price, SEO, cover spec, launch wins

## The pipeline (run these steps)

### 1. Scope the product
- Get the niche/idea + target buyer. Pick a price: **$19** (broad/entry), **$29** (pro
  niche), **$39** (specialist/dev). Prices end in 7 or 9 (Nipsey's number = 7).
- Slug = kebab-case, e.g. `real-estate-pack`. Title = "<Niche> AI Pack".

### 2. Gather source (optional but better)
- Scan the vault for existing material to ground real prompts (not generic):
  `grep -rIl -i "<niche keywords>" "$HOME/Library/CloudStorage/GoogleDrive-motocityfix@gmail.com/My Drive/ObsidianVault/BrainVault" /Volumes/HULK-STORAGE/HULK-INBOX 2>/dev/null`
- Read the strongest 1-2 hits. Bake real specifics (pricing, platforms, the user's actual
  businesses: MotoCity/CarzShine, natefunkadelic, the 2 RNs) into the prompts.

### 3. Author the production .md
- Copy `assets/pack_template.md` as the skeleton. Fill it in.
- **Target ~45-60 prompts** across 8-12 categories (5-6 prompts each).
- Each prompt: `## Prompt N: <Title>` then a fenced code block containing a copy-paste
  prompt with `[BRACKET]` placeholders the buyer fills in. Make them genuinely useful and
  specific to the niche — this is the product's whole value.
- Keep markdown to the converter-friendly subset: `#`/`##`/`###`, fenced ``` code blocks,
  pipe tables, `**bold**`, `-`/`1.` lists, `---` rules. (No nested/complex markdown.)
- Always include: frontmatter (title/subtitle/author/date), QUICK START, WHAT YOU GET
  value table, the prompt sections, a "THE META-PROMPT" bonus, a 30-day plan table, and
  the sign-off `*Marathon style. All money in.*`
- For health/legal/financial niches, add scope/disclaimer language (see nurse-pack).

### 4. Convert to HTML / PDF / TXT
```bash
cd /Volumes/HULK-STORAGE/PRODUCT-BUILD/prompt-packs/<slug>
python3 ../../_build/md2pack.py <Name>_Production.md <Name>
# optional 3rd arg = accent hex (default brand orange #ff6b35)
```
Then verify the PDF rendered fully (not a 1-page cover from a race/error):
```bash
python3 -c "import re;d=open('<Name>_Gumroad.pdf','rb').read();print('pages:',len(re.findall(rb'/Type\s*/Page[^s]',d)))"
```
If `_build/md2pack.py` is missing, copy it from `assets/md2pack.py` in this skill.

### 5. Write the Gumroad upload guide
Create `GUMROAD_UPLOAD_GUIDE.md` with: deliverables list, product setup table
(name/type/price/slug), the full **DESCRIPTION** (copy-paste block, emoji bullets,
What You Get / categories / value stack / who-for / bonuses / 30-day guarantee), **20 tags**,
categories, a custom summary, a **cover-image spec** (1280x720, dark gradient #1a1a2e→#16213e,
orange accent, niche emoji), and **launch quick wins** (a $7 tripwire, a bundle/upsell tie-in,
a discount code, and where to do outreach). Mirror the existing pack guides for tone.

### 6. Update the catalog + bundle
- Rebuild the master bundle (zip all pack PDFs + a "Start Here" index) if this pack joins it.
- Update `BrainVault/IDEAS.md` "Packaged products" table with the new row.

## Brand constants
- Accent orange `#ff6b35`; dark gradient cover `#1a1a2e → #16213e`.
- Author line: `Ceepeezee / HULK AI System` (or `natefunkadelic` for music).
- Voice: marathon grind, confident, no corny corporate-speak. Sign-off: "Marathon style. All money in."
- Value stack math: list components → "Total Value $X" >> "Your Price $Y".
- Distribution: Gumroad (primary), own site/Systeme.io funnel, $97-ish bundle anchored vs individual total.

## Existing catalog (as of 2026-05-21)
HULK Command ($19), Car Dealer ($19), Nursepreneur ($29), Music Producer ($29),
Content Creator ($29), Agent Builder ($39). Bundle = AI Creator Master Pack ($97).
Built in `/Volumes/HULK-STORAGE/PRODUCT-BUILD/prompt-packs/`.

## Speed mode
If the user says "just spin it up": pick a sensible price + 50 prompts, build all files,
write the guide, and report the folder + page count. Don't stop to ask unless the niche
is genuinely ambiguous.
