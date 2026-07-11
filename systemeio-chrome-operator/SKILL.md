---
name: systemeio-chrome-operator
description: >
  Systeme.io browser operator for Claude in Chrome. Activates when the user wants Claude
  to physically BUILD inside Systeme.io — not just plan it. Fire on: "build this funnel
  in Systeme.io", "click through and set it up", "do it in Systeme", "use Chrome to build
  the funnel", "record this workflow", "execute the funnel build", "go into Systeme.io and
  create it", "set up the automation rule", "create the email campaign in Systeme",
  "add the product to Systeme.io", or any request where the user wants Claude in Chrome
  to take physical action inside the Systeme.io dashboard. Pairs with systemeio-business-architect
  (generates the copy/specs) — this skill executes them. Always confirm user is logged into
  Systeme.io in Chrome before starting. Load workflows/build-lead-capture-funnel.md for
  the step-by-step funnel build script.
---

# Systeme.io Chrome Operator

## What This Skill Does

This skill drives Claude in Chrome to **physically operate inside Systeme.io** — clicking
buttons, filling fields, setting automations, and building the funnel the Architect Skill
planned. It's the execution layer.

**Pair with:** `systemeio-business-architect` (generates the blueprint + copy)  
**Requires:** Claude in Chrome extension active, logged into app.systeme.io

---

## Pre-Flight — Always Check First

Before taking any action inside Systeme.io, confirm:

1. Claude in Chrome extension is active (sidebar visible in browser)
2. User is logged into `app.systeme.io` in that same Chrome window
3. You have the copy/specs ready (from Architect Skill output or user input)
4. Permissions granted for `app.systeme.io` in the extension settings

If any of these are missing, **stop and tell the user what's needed** before proceeding.

---

## Safety Rules — Non-Negotiable

- **NEVER** click Delete, Remove, Archive, or Unpublish on existing content without explicit user confirmation
- **ALWAYS** pause and ask if you encounter a payment form, purchase confirmation, or plan upgrade prompt
- **ALWAYS** save before navigating away from any page editor
- **STOP** and notify user if you hit a CAPTCHA, login wall, or 2FA prompt
- **DO NOT** submit any real payment or subscription changes
- If uncertain about an action, describe what you're about to do and wait for confirmation

---

## Workflow Library

Load the relevant workflow file for step-by-step instructions:

| Task | Workflow file |
|------|--------------|
| Build lead capture funnel (squeeze + thank-you) | `workflows/build-lead-capture-funnel.md` |
| Set up email campaign | *(inline below)* |
| Add automation rule | *(inline below)* |
| Add product to store | *(inline below)* |

---

## Core Workflows (Inline)

### CREATE EMAIL CAMPAIGN

1. Navigate to `https://app.systeme.io/emails/campaigns`
2. Click "Create campaign"
3. Enter campaign name (use the sequence name from Architect output)
4. Click Save — campaign is now created and ready for emails
5. Click "Add email" for each email in the sequence:
   - Subject line: paste from Architect output
   - Delay: set Day 0 for Email 1, Day 1 for Email 2, etc.
   - Body: paste email body copy from Architect output
   - Click Save after each email
6. Confirm all emails appear in the campaign list in correct order

### ADD AUTOMATION RULE

1. Navigate to `https://app.systeme.io/automations/rules`
2. Click "Create rule"
3. Set trigger (opt-in, purchase, tag added — per Architect output)
4. Add actions in sequence (add tag, subscribe to campaign, grant course access)
5. Name the rule descriptively: "[Event] — [FunnelName]"
6. Click Save
7. Confirm rule appears in rules list as Active

### ADD PRODUCT TO STORE

1. Navigate to `https://app.systeme.io/products`
2. Click "Create product"
3. Fill in:
   - Product name: from Architect output
   - Price: as specified
   - Description: paste product description copy
4. Under "Delivery": set access type (course, file download, or custom)
5. Click Save
6. Confirm product appears in products list

---

## How to Use With Architect Skill

**Recommended flow:**

```
1. Run systemeio-business-architect → get full module blueprint with copy
2. Tell Claude: "Now use Chrome to build the funnel in Systeme.io"
3. This skill activates → loads the workflow file → executes step by step
4. Claude reports status after each major step
5. User reviews, approves, or corrects
6. Claude continues to next step
```

**Example prompt to trigger execution:**
> "I'm logged into Systeme.io. Use the funnel copy we just built and go create the lead capture funnel now."

---

## Reporting Format During Execution

After each workflow step, Claude reports:

```
✅ STEP [N] DONE — [What was completed]
   └─ [Any detail worth noting — field values entered, selections made]
⏳ NEXT — [What's coming next]
   └─ [Any input needed from user before proceeding]
```

If an error or unexpected screen appears:

```
⚠️ PAUSED — [Describe what's on screen]
   └─ [What Claude needs from user to continue]
```

---

## What This Skill Cannot Do

- Build pages with custom HTML/CSS beyond what Systeme.io's editor supports
- Upload video files to course lessons (user must do this manually)
- Connect custom domains (requires DNS access outside the browser)
- Configure payment processors (Stripe/PayPal setup — pause and hand to user)
- Access Systeme.io if user is not already logged in

For these tasks: pause, describe the gap, and give the user the exact manual steps to complete it.
