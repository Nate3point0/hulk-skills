# Systeme.io Embed + Thumbnail Templates

Copy these patterns. Swap the bracketed values per product.

## 0. THE RULE — how the app actually gets onto a Systeme.io page

Systeme.io's custom-HTML element **strips `<script>` tags**. Your app's JavaScript will not run if pasted in. Two valid paths:

**A. Live tool via iframe** — host the `.html` (Netlify Drop / GitHub Pages / Cloudflare Pages), then one line in a Custom-HTML element:
```html
<iframe src="https://YOUR-HOSTED-URL/app.html" style="width:100%;height:1100px;border:0;" loading="lazy"></iframe>
```
The JS runs on the hosted page, so it works inside the funnel. Height is fixed — pick a generous value, tell the user to nudge the px.

**B. Sell-as-download** — build the page with native drag-and-drop elements (below) and deliver the `.html` as the product. No code on the page.

## 1. Static decorative blocks (NO JavaScript — safe to paste)

These are plain styled `<div>`s with no scripts, so Systeme.io keeps them. Use for hero/bullets/guarantee visuals only — never the app logic. Set the element's desktop & mobile padding to 0.

```html
<!-- HERO BLOCK -->
<div style="background:#0f0f0f;color:#fff;padding:40px 20px;text-align:center;font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',Roboto,sans-serif;">
  <h1 style="font-size:1.6rem;margin:0 0 8px;letter-spacing:-0.5px;">[HEADLINE — use customer's exact phrase]</h1>
  <p style="color:#a0a0a0;font-size:1rem;margin:0 0 20px;">[One-line subhead]</p>
  <div style="font-size:2rem;font-weight:800;color:#00ff88;margin:0 0 16px;">$[PRICE]</div>
  <p style="color:#a0a0a0;font-size:0.85rem;margin:0 0 20px;">One-time. No subscription. Yours forever.</p>
  <a href="[CHECKOUT_URL]" style="display:inline-block;background:#00ff88;color:#000;padding:16px 40px;border-radius:10px;text-decoration:none;font-weight:700;font-size:1rem;">GET INSTANT ACCESS</a>
</div>

<!-- BULLETS BLOCK -->
<div style="background:#1a1a1a;color:#fff;padding:24px 20px;font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',Roboto,sans-serif;">
  <div style="margin-bottom:14px;font-size:0.95rem;">✅ <strong style="color:#00ff88;">[Benefit 1]</strong> — [detail]</div>
  <div style="margin-bottom:14px;font-size:0.95rem;">✅ <strong style="color:#00ff88;">[Benefit 2]</strong> — [detail]</div>
  <div style="font-size:0.95rem;">✅ <strong style="color:#00ff88;">[Benefit 3]</strong> — [detail]</div>
</div>

<!-- GUARANTEE BLOCK -->
<div style="background:#0f0f0f;color:#fff;padding:32px 20px;text-align:center;font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',Roboto,sans-serif;border-top:1px solid #2a2a2a;">
  <p style="color:#00ff88;font-weight:700;font-size:1.1rem;margin:0 0 8px;">30-Day Money-Back Guarantee</p>
  <p style="color:#a0a0a0;font-size:0.9rem;margin:0;">If it doesn't pay for itself on your next job, I'll refund every penny.</p>
</div>
```

**Two ways to host the actual app inside the funnel:**
- **Sell-then-deliver (default):** the funnel page sells; the buyer downloads the `.html` file as the product (upload it as a digital product / file in Systeme.io). Best for a paid tool.
- **Live demo embed:** to show the tool working on the page, host the `.html` somewhere and embed via `<iframe src="[URL]" style="width:100%;height:900px;border:0;"></iframe>` inside a custom-HTML element. Use for free lead-magnet versions.

## 2. Thumbnail SVG template

A self-contained SVG that renders anywhere (funnel image slot, social card). Keep text large — it must be legible as a small social thumbnail. Default 1200×630 (link/social) — for square Reels/IG use 1080×1080.

```svg
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1200 630" width="1200" height="630">
  <rect width="1200" height="630" fill="#0f0f0f"/>
  <rect x="40" y="40" width="1120" height="550" rx="24" fill="#1a1a1a" stroke="#2a2a2a"/>
  <text x="80" y="160" fill="#00ff88" font-family="Arial, sans-serif" font-size="34" font-weight="700">[EMOJI] [PRODUCT NAME]</text>
  <text x="80" y="250" fill="#ffffff" font-family="Arial, sans-serif" font-size="62" font-weight="800">[BIG HOOK LINE 1]</text>
  <text x="80" y="330" fill="#ffffff" font-family="Arial, sans-serif" font-size="62" font-weight="800">[BIG HOOK LINE 2]</text>
  <text x="80" y="430" fill="#a0a0a0" font-family="Arial, sans-serif" font-size="32">[Subhead / what it does in 6-8 words]</text>
  <rect x="80" y="480" width="280" height="72" rx="12" fill="#00ff88"/>
  <text x="220" y="527" fill="#000000" font-family="Arial, sans-serif" font-size="32" font-weight="700" text-anchor="middle">$[PRICE] · GET IT</text>
</svg>
```

Convert to PNG for platforms that won't take SVG: `rsvg-convert -w 1200 -h 630 thumb.svg -o thumb.png` (or any SVG→PNG tool). Provide the SVG by default; offer PNG if the user needs it.

## Brand palette (default — override if the product has its own)
- Background `#0f0f0f`, card `#1a1a1a`, border `#2a2a2a`
- Accent green `#00ff88`, dim accent `#00cc6a`
- Text `#ffffff`, dim text `#a0a0a0`
- System font stack: `-apple-system,BlinkMacSystemFont,'Segoe UI',Roboto,sans-serif`
