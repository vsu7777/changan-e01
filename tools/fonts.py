"""Fonts for changan-e01 (gitignored, re-fetched here). SIL Open Font License 1.1.
- Noto Sans SC 500 / 700, subset to exactly the Chinese + Latin the film draws (chars.txt + cues.json),
  through the Google Fonts CSS API (&text=); run again whenever the on-screen text changes.
usage (library root): .venv/bin/python -I films/changan-e01/tools/fonts.py films/changan-e01
"""
import json, os, re, sys, urllib.parse, urllib.request
D = sys.argv[1]; F = os.path.join(D, 'fonts'); os.makedirs(F, exist_ok=True)
UA = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 Chrome/120 Safari/537.36'}
get = lambda u: urllib.request.urlopen(urllib.request.Request(u, headers=UA), timeout=60).read()
chars = set(open(os.path.join(D, 'chars.txt'), encoding='utf-8').read())
for c in json.load(open(os.path.join(D, 'cues.json'))):
    chars |= set(c['zh'])
txt = urllib.parse.quote(''.join(sorted(chars)))
for w in (500, 700):
    p = os.path.join(F, f'NotoSansSC-{w}-sub.woff2')
    if os.path.exists(p):
        continue
    css = get(f'https://fonts.googleapis.com/css2?family=Noto+Sans+SC:wght@{w}&text={txt}').decode()
    open(p, 'wb').write(get(re.search(r'url\((https://[^)]+)\)', css).group(1)))
print('fonts ok:', len(chars), 'subset characters')
