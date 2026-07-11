#!/usr/bin/env python3
"""MotoCity lead magnet PDF generator — brand style guide applied.
Black #0A0A0A pages, gold #C5A05A headers, silver #C0C0C0 body."""
import os, re, glob
from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch
from reportlab.lib.colors import HexColor
from reportlab.lib.styles import ParagraphStyle
from reportlab.platypus import (BaseDocTemplate, PageTemplate, Frame, Paragraph,
                                Spacer, Table, TableStyle, PageBreak, KeepTogether, Preformatted)
from reportlab.lib.enums import TA_CENTER

BLACK, DGRAY, MGRAY = HexColor("#0A0A0A"), HexColor("#1A1A1A"), HexColor("#333333")
GOLD, GOLD2 = HexColor("#C5A05A"), HexColor("#D4B97A")
WHITE, SILVER, RED = HexColor("#FFFFFF"), HexColor("#C0C0C0"), HexColor("#E63946")
W, H = letter
M = 0.85 * inch

DISCLOSURE = ("Disclosure: Links below are affiliate links. If you sign up or purchase through them, "
              "City Funk Entertainment may earn a commission at no extra cost to you.")

# ---------- text sanitizing (base-14 fonts = latin-1 only) ----------
EMOJI_MAP = {
    "→": "»", "←": "«", "✅": "[ok]", "✓": "[ok]", "⚠️": "(!)", "⚠": "(!)",
    "🚩": "RED FLAG ", "🔒": "", "📧": "Email: ", "🌐": "Web: ", "🎧": "", "🎤": "",
    "🎹": "", "🎚️": "", "📀": "", "📁": "", "💾": "", "🔓": "", "📜": "", "🤖": "",
    "⚡": "", "🧠": "", "😴": "", "💰": "", "🚀": "", "📥": "", "📄": "", "🗺️": "",
    "📋": "", "🛡️": "", "🎯": "", "🔥": "", "⬛": "[ ]", "•": "-", "…": "...",
    "’": "'", "‘": "'", "“": '"', "”": '"', "–": "-", "×": "x", "☐": "[ ]",
}
def sanitize(s):
    for k, v in EMOJI_MAP.items():
        s = s.replace(k, v)
    # keep latin-1 printable + em dash (winansi has it)
    out = []
    for ch in s:
        try:
            ch.encode("latin-1"); out.append(ch)
        except UnicodeEncodeError:
            out.append("" if ord(ch) > 0x2000 else "?")
    return "".join(out)

# Friendly labels for known URLs — raw links never appear in a public PDF
LINK_LABELS = [
    (r"https?://systeme\.io/\?sa=[a-z0-9]+", "Start your free Systeme.io account here"),
    (r"https?://[a-z0-9\-]+\.hop\.clickbank\.net[^\s<]*", "Unlock live government auction access here"),
    (r"https?://(www\.)?moto-city\.systeme\.io/sound-arsenal", "The Sound Arsenal - free sound packs"),
    (r"https?://(www\.)?moto-city\.systeme\.io/dj", "Book DJ SCRTCH1"),
    (r"https?://(www\.)?moto-city\.systeme\.io/cars", "MotoCity classic car valuations"),
    (r"https?://(www\.)?moto-city\.systeme\.io/health", "The Producer Energy System"),
    (r"https?://(www\.)?moto-city\.systeme\.io/ai", "HULK Systems"),
    (r"https?://(www\.)?moto-city\.systeme\.io/fix-my-funnel", "Fix My Funnel - free launch kit"),
    (r"https?://(www\.)?motocity\.autos/gov-auction-test", "MotoCity auction guide page"),
    (r"https?://(www\.)?motocity\.autos/detail", "Book a detail at MotoCity"),
    (r"https?://(www\.)?motocity\.autos[^\s<]*", "MOTOCITY.AUTOS"),
]
def linkify(s):
    def label_for(url):
        for pat, lab in LINK_LABELS:
            if re.fullmatch(pat, url): return lab
        return re.sub(r"^https?://(www\.)?", "", url).rstrip("/")  # clean fallback, no scheme
    # markdown links [text](url) keep their own text
    s = re.sub(r"\[([^\]]+)\]\((https?://[^)]+)\)",
               lambda m: f'<a href="{m.group(2)}" color="#C5A05A"><u>{m.group(1)}</u></a>', s)
    # bare URLs get a friendly label
    s = re.sub(r"(?<!\")(?<!>)(https?://[^\s<)]+)",
               lambda m: f'<a href="{m.group(1)}" color="#C5A05A"><u>{label_for(m.group(1))}</u></a>', s)
    return s

