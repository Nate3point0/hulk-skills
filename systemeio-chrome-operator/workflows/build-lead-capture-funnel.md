# Systeme.io Chrome Workflow — Lead Capture Funnel Build
# Purpose: Claude in Chrome follows this script to physically build a funnel inside Systeme.io
# How to use: Open this file, give Claude in Chrome the instructions below, or record it once
# and save as a repeatable workflow inside the extension.
#
# ── PRE-FLIGHT ──────────────────────────────────────────────────────────────
# Before starting, confirm:
# [ ] You are logged into Systeme.io in Chrome (app.systeme.io)
# [ ] You have the Architect Skill output open (copy, headlines, automation logic)
# [ ] Claude in Chrome extension is active (sidebar visible)
# [ ] You have granted Claude permission to interact with app.systeme.io

# ══════════════════════════════════════════════════════════════════════════════
# WORKFLOW 1: CREATE A NEW FUNNEL
# ══════════════════════════════════════════════════════════════════════════════

STEP 1 — Navigate to Funnels
  Go to: https://app.systeme.io/funnels
  Wait for the funnels dashboard to load.

STEP 2 — Create new funnel
  Click the button labeled "Create" or "+ New funnel"
  When the modal appears:
    - In the "Funnel name" field, type: [INSERT FUNNEL NAME]
    - Select funnel type: "Collect leads" (for lead capture funnel)
    - Click "Save" or "Create"
  Wait for the funnel editor to open.

STEP 3 — Confirm funnel was created
  Verify you are now inside the funnel editor showing funnel steps.
  The first step "Squeeze page" should be visible.

# ══════════════════════════════════════════════════════════════════════════════
# WORKFLOW 2: BUILD THE SQUEEZE PAGE (Lead Capture)
# ══════════════════════════════════════════════════════════════════════════════

STEP 4 — Open the squeeze page editor
  Click "Edit page" on the Squeeze Page step.
  Wait for the drag-and-drop page editor to fully load.

STEP 5 — Edit the headline
  Click on the main headline text block on the page.
  Clear existing text.
  Type: [PASTE HEADLINE FROM ARCHITECT SKILL OUTPUT]
  Click outside the text block to deselect.

STEP 6 — Edit the subheadline
  Click on the subheadline text block.
  Clear existing text.
  Type: [PASTE SUBHEADLINE FROM ARCHITECT SKILL OUTPUT]
  Click outside.

STEP 7 — Edit the CTA button text
  Click on the button element.
  Find the button text field.
  Clear and type: [PASTE CTA TEXT e.g. "Send Me The Blueprint →"]
  Click outside.

STEP 8 — Edit bullet points (if present)
  For each bullet point block:
    Click the bullet text.
    Clear and type the benefit copy from the Architect Skill output.
  Click outside after each edit.

STEP 9 — Save the page
  Click "Save" in the top right of the page editor.
  Wait for the save confirmation.
  Click "Back to funnel" or the back arrow to return to funnel steps.

# ══════════════════════════════════════════════════════════════════════════════
# WORKFLOW 3: BUILD THE THANK-YOU PAGE
# ══════════════════════════════════════════════════════════════════════════════

STEP 10 — Add Thank-You page step
  In the funnel steps view, click "Add step" or the "+" icon after Squeeze page.
  Select step type: "Thank you page"
  Click "Save" or "Add"

STEP 11 — Edit Thank-You page
  Click "Edit page" on the Thank-You step.
  Wait for page editor to load.
  Click on the headline text block.
  Clear and type: [PASTE THANK-YOU HEADLINE FROM ARCHITECT SKILL]
  Click on the body text block.
  Clear and type: [PASTE CONFIRMATION COPY]
  Click "Save"
  Return to funnel steps.

# ══════════════════════════════════════════════════════════════════════════════
# WORKFLOW 4: CONNECT THE OPT-IN FORM TO AN EMAIL CAMPAIGN
# ══════════════════════════════════════════════════════════════════════════════

STEP 12 — Go back into Squeeze page editor
  Click "Edit page" on Squeeze Page step.

