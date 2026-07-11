#!/usr/bin/env python3
# MotoCity / City Funk brand page generator — 8 funnels, one skeleton, per-page accent.
import os

CSS = """
  .mc-wrap, .mc-wrap * { margin:0; padding:0; box-sizing:border-box; }
  .mc-wrap {
    font-family:'Segoe UI', system-ui, -apple-system, sans-serif;
    background:linear-gradient(160deg,{bg1} 0%,{bg2} 60%,{bg3} 100%);
    color:#f2f1ed; line-height:1.6;
  }
  .mc-bar {
    background:linear-gradient(90deg,{accDark},{accLight});
    color:#0c0c0c; text-align:center; padding:10px 14px;
    font-size:.85rem; font-weight:700; letter-spacing:.02em;
    position:sticky; top:0; z-index:100;
  }
  .mc-container { max-width:600px; margin:0 auto; padding:40px 20px 32px; }
  .mc-kicker {
    text-align:center; font-size:.78rem; font-weight:700;
    letter-spacing:.22em; text-transform:uppercase; color:{accLight};
    margin-bottom:10px;
  }
  .mc-headline {
    font-size:2.25rem; font-weight:800; text-align:center; line-height:1.12;
    margin-bottom:12px;
    background:linear-gradient(90deg,{accLight},{accDark},{accLight});
    -webkit-background-clip:text; -webkit-text-fill-color:transparent;
    background-clip:text;
  }
  .mc-subhead { text-align:center; font-size:1.05rem; color:rgba(255,255,255,.72); margin-bottom:28px; }
  .mc-subhead strong { color:{accLight}; }
  .mc-h2 {
    font-size:1.45rem; font-weight:800; text-align:center; line-height:1.2;
    margin:8px 0 18px; color:#fff;
  }
  .mc-body { font-size:.98rem; color:rgba(255,255,255,.75); text-align:center; margin-bottom:26px; }
  .mc-hero {
    background:rgba(0,0,0,.35);
    border:1px solid {accBorder}; border-radius:16px;
    padding:24px; text-align:center; margin-bottom:28px;
  }
  .mc-hero-inner { background:rgba(0,0,0,.5); border-radius:12px; padding:34px 20px; border:2px dashed {accBorder}; }
  .mc-hero-inner .em { font-size:3rem; margin-bottom:12px; }
  .mc-hero-inner .ti { font-size:1.3rem; font-weight:800; color:#fff; }
  .mc-hero-inner .me { font-size:.9rem; color:rgba(255,255,255,.55); margin-top:8px; }
  .mc-hero p { font-size:.9rem; color:rgba(255,255,255,.55); margin-top:12px; }
  .mc-highlight {
    background:linear-gradient(135deg,{accTintA},{accTintB});
    border:1px solid {accBorder}; border-radius:12px;
    padding:18px; margin-bottom:26px; text-align:center;
  }
  .mc-highlight p { font-size:.95rem; color:rgba(255,255,255,.85); }
  .mc-highlight strong { color:{accLight}; }
  .mc-bullets { display:grid; gap:14px; margin-bottom:28px; }
  .mc-bullet {
    display:flex; align-items:flex-start; gap:14px;
    background:rgba(255,255,255,.04); border:1px solid rgba(255,255,255,.09);
    border-radius:12px; padding:16px;
  }
  .mc-bullet .ic { font-size:1.5rem; flex-shrink:0; }
  .mc-bullet .tx { font-size:.95rem; color:rgba(255,255,255,.72); }
  .mc-bullet .tx strong { color:#fff; display:block; margin-bottom:4px; }
  .mc-steps { display:grid; gap:12px; margin-bottom:28px; }
  .mc-step {
    display:flex; align-items:flex-start; gap:14px;
    background:rgba(0,0,0,.3); border:1px solid rgba(255,255,255,.08);
    border-radius:12px; padding:16px;
  }
  .mc-step .num {
    flex-shrink:0; width:34px; height:34px; border-radius:50%;
    background:linear-gradient(135deg,{accDark},{accLight}); color:#0c0c0c;
    font-weight:800; display:flex; align-items:center; justify-content:center;
  }
  .mc-step .tx { font-size:.95rem; color:rgba(255,255,255,.75); }
  .mc-step .tx strong { color:#fff; display:block; margin-bottom:2px; }
  .mc-cards { display:grid; gap:16px; margin-bottom:28px; }
  .mc-card {
    background:rgba(0,0,0,.35); border:1px solid rgba(255,255,255,.1);
    border-radius:16px; padding:24px; text-align:center; position:relative;
  }
  .mc-card.pop { border:2px solid {accLight}; }
  .mc-card .tag {
    position:absolute; top:-12px; left:50%; transform:translateX(-50%);
    background:linear-gradient(90deg,{accDark},{accLight}); color:#0c0c0c;
    font-size:.7rem; font-weight:800; text-transform:uppercase; letter-spacing:.08em;
    padding:4px 14px; border-radius:999px; white-space:nowrap;
  }
  .mc-card .nm { font-size:.85rem; font-weight:700; text-transform:uppercase; letter-spacing:.12em; color:{accLight}; margin-bottom:6px; }
  .mc-card .pr { font-size:2.2rem; font-weight:800; color:#fff; }
  .mc-card .hd { font-size:1rem; font-weight:700; color:rgba(255,255,255,.85); margin:6px 0 14px; }
  .mc-card ul { list-style:none; text-align:left; margin-bottom:18px; }
  .mc-card li { font-size:.9rem; color:rgba(255,255,255,.72); padding:6px 0; border-bottom:1px solid rgba(255,255,255,.06); }
  .mc-card li:before { content:"✓ "; color:{accLight}; font-weight:800; }
  .mc-faq { display:grid; gap:12px; margin-bottom:28px; }
  .mc-faq-item { background:rgba(0,0,0,.3); border:1px solid rgba(255,255,255,.08); border-radius:12px; padding:16px; }
  .mc-faq-item .q { font-weight:700; color:#fff; font-size:.95rem; margin-bottom:6px; }
  .mc-faq-item .q:before { content:"Q · "; color:{accLight}; }
  .mc-faq-item .a { font-size:.9rem; color:rgba(255,255,255,.65); }
  .mc-form-card {
    background:rgba(255,255,255,.05); border:1px solid {accBorder};
    border-radius:16px; padding:28px; margin-bottom:24px; text-align:center;
  }
  .mc-form-title { font-size:1.15rem; font-weight:800; margin-bottom:8px; color:#fff; }
  .mc-form-sub { font-size:.9rem; color:rgba(255,255,255,.6); margin-bottom:18px; }
  .mc-form-slot {
    border:2px dashed {accBorder}; border-radius:12px; padding:26px 16px;
    font-size:.85rem; color:rgba(255,255,255,.5); margin-bottom:16px;
  }
  .mc-cta {
    display:block; width:100%; min-height:52px; padding:17px 20px;
    font-size:1.05rem; font-weight:800; color:#0c0c0c; text-align:center;
    background:linear-gradient(90deg,{accDark},{accLight});
    border:none; border-radius:12px; cursor:pointer;
    text-transform:uppercase; letter-spacing:.04em; text-decoration:none;
    transition:transform .15s, box-shadow .15s;
  }
  .mc-cta:hover { transform:translateY(-2px); box-shadow:0 12px 40px {accGlow}; }
  .mc-trust { display:flex; align-items:center; justify-content:center; gap:8px; margin-top:14px; font-size:.8rem; color:rgba(255,255,255,.45); }
  .mc-trust .lk { color:#7bc96b; }
  .mc-proof { text-align:center; padding:20px 0; border-top:1px solid rgba(255,255,255,.07); margin-top:8px; margin-bottom:8px; }
  .mc-proof .st { color:{accLight}; font-size:1.2rem; margin-bottom:6px; }
  .mc-proof p { color:rgba(255,255,255,.6); font-size:.85rem; max-width:480px; margin:0 auto; }
  .mc-final { text-align:center; margin:8px 0 24px; }
  .mc-disclaimer {
    text-align:center; font-size:.7rem; color:rgba(255,255,255,.35); margin-top:24px;
    padding-top:16px; border-top:1px solid rgba(255,255,255,.05);
  }
  .mc-footer {
    margin-top:28px; padding:26px 16px 22px; text-align:center;
    background:rgba(0,0,0,.45); border-top:1px solid {accBorder};
  }
  .mc-footer .lg { font-size:1.1rem; font-weight:800; letter-spacing:.14em; color:#fff; }
  .mc-footer .lg span { color:{accLight}; }
  .mc-footer .tg { font-size:.72rem; letter-spacing:.2em; text-transform:uppercase; color:rgba(255,255,255,.4); margin:4px 0 14px; }
  .mc-footer .soc { display:flex; flex-wrap:wrap; justify-content:center; gap:10px 18px; margin-bottom:14px; }
  .mc-footer .soc a {
    color:rgba(255,255,255,.75); text-decoration:none; font-size:.85rem; font-weight:600;
    padding:8px 12px; min-height:40px; display:inline-flex; align-items:center; gap:6px;
    border:1px solid rgba(255,255,255,.12); border-radius:999px;
  }
  .mc-footer .soc a:hover { color:{accLight}; border-color:{accBorder}; }
  .mc-footer .lgl { font-size:.75rem; color:rgba(255,255,255,.45); margin-bottom:10px; }
  .mc-footer .lgl a { color:rgba(255,255,255,.55); text-decoration:none; margin:0 8px; }
  .mc-footer .lgl a:hover { color:{accLight}; }
  .mc-footer .disc {
    font-size:.7rem; color:rgba(255,255,255,.4); max-width:480px; margin:0 auto 12px;
    padding:10px 14px; border:1px solid rgba(255,255,255,.08); border-radius:10px;
  }
  .mc-footer .cop { font-size:.7rem; color:rgba(255,255,255,.32); }
  @media (max-width:480px) {
    .mc-headline { font-size:1.7rem; }
    .mc-container { padding:24px 16px; }
  }
"""

