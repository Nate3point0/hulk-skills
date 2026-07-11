# HYBRID ASSEMBLY GUIDE — MotoCity pages

## How every page is put together (same recipe, 16 pages)

1. Page editor → add ONE **Section**. Section settings → **Background color** = the page's BG hex below. This is what makes the HTML blocks and native elements look like one continuous page.
2. Inside the section: drag **Raw HTML** → paste `block-A-top.html`. Element padding 0/0/0/0.
3. Directly below it, drag the **native elements** (see per-page row below), styled with the values in the next section.
4. Drag a second **Raw HTML** → paste `block-B-bottom.html`. Padding 0/0/0/0.
5. Preview mode does NOT render Raw HTML — always check the live/published URL, on your phone.

## Native element styling (match the brand — same values every page, accent varies)

**Input fields (First name, Email):**
- Background: #000000 at ~45% opacity if available, else #111111
- Text color: #FFFFFF · Placeholder: leave default
- Border: 1px, color = page ACCENT-LIGHT hex at low opacity (or #444444)
- Border radius: 10px · Vertical padding: 14px · Full width

**Submit / Download button:**
- Background: ACCENT-LIGHT hex (flat — native buttons don't do gradients; this matches the CTA gradient's light end)
- Text: #0C0C0C, bold, uppercase · Radius: 12px · Full width · Vertical padding: 17px
- Opt-in pages → action **Submit form** (sends contact to funnel's next step = the thank-you page)
- Thank-you pages → action **Download file** (upload the funnel's PDF to the button)

**Funnel wiring:** each funnel = 2 steps: Step 1 opt-in (squeeze page type) → Step 2 thank-you. Submit form automatically advances to step 2. Add the automation rule on step 1: Add tag `[funnel]-lead` + send welcome email with the PDF link as backup delivery.

## Per-page values

| Page | Section BG hex | Accent-light (button bg) | Accent-dark | Native elements between blocks | Button label |
|------|----------------|--------------------------|-------------|-------------------------------|--------------|
| 1-detail-service | `#081524` | `#7dd3fc` | `#0284c7` | — (link-only page, one block) |  |
| 2-health | `#07201b` | `#5eead4` | `#0d9488` | Form: First name + Email + Submit button | Send Me the Checklist |
| 3-car-calculator | `#1a1208` | `#f0c96b` | `#c98a12` | Form: First name + Email + Submit button | Get My Free Valuation |
| 4-sound-arsenal | `#140c24` | `#c4b5fd` | `#7c3aed` | Form: First name + Email + Submit button | Get My Free 110 Sounds |
| 5-gov-auction | `#1f0a0c` | `#fca5a5` | `#b91c1c` | Form: First name + Email + Submit button | Unlock Auctions &amp; Get the Free Guide |
| 6-dj | `#1f0a1a` | `#f9a8d4` | `#db2777` | Form: First name + Email + Submit button | Check Availability |
| 7-ai-hulk | `#0a2012` | `#86efac` | `#16a34a` | Form: First name + Email + Submit button | Send Me the Checklist |
| 8-fix-my-funnel | `#20100a` | `#fdba74` | `#ea580c` | Form: First name + Email + Submit button | Get the Free Kit |
| ty-1-detail | `#081524` | `#7dd3fc` | `#0284c7` | Button: action = Download file (attach PDF) | Submit |
| ty-2-health | `#07201b` | `#5eead4` | `#0d9488` | Button: action = Download file (attach PDF) | Submit |
| ty-3-cars | `#1a1208` | `#f0c96b` | `#c98a12` | Button: action = Download file (attach PDF) | Submit |
| ty-4-sound-arsenal | `#140c24` | `#c4b5fd` | `#7c3aed` | Button: action = Download file (attach PDF) | Submit |
| ty-5-gov-auction | `#1f0a0c` | `#fca5a5` | `#b91c1c` | Button: action = Download file (attach PDF) | Submit |
| ty-6-dj | `#1f0a1a` | `#f9a8d4` | `#db2777` | Button: action = Download file (attach PDF) | Submit |
| ty-7-ai | `#0a2012` | `#86efac` | `#16a34a` | Button: action = Download file (attach PDF) | Submit |
| ty-8-fix-my-funnel | `#20100a` | `#fdba74` | `#ea580c` | Button: action = Download file (attach PDF) | Submit |

## Notes
- HTML link-buttons (calendar, affiliate, cross-sell CTAs) stay inside the HTML blocks — links don't need native elements.
- The `#form` anchor sits at the bottom of Block A, so in-page 'Get the checklist' buttons scroll users to the native form right below it.
- 1-detail-service has no opt-in form → single block (all buttons are booking links).
- Sticky top bar lives in Block A and still works.
- Never wrap native elements in HTML; never rebuild forms in HTML.