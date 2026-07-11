# eBay Optimizer Playbook

## Title rewriting patterns

A title's job is to match what a buyer types. 80 characters, spent like money.

Formula: `[Brand] [Model/Product] [Key attribute] [Size/Color] [Condition qualifier] [Style/Part #]`

**Example (from live store):**
- Weak: `NEW Compact 12V Tire Inflator – Accurate Pressure Gauge & Adapter Set!`
  Problems: "Compact" and "Accurate" aren't search terms; punctuation wastes chars; no brand.
- Strong: `12V Portable Tire Inflator Air Compressor Car Pump Pressure Gauge Adapter Kit`
  Every word is something a buyer types.

Rules of thumb:
- No promo words (WOW, L@@K, Must See), no leading "NEW" unless condition-critical, no exclamation marks.
- Include the style/part/model number when it exists — that's how serious buyers search (and how comps get found).
- Sneakers: `Nike Zoom Kobe 5 Playoff Carpe Diem 395780-001 Size 12 2010 Release` beats any adjective.

## Item specifics

Fill every recommended aspect — Cassini filters on them, and unfilled aspects mean the listing is invisible to filtered searches. Use `ebay_get_item_aspects_for_category` to see what's required/recommended for a category.

Danger aspects (INAD/defect bait if wrong): Signed, Autographed, Vintage, Year, Authenticity, Material, Country of Origin. When unsure, leave accurate-generic rather than aspirational.

## Comp-search recipes

Base URL: `https://www.ebay.com/sch/i.html?_nkw=<query>&LH_Sold=1&LH_Complete=1`

- Sneakers: `<model> <colorway> <style code>` — beware reissues (Protro, Retro) sharing names with originals at very different prices.
- Apparel/hats: `<team/brand> <model line> <type>` + filter mentally by NWT vs used.
- Kitchenware/small goods: brand + product type; if fewer than 3 comps, widen to the product type without brand and price at the category median.
- Read "Best offer accepted" prices as the true clearing price, not the strikethrough.

Pricing decision:
- 3+ solid comps → price at median comp, enable Best Offer, auto-accept ≈ 96% of ask, auto-decline ≈ 83%.
- 1–2 comps → price at comp +10%, revisit in 2 weeks.
- 0 comps → check active listings instead; undercut the cheapest credible active by 5%.

## Send offers via Chrome (walkthrough)

1. `tabs_context_mcp` (createIfEmpty) → navigate to `https://www.ebay.com/sh/lst/active`.
2. `find` "Send offers" → click the banner button. A modal opens listing eligible items.
3. Wait ~3s for eligibility to load (shows "Eligible (N)").
4. Click the Percent-off field, type `10`. Verify per-item offer prices render in green.
5. Leave "Send automated offer" (7 days) and "Allow counteroffers" checked.
6. Click "Send offers", wait, screenshot to confirm the green "Offers sent" banner.
7. Report which items got offers and which weren't eligible.

Eligibility rotates — a watcher who received an offer in the last ~30 days, or a listing with an active offer, won't show. Automated offers cover future watchers automatically.

## Sell Similar (stale-listing reset)

Listings 60+ days old with ~0 views are algorithmically dead. "Sell similar" (not Relist) creates a fresh item ID and re-triggers the 48–72h new-listing boost. Before resetting: rewrite the title, complete specifics, and fix price — resetting a bad listing just restarts a bad listing. Do this via Seller Hub in Chrome (select listing → Sell similar), end the old one after the new one is live.

## Revise via MCP — worked example

Kobe 5 repricing (July 2026), the call that finally worked:

```json
{
  "itemId": "196942733890",
  "fields": {
    "StartPrice": 599,
    "ListingDetails": { "MinimumBestOfferPrice": 500, "BestOfferAutoAcceptPrice": 575 },
    "ItemSpecifics": { "NameValueList": [ /* the COMPLETE set of specifics, not just the changed one */ ] }
  }
}
```

Failure sequence to avoid:
1. `StartPrice` alone → failed: auto-decline exceeded new price.
2. Adding Best Offer bounds but partial specifics → failed: "US Shoe Size is missing" (ItemSpecifics replaces all).
3. Full specifics + price + bounds in one call → `Ack: "Warning"` = success.

## Weekly cadence hooks

This skill is the action arm of the Monday scheduled compliance check. When the check flags watchers, stale listings, or price gaps, run the relevant sections here. Store context lives in memory (`ebay-account-status`) and the project folder docs (`ebay-compliance-routine.md`, `hybrid-pod-cricut-blueprint.md`).
