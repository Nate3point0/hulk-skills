---
name: systemeio-funnel-blueprint
description: >
  Free Funnel Blueprint specialist for Systeme.io. Activate when the user wants to build
  a funnel on Systeme.io, asks "how do I set up a funnel", "what pages do I need", "build
  me a lead capture funnel", "help me get leads on Systeme.io", "I want to build my first
  funnel", "Systeme.io funnel setup", "free funnel blueprint", "what is a funnel",
  "how do I get started on Systeme.io", or any beginner-to-intermediate funnel request.
  This is a focused, entry-level tool — delivers ONE complete funnel build spec with copy,
  steps, and automation. No upsells, no overwhelm. Perfect starting point. Fire immediately
  without waiting for more context.
  Bundled reference: references/systemeio-docs.md for technical specs.
---

# Free Funnel Blueprint for Systeme.io

## What This Skill Delivers

One complete, ready-to-build funnel system on Systeme.io — the fastest path from zero to
a working lead generation and sales machine. Delivered as a step-by-step blueprint with
actual copy, automation logic, and a launch checklist.

Reference `references/systemeio-docs.md` for any platform-specific technical detail.

---

## Your Blueprint: The 5-Step Starter Funnel

This is the foundational funnel architecture that every Systeme.io business starts with.
It works for digital products, courses, coaching, affiliate offers — any niche.

---

### STEP 1 — Lead Capture Page

**Purpose:** Trade a free resource for an email address.