def md_inline(s):
    s = sanitize(s)
    s = s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
    s = re.sub(r"\*\*(.+?)\*\*", r'<b><font color="#FFFFFF">\1</font></b>', s)
    s = re.sub(r"\*(.+?)\*", r"<i>\1</i>", s)
    s = re.sub(r"`(.+?)`", r'<font face="Courier" color="#D4B97A">\1</font>', s)
    return linkify(s)

# ---------- styles ----------
def st(name, **kw):
    base = dict(fontName="Helvetica", fontSize=10.5, leading=15, textColor=SILVER)
    base.update(kw); return ParagraphStyle(name, **base)

S = dict(
    h1=st("h1", fontName="Helvetica-Bold", fontSize=20, leading=24, textColor=GOLD,
          spaceBefore=18, spaceAfter=8),
    h2=st("h2", fontName="Helvetica-Bold", fontSize=14, leading=18, textColor=GOLD2,
          spaceBefore=14, spaceAfter=6),
    body=st("body", spaceAfter=7),
    check=st("check", leftIndent=22, firstLineIndent=-22, spaceAfter=5),
    bullet=st("bullet", leftIndent=16, firstLineIndent=-10, spaceAfter=5),
    num=st("num", leftIndent=20, firstLineIndent=-14, spaceAfter=5),
    quote=st("quote", leftIndent=14, textColor=HexColor("#E8DFC8"),
             fontName="Helvetica-Oblique", spaceAfter=6),
    cta=st("cta", fontName="Helvetica-Bold", fontSize=11.5, leading=16,
           textColor=GOLD, spaceAfter=8),
    disc=st("disc", fontSize=8.5, leading=12, textColor=HexColor("#8a7c5c"), spaceAfter=8),
)

# ---------- page furniture ----------
def make_bg(footer_text):
    def bg(canv, doc):
        canv.saveState()
        canv.setFillColor(BLACK); canv.rect(0, 0, W, H, fill=1, stroke=0)
        if doc.page > 1:
            canv.setStrokeColor(MGRAY); canv.setLineWidth(0.5)
            canv.line(M, 0.62*inch, W-M, 0.62*inch)
            canv.setFillColor(HexColor("#666666")); canv.setFont("Helvetica", 8)
            canv.drawString(M, 0.45*inch, footer_text)
            canv.drawRightString(W-M, 0.45*inch, f"Page {doc.page - 1}")
            canv.setFillColor(GOLD); canv.setFont("Helvetica-Bold", 8)
            canv.drawCentredString(W/2, 0.45*inch, "MOTOCITY")
        canv.restoreState()
    return bg