CAL = "https://calendar.google.com/calendar/u/0/appointments/schedules/AcZssZ2F9hzWkCI-tfPmwvcCLpdoSncYq3uxzbfsxOjX7pUnsX-H1GB-BZSX3ecdJU7lj1dQUn6OlHlb"

DISCLOSURE = ("Disclosure: Some links on this page are affiliate links. If you sign up or purchase "
              "through them, City Funk Entertainment may earn a commission at no extra cost to you.")

def footer(note, disclosure=False):
    disc = f'<div class="disc">{DISCLOSURE}</div>' if disclosure else ''
    return f'''<div class="mc-footer">
  <div class="lg">MOTO<span>CITY</span></div>
  <div class="tg">City Funk Entertainment</div>
  <div class="soc">
    <a href="https://www.youtube.com/@MotocityOfficial" target="_blank" rel="noopener">▶ YouTube</a>
    <a href="https://www.instagram.com/natecarmoney" target="_blank" rel="noopener">◉ Instagram</a>
    <a href="https://www.tiktok.com/@motor_city_funk" target="_blank" rel="noopener">♪ TikTok</a>
    <a href="https://soundcloud.com/cityfunkentertainment" target="_blank" rel="noopener">☁ SoundCloud</a>
    <a href="mailto:admin@motocity.autos">✉ admin@motocity.autos</a>
  </div>
  <div class="lgl">
    <a href="https://www.motocity.autos/privacy-policy">Privacy Policy</a>·<a href="https://www.motocity.autos/terms-of-service">Terms of Service</a>·<a href="https://www.motocity.autos/affiliate-disclosure">Affiliate Disclosure</a>
  </div>
  {disc}
  <div class="cop">{note}</div>
</div>'''