STEP 13 — Click on the form element
  Click directly on the opt-in form (the email input + button area).
  Look for "Form settings" or a gear icon in the element toolbar.
  Click it.

STEP 14 — Connect to email campaign
  In Form Settings:
    - "After opt-in" or "On submit" → select: "Add to campaign"
    - Campaign dropdown → select or type: [NAME OF WELCOME CAMPAIGN]
    - If campaign doesn't exist yet: note to create it first in Emails tab
  Click "Save" or "Apply"

STEP 15 — Set redirect after opt-in
  Still in form settings:
    - "Redirect to" → select: "Next funnel step" (or paste Thank-You page URL)
  Click Save.
  Return to funnel steps.

# ══════════════════════════════════════════════════════════════════════════════
# WORKFLOW 5: SET UP AUTOMATION RULE (Tag on Opt-In)
# ══════════════════════════════════════════════════════════════════════════════

STEP 16 — Navigate to Automation Rules
  Go to: https://app.systeme.io/automations/rules
  Click "Create rule" or "+ New rule"

STEP 17 — Configure the trigger
  Trigger type: "Opt-in form submitted"
  Select funnel: [YOUR FUNNEL NAME]
  Select step: Squeeze page

STEP 18 — Configure the action
  Action type: "Add tag"
  Tag name: Lead-[FunnelName]  (e.g. Lead-FreeBlueprintFunnel)
  If tag doesn't exist, type the new tag name — Systeme.io will create it.
  Click "Add action"

STEP 19 — Add second action (enroll in campaign)
  Click "Add action" again
  Action type: "Subscribe to campaign"
  Select campaign: [WELCOME SEQUENCE CAMPAIGN NAME]
  Click Save.

STEP 20 — Name and save the rule
  Name the rule: "Lead Capture — [FunnelName]"
  Click "Save"

# ══════════════════════════════════════════════════════════════════════════════
# WORKFLOW 6: VERIFY END-TO-END
# ══════════════════════════════════════════════════════════════════════════════

STEP 21 — Get funnel share URL
  Return to funnel steps view.
  Click "Share" or look for the funnel URL at the top of the steps view.
  Copy the funnel URL.

STEP 22 — Open funnel URL in a new tab
  Open the copied URL.
  Confirm the lead capture page loads correctly.
  Check: headline visible, form present, button text correct.

STEP 23 — Test opt-in (use a test email)
  Submit the form with email: test+[timestamp]@yourdomain.com
  Confirm redirect to Thank-You page fires correctly.

STEP 24 — Verify contact was created
  Go to: https://app.systeme.io/contacts
  Search for the test email.
  Confirm contact exists with correct tag applied.

STEP 25 — Verify email sequence enrolled
  Click on the test contact.
  Check "Campaigns" tab — confirm Welcome sequence is active.

# ══════════════════════════════════════════════════════════════════════════════
# DONE — CHECKLIST BEFORE MARKING COMPLETE
# ══════════════════════════════════════════════════════════════════════════════

LAUNCH CHECKLIST:
  [ ] Squeeze page headline matches Architect Skill output
  [ ] CTA button text is not "Submit"
  [ ] Thank-you page loads after form submit
  [ ] Contact appears in Contacts tab after test opt-in
  [ ] Tag "Lead-[FunnelName]" applied to test contact
  [ ] Welcome sequence enrolled on test contact
  [ ] Funnel URL accessible without login

# ══════════════════════════════════════════════════════════════════════════════
# NOTES FOR CLAUDE IN CHROME
# ══════════════════════════════════════════════════════════════════════════════
#
# - If a modal or confirmation dialog appears at any step, read it and confirm
#   unless it involves payment or deletion — pause and ask user first.
# - If a text field is not editable by clicking, try double-clicking.
# - If the page editor takes more than 10 seconds to load, report it.
# - Always save before navigating away from the page editor.
# - Do not click "Delete", "Remove", or "Archive" on any existing funnel steps
#   without explicit user confirmation.
# - If you encounter a CAPTCHA or login wall, stop and notify the user.
