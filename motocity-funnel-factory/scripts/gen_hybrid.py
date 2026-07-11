#!/usr/bin/env python3
"""Hybrid split generator: breaks each page into Raw HTML Block A + [native
elements] + Raw HTML Block B, with flat backgrounds so Systeme.io section
background makes the page seamless. Emits per-page assembly instructions."""
import os, re
import gen_pages as G          # PAGES dict + components (runs full-page gen, harmless)
import gen_thankyou as T       # TY dict

OUT = "/sessions/gifted-tender-fermi/mnt/outputs/hybrid"
FORM_MARK = "YOUR SYSTEME.IO FORM HERE"
DL_MARK = "NATIVE SYSTEME.IO DOWNLOAD BUTTON HERE"

def rgba(hexc, a):
    h = hexc.lstrip("#"); return f"rgba({int(h[0:2],16)},{int(h[2:4],16)},{int(h[4:6],16)},{a})"

def css_for(p):
    c = p["colors"]
    subs = dict(bg1=c["bg1"], bg2=c["bg2"], bg3=c["bg3"],
                accDark=c["accDark"], accLight=c["accLight"],
                accBorder=rgba(c["accLight"], .3),
                accTintA=rgba(c["accDark"], .12), accTintB=rgba(c["accLight"], .06),
                accGlow=rgba(c["accDark"], .35))
    css = G.CSS
    for k, v in subs.items():
        css = css.replace("{" + k + "}", v)
    # flat wrapper color (no gradient = no seams between blocks); set the
    # Systeme.io SECTION background to the same hex so native elements match
    css = re.sub(r"background:linear-gradient\(160deg[^;]+;", f"background:{c['bg2']};", css, count=1)
    return css

def wrap(p, inner, block_label):
    return (f"<!-- {p['name']} — {block_label} -->\n"
            f'<div class="mc-wrap" style="margin:0;padding:0;width:100%;">\n'
            f"<style>{css_for(p)}</style>\n{inner}\n</div>\n<!-- END {block_label} -->\n")

def split_page(p, marker):
    """Return (blockA_inner, blockB_inner, form_title, form_sub, btn_label)."""
    secs = p["sections"]
    idx = next((i for i, s in enumerate(secs) if marker in s), None)
    head = (f'<div class="mc-bar">{p["bar"]}</div>\n<div class="mc-container" style="padding-bottom:8px;">\n'
            f'<div class="mc-kicker">{p["kicker"]}</div>\n'
            f'<h1 class="mc-headline">{p["headline"]}</h1>\n'
            f'<p class="mc-subhead">{p["subhead"]}</p>\n')
    foot = "\n" + G.footer(p["disclaimer"], p.get("disclosure", False))
    if idx is None:
        return head + "\n".join(secs) + "\n</div>" + foot, None, None, None, None
    fc = secs[idx]
    title = re.search(r'mc-form-title">(.*?)</div>', fc)
    sub = re.search(r'mc-form-sub">(.*?)</div>', fc)
    btn = re.search(r'“(.*?)”', fc) or re.search(r'class="mc-cta"[^>]*>(.*?)</a>', fc)
    # Block A ends with the form heading (native fields sit right below)
    a = (head + "\n".join(secs[:idx]) +
         f'\n<div id="form" class="mc-form-title" style="margin-top:8px;">{title.group(1) if title else "Get Instant Access"}</div>'
         + (f'\n<div class="mc-form-sub">{sub.group(1)}</div>' if sub else "")
         + "\n</div>")
    # Block B starts with the trust line, then the rest
    b = ('<div class="mc-container" style="padding-top:8px;">\n'
         '<div class="mc-trust" style="margin-top:0;"><span class="lk">🔒</span>'
         '<span>No spam. Unsubscribe anytime. Your email is never shared.</span></div>\n'
         + "\n".join(secs[idx+1:]) + "\n</div>" + foot)
    return a, b, (title.group(1) if title else ""), (sub.group(1) if sub else ""), (btn.group(1) if btn else "Submit")