HEADER = """<!-- =====================================================
     {name} — MotoCity / City Funk branded funnel page
     =====================================================
     1. Systeme.io editor: Add Element → Raw HTML
     2. Paste this ENTIRE file into the HTML box
     3. Element padding: Desktop 0/0/0/0 · Mobile 0/0/0/0
     4. OPT-IN: every dashed "YOUR SYSTEME.IO FORM HERE" box is a
        placeholder — delete it and drop your native Systeme.io
        Form element there (or right after this block).
     5. Update any href marked UPDATE-ME.
     6. Preview at mobile width before publishing.
     ===================================================== -->
"""

def bullets(items):
    rows = "".join(
        f'<div class="mc-bullet"><div class="ic">{ic}</div><div class="tx"><strong>{s}</strong>{t}</div></div>'
        for ic, s, t in items)
    return f'<div class="mc-bullets">{rows}</div>'

def steps(items):
    rows = "".join(
        f'<div class="mc-step"><div class="num">{i+1}</div><div class="tx"><strong>{s}</strong>{t}</div></div>'
        for i, (s, t) in enumerate(items))
    return f'<div class="mc-steps">{rows}</div>'

def faq(items):
    rows = "".join(
        f'<div class="mc-faq-item"><div class="q">{q}</div><div class="a">{a}</div></div>'
        for q, a in items)
    return f'<div class="mc-faq">{rows}</div>'