def cover_flow(meta):
    fl = [Spacer(1, 1.5*inch)]
    fl.append(Paragraph("MOTO<font color='#FFFFFF'>CITY</font>",
        st("logo", fontName="Helvetica-Bold", fontSize=34, leading=38, textColor=GOLD, alignment=TA_CENTER)))
    fl.append(Paragraph("C I T Y &nbsp;F U N K &nbsp;E N T E R T A I N M E N T",
        st("tag", fontSize=8, leading=12, textColor=HexColor("#666666"), alignment=TA_CENTER, spaceAfter=40)))
    fl.append(Table([[""]], colWidths=[2*inch], rowHeights=[2],
        style=TableStyle([("BACKGROUND",(0,0),(-1,-1),GOLD)]), hAlign="CENTER"))
    fl.append(Spacer(1, 30))
    fl.append(Paragraph(md_inline(meta["title"]),
        st("ct", fontName="Helvetica-Bold", fontSize=27, leading=33, textColor=GOLD, alignment=TA_CENTER, spaceAfter=16)))
    fl.append(Paragraph(md_inline(meta["subtitle"]),
        st("cs", fontSize=13, leading=19, textColor=WHITE, alignment=TA_CENTER, spaceAfter=40)))
    fl.append(Paragraph(md_inline(meta["author"]),
        st("ca", fontSize=10.5, leading=15, textColor=SILVER, alignment=TA_CENTER, spaceAfter=6)))
    fl.append(Paragraph(md_inline(meta["footer"]),
        st("cf", fontName="Helvetica-Bold", fontSize=9, leading=13, textColor=GOLD2, alignment=TA_CENTER)))
    fl.append(PageBreak())
    return fl

