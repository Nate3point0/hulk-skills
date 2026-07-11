#!/usr/bin/env python3
"""md2pack: convert a prompt-pack markdown file into branded HTML, PDF, and TXT.
Usage: python3 md2pack.py <input.md> <output_basename> [accent_hex]
Handles a controlled markdown subset: YAML frontmatter (title/subtitle/author/date),
# / ## / ### headers, fenced code blocks, pipe tables, **bold**, - / 1. lists, --- rules.
"""
import sys, os, re, html, subprocess

def parse_frontmatter(text):
    meta = {}
    if text.startswith('---'):
        end = text.find('\n---', 3)
        if end != -1:
            block = text[3:end].strip()
            for line in block.splitlines():
                if ':' in line:
                    k, v = line.split(':', 1)
                    meta[k.strip()] = v.strip().strip('"')
            text = text[end+4:]
    return meta, text.lstrip('\n')

def inline(s):
    s = html.escape(s)
    s = re.sub(r'`([^`]+)`', r'<code>\1</code>', s)
    s = re.sub(r'\*\*([^*]+)\*\*', r'<strong>\1</strong>', s)
    s = re.sub(r'(?<!\*)\*([^*]+)\*(?!\*)', r'<em>\1</em>', s)
    s = re.sub(r'\[([^\]]+)\]\(([^)]+)\)', r'<a href="\2">\1</a>', s)
    return s

def convert_body(md):
    lines = md.split('\n')
    out, i, n = [], 0, len(lines)
    while i < n:
        line = lines[i]
        # fenced code
        if line.startswith('```'):
            i += 1
            buf = []
            while i < n and not lines[i].startswith('```'):
                buf.append(html.escape(lines[i]))
                i += 1
            i += 1
            out.append('<pre><code>' + '\n'.join(buf) + '</code></pre>')
            continue
        # table
        if line.strip().startswith('|') and i+1 < n and re.match(r'^\s*\|[\s:|-]+\|\s*$', lines[i+1]):
            header = [c.strip() for c in line.strip().strip('|').split('|')]
            i += 2
            rows = []
            while i < n and lines[i].strip().startswith('|'):
                rows.append([c.strip() for c in lines[i].strip().strip('|').split('|')])
                i += 1
            t = ['<table><thead><tr>'] + [f'<th>{inline(h)}</th>' for h in header] + ['</tr></thead><tbody>']
            for r in rows:
                t.append('<tr>' + ''.join(f'<td>{inline(c)}</td>' for c in r) + '</tr>')
            t.append('</tbody></table>')
            out.append(''.join(t))
            continue
        # headers
        m = re.match(r'^(#{1,4})\s+(.*)$', line)
        if m:
            lvl = len(m.group(1))
            out.append(f'<h{lvl}>{inline(m.group(2))}</h{lvl}>')
            i += 1
            continue
        # hr / page break
        if re.match(r'^---+\s*$', line):
            out.append('<hr class="pb"/>')
            i += 1
            continue
        # lists
        if re.match(r'^\s*[-*]\s+', line):
            items = []
            while i < n and re.match(r'^\s*[-*]\s+', lines[i]):
                items.append('<li>' + inline(re.sub(r'^\s*[-*]\s+', '', lines[i])) + '</li>')
                i += 1
            out.append('<ul>' + ''.join(items) + '</ul>')
            continue
        if re.match(r'^\s*\d+\.\s+', line):
            items = []
            while i < n and re.match(r'^\s*\d+\.\s+', lines[i]):
                items.append('<li>' + inline(re.sub(r'^\s*\d+\.\s+', '', lines[i])) + '</li>')
                i += 1
            out.append('<ol>' + ''.join(items) + '</ol>')
            continue
        # blank
        if line.strip() == '':
            i += 1
            continue
        # paragraph
        out.append('<p>' + inline(line) + '</p>')
        i += 1
    return '\n'.join(out)