def h2(t): return f'<h2 class="mc-h2">{t}</h2>'
def body(t): return f'<p class="mc-body">{t}</p>'
def highlight(t): return f'<div class="mc-highlight"><p>{t}</p></div>'

def hero_card(em, ti, me, cap):
    return (f'<div class="mc-hero"><div class="mc-hero-inner"><div class="em">{em}</div>'
            f'<div class="ti">{ti}</div><div class="me">{me}</div></div><p>{cap}</p></div>')

def form_card(title, sub, btn):
    return (f'<div class="mc-form-card"><div class="mc-form-title">{title}</div>'
            f'<div class="mc-form-sub">{sub}</div>'
            f'<!-- OPT-IN SLOT: delete this dashed box and place your native Systeme.io Form element here -->'
            f'<div class="mc-form-slot">⬇ YOUR SYSTEME.IO FORM HERE ⬇<br>(First Name + Email → button: “{btn}”)</div>'
            f'<a class="mc-cta" href="#form">{btn}</a>'
            f'<div class="mc-trust"><span class="lk">🔒</span><span>No spam. Unsubscribe anytime. Your email is never shared.</span></div></div>')

def cta_btn(label, href="#"):
    return f'<div class="mc-final"><a class="mc-cta" href="{href}">{label}</a></div>'  # UPDATE-ME hrefs

def proof(quote):
    return f'<div class="mc-proof"><div class="st">★★★★★</div><p>{quote}</p></div>'

def pricing(cards):
    out = '<div class="mc-cards">'
    for c in cards:
        pop = ' pop' if c.get("pop") else ''
        tag = f'<div class="tag">{c["tag"]}</div>' if c.get("tag") else ''
        lis = "".join(f'<li>{x}</li>' for x in c["items"])
        out += (f'<div class="mc-card{pop}">{tag}<div class="nm">{c["name"]}</div>'
                f'<div class="pr">{c["price"]}</div><div class="hd">{c["head"]}</div>'
                f'<ul>{lis}</ul><a class="mc-cta" href="{c.get("href","#")}">{c["btn"]}</a></div>')
    return out + '</div>'

PAGES = {}

# ---- 1. DETAIL ----
PAGES["1-detail-service"] = dict(
    name="DETAIL SERVICE PAGE — motocity.autos/detail",
    colors=dict(accDark="#0284c7", accLight="#7dd3fc", bg1="#050b12", bg2="#081524", bg3="#0a1f36"),
    bar="🚗 Trusted by 200+ car owners · 5-star rated · Mobile &amp; shop service available",
    kicker="MotoCity Detail",
    headline="Your Car Deserves Better Than a Drive-Through Wash",
    subhead="Professional auto detailing that protects your paint, restores your interior, and makes your car feel new again. Serving <strong>[YOUR CITY/AREA]</strong>.",
    sections=[
        cta_btn("See Packages &amp; Book", "#packages"),
        f'<div id="packages"></div>' + h2("Detailing Packages"),
        pricing([
            dict(name="The Refresh", price="$97", head="Interior Deep Clean",
                 items=["Full vacuum, shampoo, and steam clean","Dashboard, console, and door panel detail","Windows cleaned inside and out","Air freshener treatment"], btn="Book This Package", href=CAL),
            dict(name="The Protection", price="$247", head="Full Detail + Paint Sealant", pop=True, tag="Most Popular",
                 items=["Everything in The Refresh","Hand wash + clay bar treatment","One-year paint sealant","Wheel and tire dressing"], btn="Book This Package", href=CAL),
            dict(name="The Showroom", price="$497", head="Paint Correction + Ceramic Coating",
                 items=["Everything in The Protection","Single-stage paint correction","2-year ceramic coating","Full interior protection treatment"], btn="Book This Package", href=CAL),
        ]),
        h2("Why Car Owners Trust MotoCity Detail"),
        bullets([("✅","Premium products","No cheap shortcuts — professional-grade product line on every job."),
                 ("✅","Mobile service available","We come to you. Driveway, office, wherever the car sits."),
                 ("✅","Transparent pricing","No hidden fees. The price you book is the price you pay."),
                 ("✅","100% satisfaction guarantee","Not happy? We make it right.")]),
        h2("Book. Relax. Drive a New Car."),
        steps([("Pick your package online","Choose Refresh, Protection, or Showroom."),
               ("Choose mobile or shop drop-off","We come to you, or you come to us."),
               ("We detail it while you handle life","Come back to a car that feels brand new.")]),
        h2("FAQ"),
        faq([("How long does a full detail take?","Most details take 2–4 hours depending on condition and package."),
             ("Do you come to me?","Yes. Mobile detailing is available within [SERVICE RADIUS]."),
             ("What payment do you accept?","Cash, card, and Venmo. Payment is due when service is complete.")]),
        h2("Ready to Love Your Car Again?"),
        body("Spots fill up fast. Book your detail today."),
        cta_btn("Book My Detail Now", CAL),
    ],
    disclaimer="© 2026 City Funk Entertainment · MotoCity Detail. All packages subject to vehicle condition assessment.")

