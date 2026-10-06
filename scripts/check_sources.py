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
# new uploads from the authors whose own Hugging Face account we link to
authors = sorted({f['url'].split('/')[3] for m in cat['models'] for f in m['files'] if 'huggingface.co' in f['url']})
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
    out += [f'- https://huggingface.co/{x}' for a in new for x in new[a]]
json.dump(state, open(STATE, 'w'), indent=1, sort_keys=True)
open(f'{HERE}/report.md', 'w').write('\n'.join(out))
print(f'{len(rows)} links, {len(dead)} dead, {len(deadb)} dead backups, {sum(len(v) for v in new.values())} new files')
