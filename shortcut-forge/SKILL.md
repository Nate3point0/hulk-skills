---
name: shortcut-forge
description: >
  Build, sign, and deliver Apple Shortcuts programmatically on macOS — no
  clicking through the Shortcuts editor. Generates the .shortcut plist,
  signs it with the `shortcuts sign` CLI, imports it on the Mac, and syncs
  to iPhone via iCloud. Activate whenever the user says "make me a
  shortcut", "build a shortcut", "automate this on my phone", "share sheet
  automation", "iphone automation", "shortcut for a client", or wants any
  iOS/macOS Shortcut created, fixed, signed, or packaged for sale. Also
  fire when a user wants to productize a shortcut as a digital product
  (sellable .shortcut file or iCloud link). First proven build: "Send Clip
  to Hulk" capture-lane shortcut, July 2026.
---

# Shortcut Forge

Build Apple Shortcuts as code on a Mac, sign them, and deliver to any
iPhone. Two delivery lanes: personal (import + iCloud sync) and revenue
(signed `.shortcut` file or iCloud share link sold as a digital product).

## Requirements

- macOS with the Shortcuts app (any Mac the agent can shell into)
- `shortcuts` CLI (ships with macOS 12+): verify with `shortcuts --help`
- For iPhone delivery: same Apple ID + iCloud sync for Shortcuts enabled

## Build workflow

1. **Interview.** Get: trigger (share sheet / home screen / automation),
   inputs (video, photo, text, URL), steps, and destination (Files
   provider, web request, clipboard). Keep it to 2-5 actions — shortcuts
   that need more logic should call a server endpoint instead.
2. **Write the plist.** XML plist with the keys in
   `references/plist-anatomy.md`. Use the action recipes in
   `references/action-recipes.md` — these are verified identifiers and
   parameter shapes, not guesses.
3. **Lint, sign, import:**

```bash
plutil -lint NAME.plist
cp NAME.plist "NAME.shortcut"
shortcuts sign --mode anyone -i "NAME.shortcut" -o "NAME-signed.shortcut"
open "NAME-signed.shortcut"      # imports into the Mac Shortcuts library
sleep 5 && shortcuts list | grep -i "NAME"   # verify import
```

4. **Verify + hand off.** Confirm it appears in `shortcuts list`. Tell the
   user: it syncs to iPhone via iCloud in ~1-2 min; rename to drop the
   "-signed" suffix; toggle "Show in Share Sheet" if it doesn't appear.

## Critical gotchas (each cost real debugging time)

- **Unsigned .shortcut files will not import** on iOS 15+/macOS 12+.
  Always `shortcuts sign --mode anyone`. The signer prints harmless
  `ERROR: Unrecognized attribute string flag '?'` lines — ignore them;
  only a nonzero exit code is a real failure.
- **`open` on the signed file auto-imports on Mac** — no dialog click
  needed in recent macOS. Verify with `shortcuts list`.
- **Share-sheet shortcuts** need BOTH `WFWorkflowTypes: [ActionExtension]`
  and `WFWorkflowInputContentItemClasses` listing the accepted types
  (`WFAVAssetContentItem` for video, `WFImageContentItem` for photos,
  `WFURLContentItem` for links).
- **You cannot pre-bake a Google Drive / third-party Files path** into a
  Save File action. Use `WFAskWhereToSave: true` — iOS remembers the
  location in Recents after the first save. Only iCloud Drive paths can
  be hardcoded.
- **Magic variables** are `attachmentsByRange` entries. Reference the
  share-sheet input with `Type: ExtensionInput`; reference a prior
  action's output with `Type: ActionOutput` + the `UUID` you assigned to
  that action's parameters. The placeholder char in the string is U+FFFC
  (`&#65532;` in XML).
- **Keep `WFWorkflowMinimumClientVersion` at 900** for wide compatibility.

## Delivery lanes

**Personal:** import on Mac (above) → iCloud syncs to iPhone.

**Sell/share (no shared Apple ID):**
- Signed `.shortcut` file: recipient opens it on iPhone, taps Add. This is
  the digital-product SKU — deliverable via Systeme.io course lesson,
  email attachment, or download link.
- iCloud link: on any device, Shortcuts → share sheet → Copy iCloud Link.
  Best for free lead magnets (revocable, always latest version).

## 💰 Productization pattern

Every client shortcut is a SKU. Standard stack:
- **Lead magnet (free):** one-action shortcut via iCloud link (e.g. "Save
  receipt to Drive")
- **Tripwire ($7-17):** 3-5 action workflow shortcut, signed file +
  30-second setup video
- **Core ($47-97):** shortcut pack (5-10 related shortcuts) + PDF setup
  guide, delivered as a Systeme.io course
- **Premium ($197+):** custom-built automation for the buyer's exact
  workflow (this skill IS the fulfillment engine — interview, build,
  sign, deliver in under 30 minutes)

Position by niche pain, not by "shortcuts": "Job-site photo filing for
contractors", "Content capture lane for creators".

## References

- `references/plist-anatomy.md` — full working plist skeleton (verified)
- `references/action-recipes.md` — verified action identifiers + params