# ---- 2. HEALTH ----
PAGES["2-health"] = dict(
    name="HEALTH PAGE — moto-city.systeme.io/health",
    colors=dict(accDark="#0d9488", accLight="#5eead4", bg1="#04100e", bg2="#07201b", bg3="#0a2c25"),
    bar="⚡ Free download: The Producer Energy Checklist — 10 habits, 10 minutes a day",
    kicker="MotoCity Health",
    headline="The Energy System for Producers, DJs, and Hustlers",
    subhead="Stay sharp through late-night sessions, long edits, and back-to-back gigs — <strong>without burning out</strong>.",
    sections=[
        cta_btn("Get the Free Energy Checklist", "#form"),
        h2("Your Output Is Suffering Because Your Body Can't Keep Up"),
        body("You already have the skills. The gear. The ideas. But if you're running on caffeine, 4 hours of sleep, and willpower, your best work never makes it out of the DAW.<br><br>The producers and entrepreneurs who win long-term treat their body like part of their stack."),
        h2("A Simple Routine That Keeps You in the Zone"),
        bullets([("⚡","Morning protocol","Wake up clear instead of groggy."),
                 ("🧠","Focus nutrients that actually work","No fake supplements."),
                 ("🎧","Session recovery","So late nights don't wreck the next day."),
                 ("😴","Sleep setup","Deeper rest in less time.")]),
        '<div id="form"></div>' + form_card("Free Download: The Producer Energy Checklist",
                  "10 habits that keep you creative, consistent, and sharp. Takes 10 minutes a day.",
                  "Send Me the Checklist"),
        h2("Your Next Hit Deserves a Better Engine"),
        body("Start with the free checklist. Upgrade to the full protocol when you're ready."),
        cta_btn("Get the Free Checklist", "#form"),
    ],
    disclaimer="© 2026 City Funk Entertainment. Not medical advice — consult a professional before changing your health routine.")

