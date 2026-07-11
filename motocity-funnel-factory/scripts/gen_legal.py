#!/usr/bin/env python3
"""Legal page generator — Privacy Policy, Terms of Service, Affiliate Disclosure.
Branded single-block HTML for Systeme.io Raw HTML. Reusable: swap the TOKENS
dict for any client build. NOT legal advice — template baseline."""
import os
import gen_pages as G

TOKENS = dict(
    BIZ="City Funk Entertainment",
    SITE="motocity.autos (and moto-city.systeme.io pages)",
    EMAIL="admin@motocity.autos",
    DATE="July 7, 2026",
    STATE="California, USA",  # UPDATE-ME if different
)

COLORS = dict(accDark="#c98a12", accLight="#f0c96b", bg1="#0d0a07", bg2="#1a1208", bg3="#2a1c0a")

def sec(h, *paras):
    out = G.h2(h)
    for p in paras:
        out += f'<p class="mc-body" style="text-align:left;">{p}</p>'
    return out

def page(key, kicker, headline, sections_html, disclaimer):
    p = dict(name=key.upper(), colors=COLORS, bar="MotoCity · " + kicker,
             kicker=kicker, headline=headline,
             subhead=f"Last updated: {TOKENS['DATE']}",
             sections=[sections_html], disclaimer=disclaimer)
    return G.render(key, p)

T = TOKENS
privacy = "".join([
 sec("Who We Are", f"{T['BIZ']} operates {T['SITE']}. Contact: {T['EMAIL']}."),
 sec("What We Collect", "When you fill out a form we collect your first name and email address. Our pages also use standard analytics and advertising pixels (such as Meta and TikTok) that collect device and usage information via cookies."),
 sec("How We Use It", "To deliver the free guides and downloads you request, send you emails you signed up for (you can unsubscribe anytime with one click), respond to booking and service inquiries, and measure how our pages perform."),
 sec("What We Never Do", "We never sell your personal information. We never share your email with third parties for their own marketing."),
 sec("Third-Party Services", "Our site runs on Systeme.io (hosting, forms, email). Bookings use Google Calendar. Some links go to third-party sites (including affiliate partners) — their privacy policies apply once you leave our pages."),
 sec("Your Rights", f"You can request a copy of your data or ask us to delete it at any time by emailing {T['EMAIL']}. Unsubscribe links are in every email."),
 sec("Data Retention & Security", "Contact data is stored in Systeme.io for as long as you remain subscribed or as required for business records. We use reputable platforms with industry-standard security."),
 sec("Children", "Our services are not directed at children under 13, and we do not knowingly collect their data."),
 sec("Changes", "We may update this policy; the date above always reflects the current version."),
 sec("Contact", f"Questions: {T['EMAIL']}"),
])

terms = "".join([
 sec("Agreement", f"By using {T['SITE']} you agree to these terms. If you do not agree, please do not use the site."),
 sec("What We Provide", "Free downloadable guides, digital products (sound packs, courses, kits), DJ and detailing services, and informational content."),
 sec("Digital Products", "Digital purchases are delivered instantly. Unless stated otherwise on the offer page, paid digital products include a 30-day money-back guarantee — email us for a full refund, no questions asked."),
 sec("Services & Bookings", "Service bookings (detailing, DJ, consulting) are confirmed on deposit and subject to availability. Quotes are provided before work begins. Cancellation terms are stated at booking."),
 sec("Licenses", "Sound packs and samples are licensed as described in the LICENSE.txt included with each download. Free guides are for personal use and may not be resold."),
 sec("No Guarantees", "Content about business, flipping, auctions, trading, or income is educational. Results vary. Nothing on this site is financial, legal, or professional advice, and past results do not guarantee future outcomes."),
 sec("Affiliate Relationships", "Some links are affiliate links — see our Affiliate Disclosure. We only recommend tools we actually use."),
 sec("Acceptable Use", "Do not misuse the site, attempt to access other users' data, or copy and resell our content or designs."),
 sec("Limitation of Liability", f"To the maximum extent permitted by law, {T['BIZ']} is not liable for indirect or consequential damages arising from use of the site or its content."),
 sec("Governing Law", f"These terms are governed by the laws of {T['STATE']}."),
 sec("Contact", f"Questions: {T['EMAIL']}"),
])

disclosure = "".join([
 sec("The Short Version", f"Some links on {T['SITE']} are affiliate links. If you click one and sign up or buy, {T['BIZ']} may earn a commission. It never costs you anything extra."),
 sec("Which Links", "Current affiliate relationships include Systeme.io (the platform this site runs on) and Gov-Auctions.org (government auction access, via ClickBank). This list may grow — this page always reflects current partners."),
 sec("Our Rule", "We only recommend tools and services we personally use in this business. Every claim about them is based on our own experience."),
 sec("FTC Compliance", "This disclosure is made in accordance with the Federal Trade Commission's 16 CFR Part 255: Guides Concerning the Use of Endorsements and Testimonials in Advertising."),
 sec("Contact", f"Questions about any partnership: {T['EMAIL']}"),
])

OUT = "/sessions/gifted-tender-fermi/mnt/outputs/legal"
os.makedirs(OUT, exist_ok=True)
note = f"© 2026 {T['BIZ']}. This page is provided for transparency; it is a standard template and not a substitute for advice from a licensed attorney."
for key, kick, head, body in [
    ("privacy-policy", "Privacy", "Privacy Policy", privacy),
    ("terms-of-service", "Terms", "Terms of Service", terms),
    ("affiliate-disclosure", "Disclosure", "Affiliate Disclosure", disclosure)]:
    open(os.path.join(OUT, key + ".html"), "w").write(page(key, kick, head, body, note))
    print(key + ".html")
