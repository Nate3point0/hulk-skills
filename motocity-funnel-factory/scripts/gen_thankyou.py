#!/usr/bin/env python3
# MotoCity thank-you page generator — same skeleton/accents as gen_pages.py
from gen_pages import (CSS, HEADER, CAL, DISCLOSURE, footer, bullets, steps,
                       h2, body, highlight, hero_card, cta_btn, proof, PAGES, render)

def download_slot(magnet):
    return ('<!-- NATIVE SLOT: delete this dashed box and place your Systeme.io '
            'Button element (linked to the uploaded PDF file) here -->'
            f'<div class="mc-form-card"><div class="mc-form-title">📥 Your Download</div>'
            f'<div class="mc-form-sub">{magnet} — also sent to your inbox.</div>'
            f'<div class="mc-form-slot">⬇ NATIVE SYSTEME.IO DOWNLOAD BUTTON HERE ⬇<br>(link the button to your uploaded PDF)</div>'
            f'<div class="mc-trust"><span class="lk">✉</span><span>Can\'t find the email? Check spam/promotions and whitelist admin@motocity.autos.</span></div></div>')

def ty(key, headline, sub, magnet, next_html, disclosure=False, note="© 2026 City Funk Entertainment."):
    base = PAGES[key]
    return dict(
        name=f"THANK-YOU PAGE for {base['name']}",
        colors=base["colors"],
        bar="✅ Success — you're in. Here's your download.",
        kicker=base["kicker"],
        headline=headline,
        subhead=sub,
        sections=[
            steps([("Check your inbox","Your download link just landed. Whitelist admin@motocity.autos so nothing gets lost."),
                   ("Grab your file below","Instant access — no waiting on email."),
                   ("Take the next step","One thing while you're here — it takes 60 seconds.")]),
            download_slot(magnet),
            next_html,
        ],
        disclosure=disclosure,
        disclaimer=note)

TY = {}

TY["ty-1-detail"] = ty("1-detail-service",
    "Your Checklist Is On Its Way",
    "The Car Owner's Weekly Maintenance Checklist is headed to your inbox right now.",
    "The Car Owner's Weekly Maintenance Checklist (PDF)",
    h2("Want It Done Professionally?") +
    body("The checklist keeps your detail alive. But if your car hasn't had a professional detail yet, that's step one.") +
    cta_btn("📅 Book My Detail Now", CAL))

TY["ty-2-health"] = ty("2-health",
    "Your Energy Checklist Is On Its Way",
    "The Producer Energy Checklist is headed to your inbox right now.",
    "The Producer Energy Checklist (PDF)",
    h2("While You're Here") +
    bullets([("🎧","Grab 110 free vintage sounds","Public domain, stem-separated, lawsuit-proof — the Sound Arsenal starter pack."),
             ("🎤","Booking 2026 dates","Open-format DJ sets for clubs, weddings, and corporate events.")]) +
    cta_btn("Get the Free 110 Sounds →", "https://moto-city.systeme.io/sound-arsenal"))

TY["ty-3-cars"] = ty("3-car-calculator",
    "Your Buyer's Guide Is On Its Way",
    "The Classic Car Buyer's Guide is headed to your inbox right now.",
    "The Classic Car Buyer's Guide (PDF)",
    h2("Before You Bid On Anything") +
    body("Government auctions are where the real deals are — seized and surplus vehicles at 30–70% off retail. Get the bidding guide that pairs with this one.") +
    cta_btn("Get the Auction Bidding Guide →", "https://www.motocity.autos/gov-auction-test"))

TY["ty-4-sound-arsenal"] = ty("4-sound-arsenal",
    "Your 110 Free Sounds Are On the Way",
    "The Vintage Vault Starter Pack is headed to your inbox right now.",
    "Vintage Vault Starter Pack (110 sounds + Beat Maker's Quick-Start Guide PDF)",
    highlight('🔥 <strong>One-time offer:</strong> Add the Vintage Vault Expansion — +200 bonus one-shots and 5 extra phrases — for just <strong>$7</strong>. This offer lives on this page only.') +
    cta_btn("Add the $7 Expansion →", "#") +  # UPDATE-ME: link to Systeme.io store product / order page
    proof('"I took a 1923 blues vocal, stem-separated it, pitched it down, and threw 808s under it. TikTok hit 2M views." — Marcus T., Atlanta Producer'))

TY["ty-5-gov-auction"] = ty("5-gov-auction",
    "Your Bidding Guide Is On Its Way",
    "The Government Auction Bidding Guide is headed to your inbox right now.",
    "The Government Auction Bidding Guide (PDF)",
    h2("Ready to See Live Auctions?") +
    body("The guide teaches you how to bid. This is where the actual auctions are — seized and surplus vehicles, updated constantly.") +
    cta_btn("Unlock Live Auction Access →", "https://9494861k-dykpidpy5n5mcyvcc.hop.clickbank.net") +  # UPDATE-ME: swap for cloaked motocity.autos/go/auctions
    body("Membership is optional — the free guide works on public auctions too."),
    disclosure=True,
    note="© 2026 City Funk Entertainment. Independent resource — not affiliated with any government agency.")

TY["ty-6-dj"] = ty("6-dj",
    "Got It — Talk Soon",
    "Your entertainment checklist is headed to your inbox, and your availability request is in.",
    "The Event Host's Entertainment Checklist (PDF)",
    h2("Want to Skip the Back-and-Forth?") +
    body("Grab a slot directly on the live calendar and your date is provisionally held while we confirm details.") +
    cta_btn("📅 Book Directly on the Live Calendar", CAL))

TY["ty-7-ai"] = ty("7-ai-hulk",
    "Your Setup Checklist Is On Its Way",
    "The Hulk Proxy Setup Checklist is headed to your inbox right now.",
    "The Hulk Proxy Setup Checklist (PDF)",
    h2("While Your Proxy Installs") +
    bullets([("🗺️","Get the AI Business Launch Kit","Blueprint + 50 prompts + email templates — how this whole operation runs."),
             ("▶","Watch the builds","New setups and walk-throughs on the channel.")]) +
    cta_btn("Get the Free Launch Kit →", "https://moto-city.systeme.io/fix-my-funnel"))

TY["ty-8-fix-my-funnel"] = ty("8-fix-my-funnel",
    "Your Launch Kit Is On Its Way",
    "The AI Business Launch Kit is headed to your inbox right now.",
    "The AI Business Launch Kit (Blueprint + 50 prompts + email templates)",
    h2("Don't Just Read It — Build It") +
    body("Everything in the kit assumes one tool: Systeme.io's free plan. Open your account now (free forever, no card) so you can follow along step-by-step.") +
    cta_btn("Start Your Free Systeme.io Account →", "https://systeme.io/?sa=sa0180716782ce4535d7f0b3ef221c7f646590fe91") +
    proof('"I built 9 income-generating pages without paying for ClickFunnels or Kartra. Systeme.io is the backbone of my entire operation." — NateFunkadelic, Founder, City Funk Entertainment'),
    disclosure=True,
    note="© 2026 City Funk Entertainment. Systeme.io is a trademark of Systeme.io Inc.")

import os
outdir = "/sessions/gifted-tender-fermi/mnt/outputs"
for key, p in TY.items():
    with open(os.path.join(outdir, f"{key}.html"), "w") as f:
        f.write(render(key, p))
    print(key)