# ---- 3. CARS ----
PAGES["3-car-calculator"] = dict(
    name="CAR CALCULATOR PAGE — moto-city.systeme.io/cars",
    colors=dict(accDark="#c98a12", accLight="#f0c96b", bg1="#0d0a07", bg2="#1a1208", bg3="#2a1c0a"),
    bar="🏁 Free classic car valuation — real auction data, results in seconds",
    kicker="MotoCity Cars",
    headline="Know What Your Classic Car Is Actually Worth",
    subhead="Search year, make, and model. Get the current market value, price history, and future projection — <strong>free</strong>.",
    sections=[
        cta_btn("Value My Car Free", "#form"),
        h2("Three Steps. Real Data. Zero Guesswork."),
        steps([("Search Your Car","Enter the year, make, and model of your classic or collectible."),
               ("Get Your Valuation","See current market value plus historical appreciation trends."),
               ("Track Your Collection","Save cars to your watchlist and monitor value changes over time.")]),
        h2("What You Get"),
        bullets([("✅","Real auction sale data","From verified sources — not inflated listings."),
                 ("✅","Historical price charts","Year-over-year appreciation at a glance."),
                 ("✅","Future value projections","Based on real market trends."),
                 ("✅","Personal watchlist","Track your whole collection in one place."),
                 ("✅","Price alerts","Know the moment values shift.")]),
        h2("Built on Real Transactions, Not Hype"),
        body("We pull from actual auction results, dealer sales, and private transactions — not inflated listings. Every valuation shows you the data behind the number."),
        h2("FAQ"),
        faq([("Is this really free?","Yes. Search and track one car free forever. Upgrade for unlimited tracking."),
             ("What years and models are covered?","Thousands of classic and collectible vehicles from all major eras."),
             ("Where does the data come from?","Verified auction houses, dealer sales, and private transaction records."),
             ("How often is the data updated?","Weekly updates keep valuations current with the market.")]),
        '<div id="form"></div>' + form_card("Find Out What Your Classic Car Is Worth Today",
                  "No credit card required. Results in seconds.","Get My Free Valuation"),
    ],
    disclaimer="© 2026 City Funk Entertainment · MotoCity Cars. Valuations are estimates based on market data, not appraisals.")

# ---- 4. SOUND ARSENAL ----
PAGES["4-sound-arsenal"] = dict(
    name="SOUND PACK PAGE — moto-city.systeme.io/sound-arsenal",
    colors=dict(accDark="#7c3aed", accLight="#c4b5fd", bg1="#0b0714", bg2="#140c24", bg3="#1c1030"),
    bar="🎛️ 46,673 sounds · 100% public domain · Stem-separated · MIDI-extracted",
    kicker="Sound Arsenal · Public Domain Vault",
    headline="Sample History No One Can Sue You For",
    subhead="46,673 sounds recorded <strong>1901–1925</strong>. Stem-separated with AI. MIDI-extracted. Free to flip, free to sell, free to chart.",
    sections=[
        hero_card("📀","The Vintage Vault Starter Pack","100 one-shots + 10 full phrases • Every DAW • Instant download • Free",
                  "Sounds no producer has touched in 100 years — ready for your DAW."),
        cta_btn("Get My Free 110 Sounds", "#form"),
        h2("Why These Sound Packs Win"),
        bullets([("🎚️","Stem-separated (Demucs 4.0)","Drag an isolated 1923 bass line straight into your trap beat."),
                 ("🎹","MIDI extracted","Load 1921 jazz melodies into Serum or Omnisphere."),
                 ("📜","Legal documentation","LICENSE.txt in every download — show your distributor, your lawyer."),
                 ("🔓","Zero subscription","Pay once, own forever. No credits. No expiration.")]),
        highlight('⬛ <strong>ORDER BUMP (add on your free checkout):</strong> YES — Add the Vintage Vault Expansion (+200 bonus one-shots and 5 extra phrases) for just $7.'),
        proof('"I took a 1923 blues vocal, stem-separated it, pitched it down, and threw 808s under it. TikTok hit 2M views." — Marcus T., Atlanta Producer'),
        body("Every sound includes a public-domain license document you can show your distributor."),
        '<div id="form"></div>' + form_card("Download Free Starter Pack",
                  "110 sounds. Instant download. No credit card.","Get My Free 110 Sounds"),
    ],
    disclaimer="© 2026 City Funk Entertainment. All recordings verified public domain (published 1901–1925, USA).")