def emit(key, p, marker, native_kind, guide_rows):
    a, b, ftitle, fsub, btn = split_page(p, marker)
    c = p["colors"]
    d = os.path.join(OUT, key); os.makedirs(d, exist_ok=True)
    if b is None:
        open(os.path.join(d, "block-single.html"), "w").write(wrap(p, a, "SINGLE BLOCK (no native form on this page)"))
        guide_rows.append((key, c["bg2"], c["accLight"], c["accDark"], "— (link-only page, one block)", ""))
        return
    open(os.path.join(d, "block-A-top.html"), "w").write(wrap(p, a, "BLOCK A (TOP)"))
    open(os.path.join(d, "block-B-bottom.html"), "w").write(wrap(p, b, "BLOCK B (BOTTOM)"))
    clean_btn = re.sub(r"<[^>]+>", "", btn)
    guide_rows.append((key, c["bg2"], c["accLight"], c["accDark"], native_kind, clean_btn))

rows = []
for key, p in G.PAGES.items():
    emit(key, p, FORM_MARK, "Form: First name + Email + Submit button", rows)
for key, p in T.TY.items():
    emit(key, p, DL_MARK, "Button: action = Download file (attach PDF)", rows)

# ---------- assembly guide ----------
g = ["# HYBRID ASSEMBLY GUIDE — MotoCity pages",
     "",
     "## How every page is put together (same recipe, 16 pages)",
     "",
     "1. Page editor → add ONE **Section**. Section settings → **Background color** = the page's BG hex below. This is what makes the HTML blocks and native elements look like one continuous page.",
     "2. Inside the section: drag **Raw HTML** → paste `block-A-top.html`. Element padding 0/0/0/0.",
     "3. Directly below it, drag the **native elements** (see per-page row below), styled with the values in the next section.",
     "4. Drag a second **Raw HTML** → paste `block-B-bottom.html`. Padding 0/0/0/0.",
     "5. Preview mode does NOT render Raw HTML — always check the live/published URL, on your phone.",
     "",
     "## Native element styling (match the brand — same values every page, accent varies)",
     "",
     "**Input fields (First name, Email):**",
     "- Background: #000000 at ~45% opacity if available, else #111111",
     "- Text color: #FFFFFF · Placeholder: leave default",
     "- Border: 1px, color = page ACCENT-LIGHT hex at low opacity (or #444444)",
     "- Border radius: 10px · Vertical padding: 14px · Full width",
     "",
     "**Submit / Download button:**",
     "- Background: ACCENT-LIGHT hex (flat — native buttons don't do gradients; this matches the CTA gradient's light end)",
     "- Text: #0C0C0C, bold, uppercase · Radius: 12px · Full width · Vertical padding: 17px",
     "- Opt-in pages → action **Submit form** (sends contact to funnel's next step = the thank-you page)",
     "- Thank-you pages → action **Download file** (upload the funnel's PDF to the button)",
     "",
     "**Funnel wiring:** each funnel = 2 steps: Step 1 opt-in (squeeze page type) → Step 2 thank-you. Submit form automatically advances to step 2. Add the automation rule on step 1: Add tag `[funnel]-lead` + send welcome email with the PDF link as backup delivery.",
     "",
     "## Per-page values",
     "",
     "| Page | Section BG hex | Accent-light (button bg) | Accent-dark | Native elements between blocks | Button label |",
     "|------|----------------|--------------------------|-------------|-------------------------------|--------------|"]
for r in rows:
    g.append(f"| {r[0]} | `{r[1]}` | `{r[2]}` | `{r[3]}` | {r[4]} | {r[5]} |")
g += ["",
      "## Notes",
      "- HTML link-buttons (calendar, affiliate, cross-sell CTAs) stay inside the HTML blocks — links don't need native elements.",
      "- The `#form` anchor sits at the bottom of Block A, so in-page 'Get the checklist' buttons scroll users to the native form right below it.",
      "- 1-detail-service has no opt-in form → single block (all buttons are booking links).",
      "- Sticky top bar lives in Block A and still works.",
      "- Never wrap native elements in HTML; never rebuild forms in HTML."]
os.makedirs(OUT, exist_ok=True)
open(os.path.join(OUT, "ASSEMBLY-GUIDE.md"), "w").write("\n".join(g))
print("done:", len(rows), "pages")
