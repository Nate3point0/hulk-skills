---
name: systeme-product-launcher
description: >
  Turn any completed build or workflow into a sellable Systeme.io product stack for
  Ceepeezee: course (delivery) + creator store product (sales page) + order bump +
  upsell + buyer tag + review-collection automation. Activate when the user says
  "productize this", "turn this build into a product", "launch the kit", "create the
  course", "add a store product", "set up the review engine", "sell this", or wants to
  package builds/build-instructions into revenue. Built around the Startup plan's real
  constraints (funnels and email campaigns MAXED — use the empty store-product, course,
  bump, upsell, coupon and workflow slots instead). First proven run: "The AI Email
  Machine - Build Kit" course, June 2026.
---

# Systeme.io Product Launcher

Packages a documented build into a full product stack. Strategy: builds are documented
for self-use anyway → the documentation IS the product. Every customer who buys a kit
also signs up to Systeme.io through the affiliate link = two revenue events per buyer.

## Account constraints (Startup $17/mo — check before building)

- Sales funnels 10/10 and email campaigns 10/10 are MAXED. Do NOT plan new funnels or
  campaigns without pruning. Sell via **creator store product pages** (0/15 used) instead.
- Empty slots to exploit: courses (5 cap, unlimited students), order bumps 0/10,
  1-click upsells 0/10, coupons 0/10, workflows 0/5, automation rules ~8 free.
- Existing assets: course id 632922 "The AI Email Machine - Build Kit"
  (motocity.autos/school/course/ai-email-machine), tag Buyer-AIEmailKit (id 2046729),
  3 creator stores, blog id 477391, affiliate ID sa0180716782ce4535d7f0b3ef221c7f646590fe91.

## The stack (build in this order)

1. **Buyer tag** — `mcp__systeme-io-official__create_tag` name `Buyer-<KitName>`. Instant, do via MCP.
2. **Course (delivery)** — Chrome: Assets → Courses → Add a new course.
   Name / domain www.motocity.autos / path kebab-case / theme 1 / Save.
   Add 5 modules (Add module → name → Save):
   M1 The System (what + why) · M2 Setup (APIs/MCP/keys) · M3 The Core Workflow ·
   M4 Publish/Operate · M5 Scale and Sell (templates + prompts).
   Lectures: draft ALL lecture content as files for user review FIRST, then paste in
   one Chrome pass (Add lecture → name, delay 0, template → Save → edit page).
3. **Store product (sales page)** — $27–47. Creator store product, delivery = course
   access (grant course in product settings). Store pages cost zero funnel slots.
4. **Order bump** — $9–17 swipe pack / template add-on on the checkout.
5. **1-click upsell** — $97 advanced tier (e.g. full Hulk stack: Telegram bot, Kimi gate, watcher).
6. **Review engine** — automation rule: purchase/enrollment → add Buyer tag →
   day-3 email asking for review + community invite; coupon code (e.g. REVIEW50) as thank-you.
   Reviews surface in community = compounding social proof.
7. **Front-end** — pair with systeme-content-publisher skill: blog post documents the
   build publicly, newsletter drives list to it, post CTA = affiliate signup; kit pitch
   goes to buyers/warm list. Never one asset doing two jobs (One Page One Purpose).

## Chrome gotchas (inherited from live runs — non-negotiable)

- Synthesized typing DROPS characters randomly. Any single-line field: locate with
  find/read_page → set via **form_input** (atomic). After any unavoidable typing,
  verify with get_page_text or a screenshot zoom and fix via the row's ⋯ → Settings modal.
- Module/course creation modals: name field + Save are centered and stable; the
  "Add module" button drifts down as modules accumulate — re-find it each cycle.
- Working courses URL: https://systeme.io/dashboard/courses (school/courses 404s).
- Course list shows drafts; Activate course + lectures before selling access.
- Always pause for user confirmation before: publishing, deleting anything, or any
  price/payment configuration. Never touch payment processor setup — hand to user.

## Pricing ladder (default)

Free (blog/lead magnet) → $9–17 bump → $27–47 kit → $97 advanced → affiliate commission
stacked on every buyer. Music packs (hulk-music-factory) ride identical rails as store
products #2+.

## Definition of done

- [ ] Course active with all lecture content loaded
- [ ] Store product live, test purchase path checked (user does payment config)
- [ ] Buyer tag fires on purchase (automation rule active)
- [ ] Review-ask email verified via test
- [ ] Front-end content published (content-publisher skill)
- [ ] Memory updated with product IDs and prices