# ---- 5. GOV AUCTION ----
PAGES["5-gov-auction"] = dict(
    name="GOV AUCTION AFFILIATE PAGE — motocity.autos/gov-auction-test",
    colors=dict(accDark="#b91c1c", accLight="#fca5a5", bg1="#120607", bg2="#1f0a0c", bg3="#2a0d0f"),
    bar="🔨 Join 100,000+ smart buyers bidding on government auctions",
    kicker="MotoCity Auctions",
    headline="Get the Free Government Auction Bidding Guide",
    subhead="Join <strong>100,000+ smart buyers</strong>. Get instant access to live auctions + the exact checklist I use to spot the best deals.",
    sections=[
        hero_card("🔨","The Government Auction Bidding Guide","Instant access • Live auctions • Free checklist",
                  "The exact checklist I use to spot the best deals before anyone else."),
        bullets([("🚗","Seized &amp; surplus vehicles","Cars, trucks, and bikes at fractions of market value."),
                 ("🧾","The pre-bid checklist","How to vet a lot in 5 minutes and skip the lemons."),
                 ("⏰","Live auction access","Know where and when the next auctions run."),
                 ("💰","Bid caps that protect you","Never overpay in the heat of the moment.")]),
        '<div id="form"></div>' + form_card("Unlock Auctions &amp; Get the Free Guide",
                  "First name + email. Instant delivery to your inbox.","Unlock Auctions &amp; Get the Free Guide"),
        cta_btn("Unlock Auctions &amp; Get the Free Guide", "#form"),
    ],
    disclosure=True,
    disclaimer="© 2026 City Funk Entertainment. Independent resource — not affiliated with any government agency.")

# ---- 6. DJ ----
PAGES["6-dj"] = dict(
    name="DJ PAGE — moto-city.systeme.io/dj",
    colors=dict(accDark="#db2777", accLight="#f9a8d4", bg1="#120610", bg2="#1f0a1a", bg3="#2a0d20"),
    bar="🎧 Now booking 2026 — clubs, private events, weddings, corporate",
    kicker="City Funk Entertainment",
    headline="Available for 2026 Bookings",
    subhead="Open-format DJ sets that keep the floor moving — <strong>any crowd, any room</strong>.",
    sections=[
        hero_card("🎧","Open-Format DJ Sets","Clubs • Private events • Weddings • Corporate","Starting at $[YOUR STARTING PRICE] for local events. Travel available."),
        h2("What You Get"),
        bullets([("🎚️","Open-format versatility","Hip-hop, house, funk, throwbacks — read the room, move the crowd."),
                 ("🔊","Pro-grade sound","Clean mixes, seamless transitions, no dead air."),
                 ("📋","Fully planned sets","Timeline, do-not-play list, and special moments handled in advance."),
                 ("✈️","Travel available","Local rates start at $[YOUR STARTING PRICE]; travel quoted per event.")]),
        h2("Lock In Your Date"),
        steps([("Check availability","Send your date, venue, and event type."),
               ("Get your quote","Flat, transparent pricing — no surprise fees."),
               ("Book the set","Deposit locks the date. Then we build your night.")]),
        '<div id="form"></div>' + form_card("Check Availability","Tell us your date and event type — we reply within 24 hours.","Check Availability"),
        cta_btn("📅 Book Directly on the Live Calendar", CAL),
    ],
    disclaimer="© 2026 City Funk Entertainment. Booking subject to availability. Deposit required to hold dates.")

# ---- 7. AI HULK ----
PAGES["7-ai-hulk"] = dict(
    name="AI HULK PAGE — moto-city.systeme.io/ai",
    colors=dict(accDark="#16a34a", accLight="#86efac", bg1="#06120a", bg2="#0a2012", bg3="#0d2a16"),
    bar="🤖 Free setup guide: cut your AI bill by 70–90% in 30 minutes",
    kicker="HULK · AI Cost Routing",
    headline="Cut Your AI Bill by 70–90% Without Losing Quality",
    subhead="HULK routes every AI request to the cheapest model that can handle it. <strong>Same output. Smaller invoice.</strong>",
    sections=[
        cta_btn("Get the Free Hulk Setup Guide", "#form"),
        h2("You're Overpaying for Simple AI Tasks"),
        body("Claude Opus for a two-word reply. GPT-4 for a regex question. Frontier models for work a smaller model can handle in half a second.<br><br>Most AI stacks route everything to one expensive model. That's like using a Ferrari to deliver pizza."),
        h2("Smart Routing. Same Results. Lower Cost."),
        bullets([("⚡","Drop-in proxy","No code changes to your existing tools."),
                 ("🧠","Automatic model selection","Routes by task complexity, every request."),
                 ("🔒","Your keys, your control","Nothing leaves your stack."),
                 ("📉","Real-time cost visibility","See cost per request as it happens.")]),
        '<div id="form"></div>' + form_card("Free Download: The Hulk Proxy Setup Checklist",
                  "The exact 30-minute setup I use to route AI requests and slash inference costs.","Send Me the Checklist"),
        h2("Stop Burning Money on Overpowered AI Calls"),
        cta_btn("Get the Free Checklist", "#form"),
    ],
    disclaimer="© 2026 City Funk Entertainment. Savings vary by workload and model mix.")

