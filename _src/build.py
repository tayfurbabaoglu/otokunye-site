import re, html, sys
from pathlib import Path
SRC = Path(r'C:/Projects/carcompare/app/assets/legal/privacy_tr.md')
OUT = Path(r'C:/Projects/otokunye-site')

def inline(s):
    s = html.escape(s, quote=False)
    s = re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', s)
    s = re.sub(r'(https://[^\s<]+[^\s<.,])', r'<a href="\1">\1</a>', s)
    s = re.sub(r'([\w.+-]+@[\w-]+\.[\w.]*\w)', r'<a href="mailto:\1">\1</a>', s)
    return s

def md(text):
    out, lst = [], False
    for line in text.splitlines():
        if line.startswith('- '):
            if not lst: out.append('<ul>'); lst = True
            out.append(f'<li>{inline(line[2:])}</li>'); continue
        if lst: out.append('</ul>'); lst = False
        if line.startswith('### '): out.append(f'<h2>{inline(line[4:])}</h2>')
        elif line.startswith('> '): out.append(f'<p class="note">{inline(line[2:])}</p>')
        elif line.strip(): out.append(f'<p>{inline(line)}</p>')
    if lst: out.append('</ul>')
    return '\n'.join(out)

CSS = """:root{--bg:#fff;--fg:#1b1d22;--muted:#5d6370;--line:#e3e5ea;--accent:#2457d6}
@media (prefers-color-scheme:dark){:root{--bg:#121318;--fg:#e8e9ed;--muted:#a3a8b4;--line:#2a2d35;--accent:#8ab0ff}}
*{box-sizing:border-box}body{margin:0;background:var(--bg);color:var(--fg);font:16px/1.6 -apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,sans-serif}
main{max-width:720px;margin:0 auto;padding:32px 16px 64px}header{display:flex;gap:16px;flex-wrap:wrap;align-items:baseline;border-bottom:1px solid var(--line);padding-bottom:12px;margin-bottom:24px}
header a.brand{font-weight:700;font-size:20px;color:var(--fg);text-decoration:none}nav a{margin-right:14px}a{color:var(--accent)}
h1{font-size:28px;line-height:1.25}h2{font-size:19px;margin-top:28px}.note,footer{color:var(--muted);font-size:14px}footer{border-top:1px solid var(--line);margin-top:40px;padding-top:12px}"""

def page(name, title, body):
    doc = f"""<!doctype html>
<html lang="tr"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>{title}</title><link rel="stylesheet" href="style.css"></head>
<body><main><header><a class="brand" href="./">OtoKünye</a><nav><a href="./">Destek</a><a href="privacy.html">Gizlilik</a><a href="terms.html">Kullanım koşulları</a></nav></header>
{body}
<footer>OtoKünye · İletişim: <a href="mailto:otokunye.app@gmail.com">otokunye.app@gmail.com</a></footer></main></body></html>
"""
    (OUT / name).write_text(doc, encoding='utf-8')

(OUT / 'style.css').write_text(CSS, encoding='utf-8')
src = SRC.read_text(encoding='utf-8').split('---', 2)[2]
page('privacy.html', 'Gizlilik ve KVKK aydınlatma metni – OtoKünye',
     '<h1>Gizlilik ve KVKK aydınlatma metni</h1>\n' + md(src))
page('index.html', 'OtoKünye – Sıfır araç kıyasla', md(Path(sys.argv[1]).read_text(encoding='utf-8')).replace('<h2>', '<h2>', 1).replace('<p>', '<p>', 1).join(['<h1>OtoKünye: Sıfır Araç Kıyasla</h1>\n', '']))
page('terms.html', 'Kullanım koşulları – OtoKünye', '<h1>Kullanım koşulları</h1>\n' + md(Path(sys.argv[2]).read_text(encoding='utf-8')))
print(sorted(p.name for p in OUT.iterdir()))
