# TMF Trader

**Trigger:** When loading morning trading signals or analyzing GC/MNQ futures setups

**Platforms:** Mac, TradingView, futures trading platforms

**MCP Required:** No (but webhook integration recommended)

## What It Does

Loads TMF Lab morning signals for GC (gold) and MNQ (micro Nasdaq) futures. Pulls current price levels, identifies support/resistance, flags directional bias, and suggests entry/exit zones. Integrates with TradingView webhooks to auto-notify on signal changes.

## How to Use

1. At market open, ask Claude: "Load today's GC/MNQ signals"
2. Claude pulls TMF Lab data, charts current levels, and shows probable setups
3. Claude identifies your edge (volume profile, trend, mean reversion pattern)
4. Set alerts and monitor — Claude can send Telegram notifications on breakouts

## Notes

- TMF signals are best 30 min before market open through first 2 hours of RTH (Regular Trading Hours)
- GC and MNQ trade 23-hour sessions (Sun 6pm - Fri 5pm ET) — off-hours liquidity is thin
- Requires API key for TMF Lab data feed (subscription-based)
- TradingView webhook setup: use standard JSON format for price alerts
- Risk management: never risk more than 2% per trade; use hard stops
- MNQ moves fast in thin markets (early morning, last 30 min) — watch out for slippage

---

**Created:** Nate (Ceepeezee), July 2026
**Last updated:** July 2026
**Status:** Production