**Page Elements:**
- **Headline formula:** "Get [Specific Result] Without [Painful Alternative] — Free"
- **Subheadline:** One sentence that backs up the promise with specificity
- **Opt-in form:** First name + email only (fewer fields = more conversions)
- **CTA button text:** NOT "Submit" — use "Send Me The Free Blueprint →" or "Yes, I Want This!"
- **Below the fold:** 3 bullet benefits (what they'll learn/get), social proof line

**Systeme.io Build Steps:**
1. Dashboard → Funnels → Create → "Lead generation" type
2. Name your funnel (internal use only)
3. Step 1 = "Squeeze page" — use drag-and-drop editor
4. Add Form element → connect to your email campaign
5. Set Step 1 redirect to Step 2 (Thank-You page)

**Sample Headline Copy:**
> "Get Your First 100 Email Subscribers in 30 Days — Using Only Free Tools"

**Sample Subheadline:**
> "This free blueprint shows you the exact 5-step funnel I used — no tech skills, no ad budget required."

**Sample CTA:** "Send Me The Blueprint →"

---

### STEP 2 — Thank-You / Bridge Page

**Purpose:** Confirm delivery, warm the lead, set up the next step.

**Page Elements:**
- Confirmation headline: "You're in! Check your email for [Resource Name]."
- One paragraph: tell them what to expect next and when
- Bridge sentence: introduce your paid offer or next funnel step naturally
- Optional: embed a short video (60–90 sec) — face-to-camera, personal, direct

**Systeme.io Build Steps:**
1. Add Step 2 = "Thank you page" in your funnel
2. Keep it simple — one column, no nav links
3. If bridging to a sales page: add a button → redirect to Step 3

**Sample Copy:**
> "Your free blueprint is on its way — check your inbox in the next 2 minutes.
> While you wait: if you want me to walk you through this live and help you
> set up your entire system in one afternoon, I've got something for you below."

---

### STEP 3 — Sales Page (Optional for Lead Magnets, Required for Offers)

**Purpose:** Convert warm leads into buyers.

**Page Structure:**
1. **Hero section:** Headline (outcome) + subheadline (mechanism) + CTA button
2. **Problem section:** Agitate the pain point — be specific
3. **Solution section:** Introduce the offer as the bridge
4. **What's inside:** Benefit-driven bullet list (transformation, not features)
5. **Social proof:** Testimonials, screenshots, results
6. **Offer stack:** Show full value, then reveal price (anchoring)
7. **Guarantee:** Remove risk — 30-day money-back minimum
8. **Urgency close:** Why act now (bonus expiry, price increase, limited spots)
9. **Final CTA:** Repeat the buy button with a strong action phrase

**Systeme.io Build Steps:**
1. Add Step 3 = "Sales page" in your funnel
2. Add an Order Form as Step 4 (separate funnel step)
3. Connect sales page CTA button to order form URL

**Headline Formula:**
> "Finally: [Outcome] — Even If [Biggest Objection]"

**Example:**
> "Finally: A Complete Online Business in 30 Days — Even If You've Never Built a Funnel Before"

---

### STEP 4 — Order Form

**Purpose:** Frictionless checkout.

**Must-Haves:**
- Product name visible at top
- Price clearly displayed (no surprises)
- Guarantee badge near payment fields
- Trust seals (SSL, payment logos)
- **Order Bump:** One low-cost add-on, checkbox format, 1–2 sentence description

**Systeme.io Build Steps:**
1. Add Step 4 = "Order form" in your funnel
2. Create your product first in Products tab, then link to order form
3. Add order bump: Order Form step → "Bump" tab → add bump product
4. Set post-purchase redirect to Step 5

**Order Bump Copy Formula:**
> "⬛ YES — Add [Complementary Product] for just $[Price] (normally $[Higher Price]).
> [One sentence: what it does + why they need it now]."

---

### STEP 5 — Confirmation / Thank-You Page

**Purpose:** Deliver access, celebrate the purchase, set next step.

**Page Elements:**
- Celebration headline: "Welcome to [Product Name]! You made the right call."
- Access instructions (clear, numbered)
- What to do first (one specific action)
- Community link (if applicable)
- Upsell teaser (soft — "When you're ready for the next level…")

**Systeme.io Build Steps:**
1. Add Step 5 = "Thank you page"
2. Include direct link to course access / download / member area
3. This page also fires your post-purchase automation

---

## Automation: The Minimum Viable Setup

Three automation rules required for a working funnel:

**Rule 1 — Lead capture:**
- Trigger: Contact submits opt-in form
- Action: Add tag "Lead-[FunnelName]" → Enroll in Welcome Email Sequence

**Rule 2 — Purchase:**
- Trigger: Contact completes purchase of [Product]
- Action: Add tag "Customer-[ProductName]" → Grant course/product access → Send delivery email

**Rule 3 — No-purchase follow-up:**
- Trigger: Tag "Lead-[FunnelName]" added AND tag "Customer-[ProductName]" NOT present (after 3 days)
- Action: Enroll in Sales Email Sequence

**Systeme.io Build Steps:**
1. Dashboard → Automation → Rules → Create Rule
2. Set trigger (form submission, tag added, purchase)
3. Set action(s) in sequence
4. Test by submitting a form with a test email

---

## Your Launch Checklist

Before going live — check every item:

**Pages:**
- [ ] Lead capture page headline tested (is the offer clear in 3 seconds?)
- [ ] Opt-in form connected to email campaign
- [ ] Thank-you page redirect works
- [ ] Sales page CTA links to order form
- [ ] Order form product linked and price correct
- [ ] Order bump displays on checkout
- [ ] Confirmation page shows correct access instructions

**Automation:**
- [ ] Tag fires on opt-in form submission
- [ ] Welcome email sequence receives the tag trigger and sends Email 1 immediately
- [ ] Purchase tag fires after completed order
- [ ] Delivery/access email sends within 5 minutes of purchase
- [ ] All test emails received in inbox (not spam)

**Technical:**
- [ ] Custom domain connected (or Systeme.io subdomain active)
- [ ] All pages mobile-responsive
- [ ] Page load time under 3 seconds
- [ ] SSL active (https://)
- [ ] Test purchase completed end-to-end with real payment method

---

## What's Next

This blueprint covers the foundation. The full **Systeme.io Business Architect** system
extends this into:
- Complete email sequence system (Welcome → Nurture → Sales → Re-engagement)
- Online course architecture with drip scheduling
- Branded community with gating and retention automation
- Digital store with bundles, upsells, and post-purchase sequences

That's the paid system. This blueprint gets you live and making money first.

---

## Plan Note

Systeme.io **Free plan** supports basic funnels (verify current limits in `references/systemeio-docs.md`).
For unlimited funnels, automation rules, and email contacts — Startup plan or higher recommended.
