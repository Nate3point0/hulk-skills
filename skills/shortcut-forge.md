# Shortcut Forge

**Trigger:** When building, signing, or deploying Apple Shortcuts programmatically

**Platforms:** macOS, iOS, iPadOS

**MCP Required:** No (uses native Apple Shortcuts framework)

## What It Does

Builds, signs, and delivers Apple Shortcuts programmatically via the native Shortcuts framework. Creates automation for Mac startup tasks, Telegram notifications, file processing, and multi-device workflows. Deploys shortcuts to multiple devices via iCloud or direct delivery.

## How to Use

1. Describe the shortcut you need (e.g., "Daily routine: open apps, check email, set status")
2. Claude builds the shortcut XML and signs it with your Apple credentials
3. Claude deploys to your devices or generates a shareable link
4. Run from Siri, home screen, or automation triggers

## Notes

- Shortcut XML format: newer Shortcuts framework is different from legacy workflow
- Signing: requires Apple Developer credentials and valid provisioning profiles
- iCloud sync: shortcuts sync automatically if set up in Settings
- Reliability: shortcuts are solid for automation, but error handling is verbose
- File handling: shortcuts can read/write to Documents, Downloads, and iCloud Drive
- Automation triggers: time-based, location-based, app-based, or manual
- External calls: HTTP requests work well for webhooks (n8n, Zapier, Make)
- Mobile-first: iOS shortcuts run faster than Mac versions; test on device

---

**Created:** Nate (Ceepeezee), July 2026
**Last updated:** July 2026
**Status:** Production