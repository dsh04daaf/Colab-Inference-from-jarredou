"""Weekly monitor: (1) every model link still answers, (2) the active authors' accounts have nothing new.
Writes report.md (empty when there is nothing to tell) and refreshes sources_state.json."""
import json, os, subprocess, concurrent.futures as cf
from urllib.parse import quote
HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
cat = json.load(open(f'{HERE}/models.json', encoding='utf-8'))
STATE = f'{HERE}/sources_state.json'
state = json.load(open(STATE)) if os.path.exists(STATE) else {}


def alive(url):
    for _ in range(3):
        c = subprocess.run(['curl', '-s', '-L', '-o', '/dev/null', '-r', '0-0', '-m', '60', '-w', '%{http_code}', url],
                           capture_output=True, text=True).stdout
        if c in ('200', '206'): return True
    return False


rows = [(m['name'], f['name'], quote(f['url'], safe=':/%'), f.get('backup')) for m in cat['models'] for f in m['files']]
with cf.ThreadPoolExecutor(6) as ex:
    src = list(ex.map(lambda r: alive(r[2]), rows))
    bak = list(ex.map(lambda r: alive(r[3]) if r[3] else None, rows))
out = []
dead = [(r, b) for r, s, b in zip(rows, src, bak) if not s]
if dead:
    out.append('## Dead source links\n')
    out += [f'- **{r[0]}** — `{r[1]}` — {r[2]} — backup: {"OK" if b else "MISSING" if b is None else "DEAD"}' for r, b in dead]
deadb = [r for r, b in zip(rows, bak) if b is False]
if deadb:
    out.append('\n## Dead backup links\n')
    out += [f'- **{r[0]}** — `{r[1]}` — {r[3]}' for r in deadb]
# new uploads from the authors whose own Hugging Face account we link to. Mirror accounts re-upload other people's
# models by the hundred (Eddycrack864 alone ~1,700 files): they are not authors, and they made the report too long
# for a GitHub issue, which failed the job and kept the snapshot from being saved (2026-10-19 → 11-09).
MIRRORS = {'Eddycrack864', 'Politrees', 'RareSirMix', 'enerjazzer', 'xavriley', 'noblebarkrr', 'listra92', 'baicai1145',
           'TRvlvr', 'miercolesv', 'dshdaaf'}
authors = sorted({f['url'].split('/')[3] for m in cat['models'] for f in m['files'] if 'huggingface.co' in f['url']} - MIRRORS)
for a in list(state):
    if a in MIRRORS: state.pop(a)
new = {}
for a in authors:
    try:
        r = subprocess.run(['curl', '-s', '-m', '60', f'https://huggingface.co/api/models?author={a}&limit=200&full=true'],
                           capture_output=True, text=True).stdout
        cur = {x['id']: sorted(s['rfilename'] for s in x.get('siblings', []) if s['rfilename'].endswith(('.ckpt', '.th', '.pt', '.safetensors')))
               for x in json.loads(r)}
    except Exception:
        continue
    old = state.get(a)
    if old is not None:
        added = [f'{rid}/{fn}' for rid, fs in cur.items() for fn in fs if fn not in old.get(rid, [])]
        if added: new[a] = added
        if not cur and old: out.append(f'\n## Account empty or gone: {a}\n')
    state[a] = cur
if new:
    out.append('\n## New model files from tracked authors\n')
    for a, xs in new.items():
        out.append(f'**{a}** ({len(xs)})')
        out += [f'- https://huggingface.co/{x}' for x in xs[:15]]
        if len(xs) > 15: out.append(f'- … and {len(xs) - 15} more: https://huggingface.co/{a}')

# deton24's guide: the notebook's defaults and list order come from it (models.json → guide_edition)
GUIDE = 'https://docs.google.com/document/d/17fjNvJzj8ZGSer7c7OFe_CNfUKbAxEh_OBv94ZdRG5c/export?format=txt'
import re
txt = subprocess.run(['curl', '-s', '-L', '-m', '180', GUIDE], capture_output=True, text=True).stdout
lines = [l.strip() for l in txt.lstrip('\ufeff').splitlines()]
m = re.match(r'edit\.\s*(\d+)\.(\d+)\.(\d+)', lines[0] if lines else '')
if not m or len(lines) < 5000:
    out.append('\n## Guide: could not read it\n\nThe export of deton24\'s guide did not come back as expected; check it by hand.')
else:
    edition = f'20{m.group(3)}-{m.group(2)}-{m.group(1)}'
    # news = the bullets at the top ("Last updates and news"); models = a bullet followed by its metrics line
    try:
        i = next(k for k, l in enumerate(lines) if l.startswith('Last updates and news'))
        news = [l for l in lines[i + 1:i + 400] if l.startswith('- ')][:60]
    except StopIteration:
        news = []
    metric = re.compile(r'(fullness|bleedless|SDR)\W{0,3}\d{1,2}[.,]\d{1,4}', re.I)  # a real number, not a description
    entries = []
    for k, l in enumerate(lines):
        if metric.search(l) and len(l) < 200:
            head = next((lines[j] for j in range(k - 1, max(k - 4, 0), -1) if lines[j].startswith(('- ', '* ', '0) '))), '')
            if head: entries.append(head.lstrip('-*0) ')[:160] + ' → ' + l[:120])
    g = state.get('_guide')
    if g and g.get('edition') != edition:
        add_news = [n for n in news if n not in g.get('news', [])]
        add_ent = [e for e in dict.fromkeys(entries) if e not in g.get('entries', [])]
        out.append(f"\n## deton24's guide changed: {g.get('edition')} → {edition}\n")
        out.append(f"The notebook's defaults follow edition **{cat.get('guide_edition')}**. Review whether the best model of each kind changed.\n")
        if add_news:
            out.append('**New in "Last updates and news"**')
            out += [f'- {n[2:300]}' for n in add_news[:25]]
        if add_ent:
            out.append('\n**Model entries with new or changed metrics**')
            out += [f'- {e}' for e in add_ent[:40]]
            if len(add_ent) > 40: out.append(f'- … and {len(add_ent) - 40} more')
        if not add_news and not add_ent:
            out.append('Only wording changed (no new news items or metric lines).')
    state['_guide'] = {'edition': edition, 'news': news, 'entries': list(dict.fromkeys(entries))}

# a GitHub issue body takes at most 65,536 characters
rep = '\n'.join(out)
if len(rep) > 60000:
    rep = rep[:60000].rsplit('\n', 1)[0] + '\n\n… (report cut: too long)'
out = [rep] if rep else []
json.dump(state, open(STATE, 'w'), indent=1, sort_keys=True)
open(f'{HERE}/report.md', 'w').write('\n'.join(out))
print(f'{len(rows)} links, {len(dead)} dead, {len(deadb)} dead backups, {sum(len(v) for v in new.values())} new files, guide {state.get("_guide", {}).get("edition")}')