CSS = """
@page {{ size: A4; margin: 2cm 1.5cm; }}
@page :first {{ margin: 0; }}
body {{ font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif;
  line-height: 1.5; color: #333; font-size: 10.5pt; max-width: 100%; }}
.cover {{ height: 100vh; background: linear-gradient(135deg, #1a1a2e 0%, #16213e 100%);
  color: #fff; display: flex; flex-direction: column; justify-content: center; align-items: center;
  text-align: center; padding: 3cm; page-break-after: always; }}
.cover h1 {{ font-size: 3em; border: none; color: #fff; margin: 0.2em 0; }}
.cover .sub {{ font-size: 1.3em; color: {accent}; max-width: 80%; }}
.cover .author {{ margin-top: 2em; font-size: 1em; color: #cfd3dc; letter-spacing: 1px; }}
h1 {{ color: #1a1a1a; border-bottom: 3px solid {accent}; padding-bottom: 0.3em; margin-top: 1.2em; font-size: 1.6em; page-break-after: avoid; }}
h2 {{ color: #2c2c2c; border-left: 4px solid {accent}; padding-left: 0.5em; margin-top: 1em; font-size: 1.25em; page-break-after: avoid; }}
h3 {{ color: #3d3d3d; margin-top: 0.8em; font-size: 1.05em; page-break-after: avoid; }}
pre {{ background: #f8f9fa; padding: 0.8em; border-radius: 4px; border-left: 3px solid {accent};
  font-size: 0.8em; line-height: 1.35; white-space: pre-wrap; word-wrap: break-word; page-break-inside: avoid; margin: 0.8em 0; }}
code {{ font-family: 'Consolas','Monaco','Courier New',monospace; background: #f0f0f0; padding: 0.15em 0.3em; border-radius: 3px; font-size: 0.9em; }}
pre code {{ background: none; padding: 0; }}
table {{ border-collapse: collapse; width: 100%; margin: 0.8em 0; font-size: 0.95em; page-break-inside: avoid; }}
th, td {{ border: 1px solid #ddd; padding: 0.4em 0.5em; text-align: left; }}
th {{ background: {accent}; color: white; }}
hr.pb {{ border: none; border-top: 1px solid #eee; margin: 1.2em 0; }}
a {{ color: {accent}; }}
"""

def main():
    inp, base = sys.argv[1], sys.argv[2]
    accent = sys.argv[3] if len(sys.argv) > 3 else '#ff6b35'
    raw = open(inp, encoding='utf-8').read()
    meta, body = parse_frontmatter(raw)
    cover = ''
    if meta.get('title'):
        cover = (f'<div class="cover"><h1>{html.escape(meta["title"])}</h1>'
                 f'<div class="sub">{html.escape(meta.get("subtitle",""))}</div>'
                 f'<div class="author">{html.escape(meta.get("author",""))} &nbsp;|&nbsp; {html.escape(meta.get("date",""))}</div></div>')
    doc = (f'<!DOCTYPE html><html><head><meta charset="UTF-8"><style>{CSS.format(accent=accent)}</style></head>'
           f'<body>{cover}{convert_body(body)}</body></html>')
    html_path = base + '.html'
    open(html_path, 'w', encoding='utf-8').write(doc)
    # plain text
    txt = re.sub(r'^---.*?---\n', '', raw, flags=re.S)
    txt = re.sub(r'```', '', txt)
    open(base + '.txt', 'w', encoding='utf-8').write(txt)
    # pdf via chrome headless
    chrome = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
    pdf_path = base + '_Gumroad.pdf'
    r = subprocess.run([chrome, '--headless', '--disable-gpu', '--no-pdf-header-footer',
        f'--print-to-pdf={pdf_path}', 'file://' + os.path.abspath(html_path)],
        capture_output=True, text=True, timeout=120)
    ok = os.path.exists(pdf_path)
    print(f"HTML: {html_path}\nTXT: {base}.txt\nPDF: {pdf_path} ({'OK '+str(os.path.getsize(pdf_path))+'b' if ok else 'FAILED'})")
    if not ok:
        print(r.stderr[-500:])

if __name__ == '__main__':
    main()
