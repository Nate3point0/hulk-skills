---
name: systeme-app-builder
description: Build any small web app, calculator, tool, or interactive widget as a complete Systeme.io-ready sales bundle. Use this skill WHENEVER the user asks to build an app, build a tool, build a calculator, "make me an app", build a widget, create an interactive thing, or turn a product idea into something deployable — even if they don't mention Systeme.io by name. The user (Ceepeezee) sells small digital tools through Systeme.io funnels distributed via Reddit/TikTok/Reels, so EVERY app build must ship as a single self-contained HTML file plus Systeme.io embed blocks, a quick-start guide, landing copy, and a thumbnail. Default to this standard automatically; do not ask whether to apply it.
---

# Systeme.io App Builder

This skill encodes Ceepeezee's permanent build standard. Any time you build an app, tool, calculator, or interactive widget, produce the **full deployable bundle** below — not just the code. Speed and zero-friction deployment are the whole business model: hunt a pain → build a $17–$47 tool in ~2 hours → sell it through a Systeme.io funnel → distribute on social.

## The 5 non-negotiables

Every build must satisfy all five. Bake them in automatically.

1. **Always ship TWO app versions + a promo block.** Every build outputs both, no exceptions:
   - **`<SLUG>.html` — standalone/user-friendly.** Self-contained (inline CSS+JS, no external deps), full viewport, add-to-homescreen friendly, ready to download and ship. This is what the buyer gets.
   - **`<SLUG>_SIO.html` — Systeme.io embed version.** SAME app, identical features, but tuned to live inside a funnel via iframe: remove `maximum-scale`/`user-scalable=no` (zoom lock breaks embedded UX), drop fixed body margins/heights that clip in an iframe, let content flow to natural height, use a background that matches or is transparent. It differs from standalone ONLY in embed-tuning — never strip features.

   ⚠️ **CRITICAL — Systeme.io strips `<script>` tags from its custom-HTML element. JavaScript pasted into a page WILL NOT RUN.** So `_SIO.html` is not pasted — it is HOSTED (Netlify Drop / GitHub Pages / Cloudflare Pages) and embedded with ONE `<iframe src="...">` line in a Custom-HTML element. The JS runs on the hosted page. Iframe height is fixed (no auto-resize — parent listener would need JS SIO blocks); set a generous height and tell the user to adjust the px.

   - **`<SLUG>_SIO_PROMO.html` — static no-JS block.** A code-free styled HTML block (hero/bullets/CTA, no app logic) that pastes directly into a custom-HTML element and renders. Safe because it contains no `<script>`.
   - Always give the iframe paste-snippet pointing at the hosted `_SIO.html`.

   For sales-page copy, also provide it mapped to **native Systeme.io elements** (Heading/Text/Image/Button) for the download path. Export thumbnails to PNG/JPG — SIO image slots prefer those over SVG.

2. **Browser-friendly + simple.** Works offline. No login, no account, no install, no app store. Opens by double-click on any phone or laptop. Mobile-first responsive layout (max-width ~480px, large tap targets). No `localStorage`/`sessionStorage` reliance for core function (some embed contexts block it) — keep state in memory.

3. **Easy download + distribution.** Deliver as a downloadable file the buyer saves and opens with zero hassle. Always include a plain-English **Quick-Start** block (3–5 numbered steps) written for a non-technical end user.

4. **Marketing / showcase ready.** Include a **thumbnail** (a standalone `.svg` or simple HTML preview card) sized for funnel display and social (roughly 1200×630 or 1080×1080 framing). Provide social hooks and a screenshot-friendly UI so it displays well on the funnel and in Reels/Reddit.

5. **Save to the user's selected folder** so everything persists after the session, and present the files at the end.

## What to output every time

Produce these as separate files, named with the product slug + date (e.g. `MOBILE_DETAILER_PROFIT_CALC_0605`):

- `<SLUG>.html` — standalone user-friendly app (download/ship)
- `<SLUG>_SIO.html` — embed-tuned app for iframe hosting in a funnel
- `<SLUG>_SIO_PROMO.html` — static no-JS promo block to paste into a custom-HTML element
- `<SLUG>_LANDING_COPY.md` — headline, subhead, bullets, price/CTA, guarantee, FAQ, AND a "Systeme.io Embed Blocks" section with raw zero-padding HTML
- `<SLUG>_EMAIL_SEQUENCE.md` — delivery email + 1–2 follow-ups + abandoned-cart (optional but default yes)
- `<SLUG>_THUMBNAIL.svg` — display/social thumbnail
- `<SLUG>_QUICKSTART.md` — the 3–5 step end-user guide (can be folded into the delivery email instead)

See `references/embed-template.md` for the exact embed-block pattern and thumbnail structure to copy.

## Tool Hub + Reddit launch (every build plugs into the hub)

Tools don't live as one-off funnels — they live in a **Tool Hub**: one link-in-bio → a hub page of tool cards, each tool its own page with its own gate. So every build must ALSO output:

- `<SLUG>_HUB_CARD.html` — a static no-JS card (icon, name, one-line benefit, "Open" button linking to the tool's page) to drop onto the hub page.
- `<SLUG>_FUNNEL.md` — the matching funnel + Reddit launch plan: which gate (free-to-use / email-gated upgrade / paywall — pick per tool, default email-gated), the page wiring (iframe the hosted `_SIO.html`, two-step order form if paid), the 3 automation rules tagged `Lead-<slug>`/`Customer-<slug>`, and a value-first Reddit comment that deep-links to THIS tool's page (not the hub root).

**Gate guidance:** cold Reddit traffic converts on free working value first, then email, then buy. Never send cold traffic to a bare paywall. Capture email on the UPGRADE, not the entry. Use a custom domain so links don't read as a funnel. The tool must be share-worthy even with no funnel behind it. Full strategy: `REDDIT_TO_FUNNEL_PLAYBOOK.md` in the user's folder.

## Integrity rules (important)

These protect the user legally and protect the product's reputation:

- **Math must be real.** Before shipping any calculator, verify the formula with a quick script across realistic scenarios. Watch for compounding bugs (multiplying two values that should be one base + multipliers). A pricing tool that outputs absurd numbers destroys trust on first use.
- **No fabricated proof.** Never invent testimonials, customer names, results stats, or fake scarcity ("only 20 left"). FTC rules require endorsements to be real. Use clearly-labeled `[REAL TESTIMONIAL NEEDED]` placeholders until the user has genuine ones. Sell on the math and the guarantee instead.
- **Label synthesized data.** If market/pain research is inferred rather than scraped, say so; don't claim specific sources that don't exist.

## Build speed rule

If a build exceeds ~2 hours, cut scope, not the deadline. Fancy CSS and animations die first. Core function, correct math, and copy-to-clipboard never get cut.

## Workflow

1. Confirm the product idea and core function (one sentence). If pain-research intel exists, use the customer's exact phrase as the headline.
2. Build the self-contained HTML app. Verify any math with a script.
3. Write landing copy + embed blocks + email sequence.
4. Generate the thumbnail SVG and quick-start.
5. Save everything to the user's folder, then present the files.
