---
name: systeme-master
description: Master reference for building anything on Systeme.io — funnels, pages, order forms, courses, email campaigns, automation rules, affiliate programs, domains/deliverability, the public API, and the MCP server. Use this skill WHENEVER the user asks how to do ANYTHING on Systeme.io, mentions a Systeme.io funnel/page/order-form/course/campaign/tag/automation, asks where a setting lives, hits an error or "it's not working" on the platform, or needs platform-accurate build steps. This is Ceepeezee's primary platform — default to consulting it so answers are correct the first time with no back-and-forth. Covers the exact UI paths, element names, and the real constraints (e.g. how custom HTML/JS actually works). Do NOT guess Systeme.io behavior from general knowledge; read the relevant reference file.
---

# Systeme.io Master

Ceepeezee's go-to platform. The whole point of this skill is **no mistakes, no back-and-forth** — answers grounded in the actual help docs, not assumptions. The reference library in `references/` is scraped directly from help.systeme.io. When a question touches a specific feature, READ the matching reference file before answering.

## How to use this skill

1. Identify which area the task touches (funnel, order form, course, email, automation, domain, API/MCP, editor/embeds).
2. Open the matching file in `references/` and follow the real UI path and element names.
3. Give the user exact steps: which menu, which element to drag, what to name things.
4. For anything code/embed-related, follow the **Critical platform rules** below — this is where mistakes happen.

## Critical platform rules (memorize these — they cause the most errors)

