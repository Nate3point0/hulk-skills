# MotoCity Funnel Factory

**Trigger:** When building complete sales funnels or lead magnet ecosystems for automotive brand

**Platforms:** Systeme.io (API), local HTML/CSS generation

**MCP Required:** Yes — Systeme.io MCP server

## What It Does

Generates complete MotoCity funnel ecosystems from one brand skeleton. Builds opt-in pages, thank-you pages, email sequences, lead magnet PDFs, and product landing pages — all styled with brand tokens and ready to deploy. One command: full funnel in minutes.

## How to Use

1. Provide funnel type (e.g., "Car Buying Guide", "Insurance Secrets") and target audience
2. Claude generates: landing page HTML, email sequence copy, PDF lead magnet, thank-you sequence
3. Claude uploads to Systeme.io and returns live funnel link
4. You run ads, Claude tracks conversions and suggests optimizations

## Notes

- Funnel conversion baseline: 5-10% opt-in rate for automotive funnels (MotoCity average: 8.3%)
- Lead magnet PDFs: generate via Python + WeasyPrint, hosted on Systeme.io
- Email sequences: 5-email sequence + follow-up broadcasts work best for automotive
- Brand tokens: all pages use same CSS custom properties (one change updates everything)
- Testing: A/B test headlines and CTA copy; email subject lines drive 30-40% of opens
- Systeme.io courses: use funnels to capture emails, deliver course inside platform
- Automation: use webhooks to trigger n8n workflows on opt-in (Telegram notifications, CRM sync)
- Compliance: include GDPR/CCPA disclaimers on opt-in pages

---

**Created:** Nate (Ceepeezee), July 2026
**Last updated:** July 2026
**Status:** Production