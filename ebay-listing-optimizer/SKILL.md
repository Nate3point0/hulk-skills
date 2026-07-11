---
name: ebay-listing-optimizer
description: >
  Audits Ceepeezee's live eBay store and makes listings actually sell: pulls seller standards and
  active listings via the eBay MCP, runs sold-comp price checks, rewrites weak titles/item specifics,
  sends offers to watchers, refreshes stale listings, and applies revisions directly via the API.
  Activate whenever the user says "optimize my eBay", "why isn't this selling", "fix my listings",
  "check my eBay store", "price check", "send offers", "make things sell", "eBay audit", "comp check",
  mentions a specific eBay listing that's sitting with no sales, or pastes an eBay item number or URL.
  Also fire during any weekly eBay review or when the Monday compliance check surfaces action items —
  don't wait for the word "optimize".
---

# eBay Listing Optimizer

Turn a stagnant eBay store into one that clears inventory. The seller (Ceepeezee, account `dailydealdepo`) has perfect quality metrics — the gap is always **sales velocity**, so every action here is judged by one question: does this make an item more likely to sell this week?

## Prerequisites

The eBay MCP (`mcp__ebay-mcp__*`) must have a user OAuth token. Check with `ebay_get_token_status`. If not authenticated, generate a login link with `ebay_get_oauth_url` — **use the trimmed scope list** (basic + sell.inventory + sell.account + sell.fulfillment + sell.analytics.readonly + sell.marketing + commerce.identity.readonly); the full default scope list throws `invalid_scope` on this app. Exchange the redirect's `code=` with `ebay_exchange_authorization_code`.

## The Optimization Pass (run in this order)

### 1. Pull the picture
- `ebay_find_seller_standards_profiles` — confirm standing and TRS progress (needs 100 txns / $1,000 trailing 12mo).
- `ebay_get_active_listings` — every listing with price, quantity, watch count.
- `ebay_get_traffic_report` if available — impressions/CTR tell you whether the problem is visibility (title/specifics) or conversion (price/photos).

### 2. Triage every listing into one bucket
| Signal | Bucket | Action |
|---|---|---|
| 3+ watchers, no sale | **Hot but priced wrong** | Send offer to watchers (see §4), consider small price drop |
| Views but no watchers | **Conversion problem** | Comp check → reprice; improve photos/description |
| Near-zero views, 60+ days old | **Visibility problem** | Rewrite title + specifics, then "Sell similar" to reset (new-listing boost) |
| Priced 1.5x+ above sold comps | **Fantasy price** | Reprice to comps (see §3) — this was the Kobe 5 case: $899 vs $450 comp = 3 views in 18 months |
| POD item, thin margin | **Margin problem** | Flag for Lane B (press-your-own) per the hybrid blueprint |

### 3. Comp check (the core move)
Search eBay sold listings via Claude in Chrome:
`https://www.ebay.com/sch/i.html?_nkw=<keywords+style/part number>&LH_Sold=1&LH_Complete=1`
- Match on style code / part number first, then size/condition. Same-model-different-year matters (an original release ≠ a Protro/reissue — can be 2–3x apart).
- Recommended price = recent sold comp for closest condition/size, +10–20% if the item is better condition, never more than ~1.3x the best comp.
- Note "Best offer accepted" comps — the sticker price wasn't the real price.

### 4. Send offers to watchers — use Chrome, not the MCP
⚠️ The MCP's `ebay_send_offer_to_interested_buyers` is broken (always returns "Offer details cannot be empty" regardless of payload). Go through Seller Hub instead:
1. Navigate to `https://www.ebay.com/sh/lst/active`, click the "Send offers" banner/button.
2. Set **Percent off = 10** (default; ask before going deeper), keep "Send automated offer" and "Allow counteroffers" checked — automated offers keep firing at future watchers for free.
3. Screenshot-confirm the "Offers sent" state. Note which listings weren't eligible (eBay rotates eligibility; automated offers will catch them later).

### 5. Apply revisions via `ebay_revise_listing`
Two hard-won gotchas:
- **ItemSpecifics is replace-all.** Sending one NameValueList entry wipes the rest and errors on required aspects. Read the current specifics first (listing page or `ebay_get_listing`), then send the complete set with your changes merged in.
- **Best Offer bounds:** if lowering StartPrice below the existing auto-decline, the call fails ("Auto decline amount cannot be greater than or equal to the Buy It Now price"). Set `ListingDetails.MinimumBestOfferPrice` (~83% of new price) and `BestOfferAutoAcceptPrice` (~96%) in the same call.
- `Ack: "Warning"` = success with informational notices. Only `Ack: "Failure"` is a failure.

### 6. Compliance guardrails (protect the perfect record)
- Never claim "Signed", autographed, or brand affiliations in specifics unless verifiably true — false specifics = INAD defect risk.
- Titles: max 80 chars, front-load buyer search keywords, no keyword-spam or ALL CAPS.
- POD/dropship listings: handling time must cover Printify production (5 business days). Never source fulfillment from retail sites.
- VeRO: no trademarked phrases/logos in design listings.

## Output format

End every optimization pass with:

```
📈 STORE SNAPSHOT — <date>
Standing: <level> | TRS gap: <txns>/<GMV>
⚡ ACTIONS TAKEN: <each revision/offer with before → after>
⚠️ NEEDS YOUR CALL: <decisions requiring the user — big price cuts, item-specific questions>
📋 NEXT: <what the next session or Monday check should pick up>
```

Ask before: price cuts >25%, ending any listing, or sending offers deeper than 10% off. Everything else, just do and report.

## Reference
- `references/playbook.md` — full triage detail, title-rewriting patterns, comp-search recipes, and the send-offers Chrome walkthrough. Read it when handling a full-store pass or an unfamiliar edge case.