### Custom HTML / CSS / JS (`references/html_css_js_embeds.txt`)
- Systeme.io **DOES** support custom code via three places: the **Raw HTML** element (drag onto a page), the page **Settings → Tracking** header/footer sections, and global Sales-Funnel tracking settings.
- **Never include these tags** in pasted code: `<head></head>`, `<body></body>`, `<html></html>`, `<footer></footer>`. Including them breaks the block.
- **Raw HTML does NOT render in Preview mode — only on the live/published page.** This is the #1 reason people think their embed "doesn't work." Always tell the user to check the live page, not preview.
- **iframes:** paste the bare `<iframe src="..."></iframe>` with NO wrapping `<div>`. A wrapping div is explicitly called out as incorrect.
- **Practical upshot for embedding a JS app/calculator:** host the app's `.html` externally (Netlify/GitHub Pages/Cloudflare Pages) and embed it with a bare iframe. This is reliable. Pasting a full app's inline `<script>` into a Raw HTML element is less reliable across the editor — prefer the iframe for interactive tools. (This is why Ceepeezee's app builds ship a hosted `_SIO.html` + iframe snippet; see the `systeme-app-builder` skill.)

### Funnel structure (`references/custom_page_editor.txt`)
- Pages are built from **Sections → Rows (columns) → Elements**. You drag a Section, it auto-includes a row+column, then drop Elements (Text, Image, Video, Button, Raw HTML, Order bump, Two-step order form) inside.
- Funnel types include Lead generation and Custom. Each funnel is a series of **Steps** (squeeze page, thank-you, sales page, order form, etc.).

### Order forms & payments (`references/order_bump.txt`, `two_step_order_form.txt`, `sell_course.txt`)
- **Order bump:** configured in the payment page settings (Add order bump → choose Physical/Digital → attach resource: course, bundle, tag, or community → set a price), THEN drag the **Order bump** element onto the page body so it's visible.
- **Two-step order form:** captures contact info before payment, so non-completers still join your list. Drag the **Two-step order form** element. Trigger automations with the **"Funnel step form subscribed"** trigger.
- Digital product resources you can deliver: Courses, Course bundles, Tags, Communities. (Calendar events can't be an order-bump resource.)
- Physical product fulfillment is NOT handled by Systeme.io — you ship externally.

### Automation (the minimum viable pattern)
- Menu → Automations → Rules → Create. Common triggers: form submission, **Tag assigned**, purchase completed, **Funnel step form subscribed**. Actions: add tag, send email, enroll in campaign, grant course access.
- Standard 3-rule funnel: (1) opt-in → tag Lead-X → welcome sequence; (2) purchase → tag Customer-X → grant access + delivery email; (3) has Lead-X AND NOT Customer-X after N days → sales sequence.
- Tags are the backbone of segmentation. Assign via automation rules OR via the Resources section of a payment page OR manually in CRM → Contacts.

### Courses (`references/create_course.txt`, `sell_course.txt`)
- Structure: Course → Modules → Lectures. Assets → Courses → Add new course.
- "Delay after previous lecture" controls **drip** scheduling. Access types when selling: Full, Partial (specific modules), Drip (gradual). Can also set a specific access start date and an expiration delay (days).

### Email (`references/email_campaign.txt`)
- Campaigns live under Emails → Campaigns. Each campaign holds a series of emails with configurable send delays, times, and days. Classic vs Visual editor — **switching editors mid-email loses your content.**
- Deliverability: authenticate your sending domain (DKIM/SPF) and set a **DMARC** record. See `improve_deliverability.txt`, `domain_auth_email.txt`, `dmarc_record.txt`.

### Domains (`references/connect_domain.txt`)
- Settings → Custom Domain → Add domain. A root domain can only point to ONE website. Subdomain setup is a separate path.

### Affiliate program (`references/affiliate_program.txt`, `affiliate_links.txt`)
- Settings → Affiliate Program. Defaults mirror Systeme.io's own: 40% commission, $30 min payout, 0% second tier, 30-day payout delay. Commissions paid on the 10th monthly.
- Affiliate link format: `https://yourpage?sa=AFFILIATEID`. Use the `{affiliate_id}` email variable to send each contact their unique link. Tag affiliates via a dedicated opt-in page.

### Integrations
- Payments: Stripe (`stripe_integration.txt`), PayPal (`paypal_integration.txt`), Cash on delivery (`cash_on_delivery.txt`).
- Email sending: SendGrid API (`sendgrid_api.txt`).
- Booking: `booking_calendar.txt`. Blog: `create_blog.txt`. Homepage: `define_homepage.txt`. A/B test: `ab_test.txt`. Contacts import/export: `import_export_contacts.txt`.

### Public API & MCP (`references/public_api.txt`, `mcp_server.txt`)
- **Public API** scope: contacts, tags, subscriptions, newsletters. It doesn't trigger automations directly, but API actions (create contact, assign tag) DO fire the automations you've set up. Docs: developer.systeme.io.
- **MCP server** lets Claude/ChatGPT connect directly to the account for **contact, tag, custom-field, and newsletter management** via natural language. Generate a key: Settings → MCP & API keys → MCP keys → Create. Keys last max 90 days, max 2 at a time, no OAuth yet. Docs: developer.systeme.io/docs/mcp-server.

## Reference index

Read the file that matches the task:

| Area | File |
|------|------|
| Custom HTML/CSS/JS, iframes, Raw HTML | `html_css_js_embeds.txt` |
| Page editor: sections/rows/elements | `custom_page_editor.txt` |
| Order bump | `order_bump.txt` |
| Two-step order form | `two_step_order_form.txt` |
| Configure a button | `configure_button.txt` |
| Downloadable file delivery | `downloadable_file.txt` |
| Link funnel to external site | `link_funnel_external.txt` |
| Create / sell a course | `create_course.txt`, `sell_course.txt` |
| Email campaign setup | `email_campaign.txt` |
| Create tag / add tags | `create_tag.txt`, `add_tags.txt` |
| Import/export contacts | `import_export_contacts.txt` |
| Affiliate program / links | `affiliate_program.txt`, `affiliate_links.txt` |
| Connect domain | `connect_domain.txt` |
| Email deliverability / auth / DMARC | `improve_deliverability.txt`, `domain_auth_email.txt`, `dmarc_record.txt` |
| Stripe / PayPal / Cash on delivery | `stripe_integration.txt`, `paypal_integration.txt`, `cash_on_delivery.txt` |
| SendGrid | `sendgrid_api.txt` |
| Booking calendar | `booking_calendar.txt` |
| Blog | `create_blog.txt` |
| Homepage | `define_homepage.txt` |
| A/B test | `ab_test.txt` |
| Add image | `add_image.txt` |
| Public API | `public_api.txt` |
| MCP server | `mcp_server.txt` |
| Everything (raw scrape) | `priority_scraped.json` |

When a reference file doesn't fully answer something, the live source is help.systeme.io — search there and update the relevant reference file so the library keeps improving.