# ---------- markdown parsing ----------
def parse(md):
    lines = md.split("\n")
    meta = dict(title="", subtitle="", author="", footer="MOTOCITY.AUTOS")
    if lines and lines[0].startswith("# "): meta["title"] = lines[0][2:].strip()
    if len(lines) > 1 and lines[1].startswith("## "): meta["subtitle"] = lines[1][3:].strip()
    for ln in lines[:20]:
        m = re.match(r"\*\*Author:\*\*\s*(.+)", ln)
        if m: meta["author"] = "By " + m.group(1).strip()
        m = re.match(r"\*\*Footer:\*\*\s*(.+)", ln)
        if m: meta["footer"] = m.group(1).strip()
    if not meta["author"]:
        for ln in lines[:8]:
            m = re.match(r"\*\*By (.+?)\*\*", ln)
            if m: meta["author"] = "By " + m.group(1).split("|")[0].strip()

    fl, i, in_cover, first_h = [], 0, False, True
    while i < len(lines):
        ln = lines[i].rstrip()
        # skip cover block (rendered separately) and canva notes
        if re.match(r"###\s+COVER", ln): in_cover = True; i += 1; continue
        if in_cover:
            if ln.startswith("---") or (ln.startswith("#") and "COVER" not in ln): in_cover = False
            else: i += 1; continue
        if "[Place MotoCity logo" in ln or ln.startswith("---"): i += 1; continue
        if i < 2 and (ln.startswith("# ") or ln.startswith("## ")): i += 1; continue
        if re.match(r"\*\*By .+\*\*$", ln) and i < 6: i += 1; continue

        if ln.startswith("## "):
            txt = ln[3:].strip()
            if "BUILT WITH SYSTEME.IO" in txt.upper():
                fl.append(Spacer(1, 6)); fl.append(Paragraph(md_inline(DISCLOSURE), S["disc"]))
            fl.append(Paragraph(md_inline(txt), S["h1"]))
        elif ln.startswith("### "):
            fl.append(Paragraph(md_inline(ln[4:].strip()), S["h2"]))
        elif ln.startswith("#### "):
            fl.append(Paragraph(md_inline(ln[5:].strip()), S["h2"]))
        elif ln.startswith("```"):
            code, i = [], i + 1
            while i < len(lines) and not lines[i].startswith("```"):
                code.append(sanitize(lines[i])); i += 1
            chunks = [code[j:j+42] for j in range(0, len(code), 42)] or [[""]]
            for ch in chunks:
                t = Table([[Preformatted("\n".join(ch),
                        st("code", fontName="Courier", fontSize=8.5, leading=11.5, textColor=GOLD2))]],
                    colWidths=[W - 2*M],
                    style=TableStyle([("BACKGROUND",(0,0),(-1,-1),DGRAY),
                                      ("BOX",(0,0),(-1,-1),0.5,MGRAY),
                                      ("LEFTPADDING",(0,0),(-1,-1),10),("RIGHTPADDING",(0,0),(-1,-1),10),
                                      ("TOPPADDING",(0,0),(-1,-1),8),("BOTTOMPADDING",(0,0),(-1,-1),8)]))
                fl.append(t); fl.append(Spacer(1, 8))
        elif ln.startswith("|") and i+1 < len(lines) and re.match(r"\|[\s\-|:]+\|", lines[i+1]):
            rows = [ [md_inline(c.strip()) for c in ln.strip("|").split("|")] ]
            i += 2
            while i < len(lines) and lines[i].startswith("|"):
                rows.append([md_inline(c.strip()) for c in lines[i].strip("|").split("|")]); i += 1
            ncol = len(rows[0]); cw = (W - 2*M) / ncol
            data = [[Paragraph(c, st("tc", fontSize=8.5, leading=12,
                     textColor=(WHITE if r==0 else SILVER),
                     fontName=("Helvetica-Bold" if r==0 else "Helvetica")))
                     for c in row[:ncol]] for r, row in enumerate(rows)]
            t = Table(data, colWidths=[cw]*ncol,
                style=TableStyle([("BACKGROUND",(0,0),(-1,0),MGRAY),
                    ("ROWBACKGROUNDS",(0,1),(-1,-1),[DGRAY, HexColor("#141414")]),
                    ("GRID",(0,0),(-1,-1),0.4,MGRAY),
                    ("VALIGN",(0,0),(-1,-1),"TOP"),
                    ("LEFTPADDING",(0,0),(-1,-1),6),("RIGHTPADDING",(0,0),(-1,-1),6),
                    ("TOPPADDING",(0,0),(-1,-1),5),("BOTTOMPADDING",(0,0),(-1,-1),5)]))
            fl.append(t); fl.append(Spacer(1, 10)); continue
        elif re.match(r"- \[ \]", ln):
            fl.append(Paragraph('<font color="#C5A05A"><b>[&nbsp;&nbsp;]</b></font> ' + md_inline(ln[5:].strip()), S["check"]))
        elif ln.startswith("- ") or ln.startswith("* "):
            fl.append(Paragraph('<font color="#C5A05A">-</font> ' + md_inline(ln[2:].strip()), S["bullet"]))
        elif re.match(r"\d+\. ", ln):
            n, rest = ln.split(". ", 1)
            fl.append(Paragraph(f'<font color="#C5A05A"><b>{n}.</b></font> ' + md_inline(rest.strip()), S["num"]))
        elif ln.startswith("> "):
            fl.append(Paragraph(md_inline(ln[2:].strip()), S["quote"]))
        elif ln.startswith(">"):
            fl.append(Spacer(1, 3))
        elif re.match(r"\*\*»|\*\*→", sanitize(ln)) or ln.startswith("**→"):
            fl.append(Paragraph(md_inline(ln.strip("*").strip()), S["cta"]))
        elif ln.strip():
            fl.append(Paragraph(md_inline(ln.strip()), S["body"]))
        i += 1
    return meta, fl

def fix_year(md): return md.replace("© 2025", "© 2026").replace("(c) 2025", "(c) 2026")

def build(src, dst):
    md = fix_year(open(src, encoding="utf-8").read())
    meta, content = parse(md)
    doc = BaseDocTemplate(dst, pagesize=letter,
        leftMargin=M, rightMargin=M, topMargin=0.8*inch, bottomMargin=0.9*inch,
        title=sanitize(meta["title"]), author="City Funk Entertainment")
    frame = Frame(M, 0.9*inch, W-2*M, H-1.7*inch, id="f")
    doc.addPageTemplates([PageTemplate(id="p", frames=[frame], onPage=make_bg(sanitize(meta["footer"])))])
    doc.build(cover_flow(meta) + content)
    print(os.path.basename(dst))

up = "/sessions/gifted-tender-fermi/mnt/uploads"
out = "/sessions/gifted-tender-fermi/mnt/outputs/lead-magnets"
os.makedirs(out, exist_ok=True)
for f in sorted(glob.glob(up + "/0*.md")):
    name = os.path.splitext(os.path.basename(f))[0] + ".pdf"
    build(f, os.path.join(out, name))