# ---- 8. FIX MY FUNNEL ----
PAGES["8-fix-my-funnel"] = dict(
    name="SYSTEME.IO AFFILIATE PAGE — moto-city.systeme.io/fix-my-funnel",
    colors=dict(accDark="#ea580c", accLight="#fdba74", bg1="#120a05", bg2="#20100a", bg3="#2a150a"),
    bar="🧰 Free: The AI Business Launch Kit — first automated income system in under 60 minutes",
    kicker="City Funk · Fix My Funnel",
    headline="Build Funnels That Sell — Without the $500/Mo Tool Stack",
    subhead="I run my sound pack store, affiliate pages, and this hub on <strong>Systeme.io</strong>. Get the free AI Business Launch Kit and see how to set up your first automated income system in under 60 minutes.",
    sections=[
        cta_btn("Get the Free AI Business Launch Kit", "#form"),
        proof('"I built 9 income-generating pages — sound packs, affiliate offers, booking pages — without paying for ClickFunnels or Kartra. Systeme.io is the backbone of my entire operation." — NateFunkadelic, Founder, City Funk Entertainment'),
        h2("What's Inside the Free Kit"),
        bullets([("📄","The AI Funnel Blueprint","The exact page flow that converts cold traffic to buyers."),
                 ("🤖","50 ChatGPT Prompts for Business","Copy, offers, emails — done in minutes."),
                 ("📧","7-Day Email Sequence Templates","Plug-and-play nurture that sells on autopilot."),
                 ("🗺️","Automation Workflow Map","Tag, trigger, and upsell without touching it twice.")]),
        '<div id="form"></div>' + form_card("Get the Free Kit",
                  "Instant download. No credit card. Built on the free Systeme.io plan.","Get the Free Kit"),
        highlight('Already convinced? <strong><a href="https://systeme.io/?sa=sa0180716782ce4535d7f0b3ef221c7f646590fe91" style="color:inherit;">Start your free Systeme.io account here →</a></strong>'),
    ],
    disclosure=True,
    disclaimer="© 2026 City Funk Entertainment. Systeme.io is a trademark of Systeme.io Inc.")

def render(key, p):
    c = p["colors"]
    def rgba(hexc, a):
        h = hexc.lstrip("#")
        r, g, b = int(h[0:2],16), int(h[2:4],16), int(h[4:6],16)
        return f"rgba({r},{g},{b},{a})"
    subs = dict(bg1=c["bg1"], bg2=c["bg2"], bg3=c["bg3"],
                accDark=c["accDark"], accLight=c["accLight"],
                accBorder=rgba(c["accLight"], .3),
                accTintA=rgba(c["accDark"], .12), accTintB=rgba(c["accLight"], .06),
                accGlow=rgba(c["accDark"], .35))
    css = CSS
    for k, v in subs.items():
        css = css.replace("{" + k + "}", v)
    html = HEADER.format(name=p["name"])
    html += f'<div class="mc-wrap" style="margin:0;padding:0;width:100%;">\n<style>{css}</style>\n'
    html += f'<div class="mc-bar">{p["bar"]}</div>\n<div class="mc-container">\n'
    html += f'<div class="mc-kicker">{p["kicker"]}</div>\n'
    html += f'<h1 class="mc-headline">{p["headline"]}</h1>\n'
    html += f'<p class="mc-subhead">{p["subhead"]}</p>\n'
    html += "\n".join(p["sections"])
    html += "\n" + footer(p["disclaimer"], p.get("disclosure", False))
    html += '\n</div>\n</div>\n<!-- END WIDGET -->\n'
    return html

outdir = "/sessions/gifted-tender-fermi/mnt/outputs"
for key, p in PAGES.items():
    path = os.path.join(outdir, f"{key}.html")
    with open(path, "w") as f:
        f.write(render(key, p))
    print(path)
