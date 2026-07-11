# BUILD YOUR FUNNEL PAGE — THE SIMPLE VERSION
*If you can copy and paste, you can do this. 10 minutes per page.*

---

## What you're building (the sandwich 🥪)

```
┌──────────────────────────┐
│  HTML BLOCK A  (the top) │  ← pretty design, copy-paste
├──────────────────────────┤
│  NAME BOX   [________]   │  ← real Systeme.io pieces
│  EMAIL BOX  [________]   │     (these do the actual work)
│  [  BIG GOLD BUTTON  ]   │
├──────────────────────────┤
│  HTML BLOCK B (the rest) │  ← pretty design, copy-paste
└──────────────────────────┘
```

The HTML blocks are the "bread" (they just look good).
The Systeme.io pieces are the "meat" (they collect emails and deliver files).

---

## Step-by-step (opt-in page)

**1. Make the funnel.**
Sales Funnels → Create → Custom. Add Step 1 (name it "Opt-in", type: squeeze page).
Add Step 2 (name it "Thank You", type: thank you page).

**2. Open Step 1 in the editor. Add a Section.**
Click the section's gear ⚙ → Background color → paste the page's BG hex
(it's in ASSEMBLY-GUIDE.md — example: health page = `#07201b`).

**3. Paste the top.**
Drag a **Raw HTML** element into the section → Edit code → paste ALL of
`block-A-top.html` → Save. Set the element's padding to 0 on all four sides.

**4. Add the real form.**
Right under it, drag in: **Input** (First name) → **Input** (Email) → **Button**.
Style them (one time — then save the block, see "The Shortcut" below):
- Inputs: dark background `#111111`, white text, radius 10
- Button: background = the page's accent hex, black bold text, radius 12, full width
- Button action: **Submit form** ← this is the magic. It saves the contact AND
  sends them to Step 2 automatically. No links to set up.

**5. Paste the bottom.**
Drag another **Raw HTML** below the button → paste ALL of `block-B-bottom.html`
→ Save. Padding 0 on all sides.

**6. Build Step 2 (thank-you page) the same way**, except the middle piece is
just one **Button** with action = **Download file** → upload that funnel's PDF.

**7. Check it live.**
⚠ Raw HTML does NOT show in the editor preview. That is NORMAL, not broken.
Publish, open the real link on your phone, fill the form with your own email,
and make sure you land on Step 2 and the download works.

---

## The Shortcut (do this after page #1) ✂

After you build your first form (inputs + button), **save it as a block**:
select the section/row → Save as template. Next page, insert your saved block
and change ONE thing: the button's background color to the new page's accent hex.
Same for the thank-you download button. Build once, reuse seven times.

---

## Legal pages (do once, takes 5 minutes)

1. Make one funnel called "Legal" with 3 steps (or 3 pages on your site):
   privacy, terms, disclosure.
2. Paste `legal/privacy-policy.html`, `legal/terms-of-service.html`,
   `legal/affiliate-disclosure.html` — each is one Raw HTML block. Done.
3. Copy each page's URL. In every funnel page's footer, the words
   Privacy / Terms / Disclosure are links marked UPDATE-ME — point them
   at these URLs.
*(For client builds: open gen_legal.py, change the 5 lines in TOKENS —
business name, site, email, date, state — and rerun. Instant rebrand.)*

---

## Golden rules (never break these)

1. Forms, download buttons, checkouts = ALWAYS real Systeme.io elements.
2. HTML blocks = looks only. Never build a form inside HTML.
3. Section background color must match the page hex, or you'll see seams.
4. Element padding on Raw HTML = 0/0/0/0. Always.
5. Test on the LIVE page, on a PHONE, with a REAL email. Every page. Every time.
