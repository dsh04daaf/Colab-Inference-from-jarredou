"""Genera models.json a partir del notebook original de jarredou (ya con espejos) + el manifiesto del respaldo."""
import json, re, subprocess, sys, yaml, concurrent.futures as cf
from urllib.parse import quote
yaml.SafeLoader.add_constructor('tag:yaml.org,2002:python/tuple', lambda l, n: tuple(l.construct_sequence(n)))
SRC_NB, SIZES, MANIFEST, OUT = sys.argv[1:5]
BACKUP = 'https://huggingface.co/dshdaaf/separation-models/resolve/main/'
AUTHORS = {'VOCALS-InstVocHQ': 'Anjok07, aufr33 & ZFTurbo', '6STEMS-BS-Roformer-SW': 'unknown ("shared weights")',
           'DENOISE-MelBand-Roformer-1 (by aufr33)': 'aufr33', 'DENOISE-MelBand-Roformer-2 (by aufr33)': 'aufr33'}
s = ''.join(json.load(open(SRC_NB))['cells'][3]['source'])
order = re.findall(r"'([^']+)'", re.search(r"model = '[^']*' #@param \[(.*?)\]\n", s, re.S).group(1))
sizes = json.load(open(SIZES))['sizes']
man = {v['source']: v for v in json.load(open(MANIFEST)).values()}
blocks = {}
for b in re.split(r"\n(?=(?:if|elif) model == ')", s):
    m = re.match(r"(?:if|elif) model == '([^']+)'", b)
    if m: blocks[m.group(1)] = b


def one(name):
    b = blocks[name]
    cfg = re.search(r"config_path = 'ckpts/([^']+)'", b).group(1)
    ck = re.search(r"start_check_point = 'ckpts/([^']+)'", b).group(1)
    files = []
    for u in re.findall(r"download_file\('([^']+)'\)", b):
        fn = quote(u, safe=':/').rsplit('/', 1)[1]
        f = {'role': 'config' if fn == cfg else 'checkpoint' if fn == ck else 'extra', 'name': fn, 'url': u, 'bytes': sizes[u]}
        if u in man: f['backup'] = BACKUP + quote(man[u]['path']); f['sha256'] = man[u]['sha256']
        files.append(f)
    cu = [f['url'] for f in files if f['role'] == 'config'][0]
    d = yaml.load(subprocess.run(['curl', '-s', '-L', '-m', '60', quote(cu, safe=':/')], capture_output=True, text=True).stdout, Loader=yaml.SafeLoader)
    a = re.search(r'\(by ([^)]+)\)', name)
    return {'name': name, 'category': name.split('-')[0], 'author': AUTHORS.get(name) or (a.group(1) if a else 'unknown'),
            'model_type': re.search(r"model_type = '([^']+)'", b).group(1), 'tunable': 'conf_edit' in b,
            'chunk_size': d.get('audio', {}).get('chunk_size'), 'overlap': d.get('inference', {}).get('num_overlap'),
            'instruments': list(d.get('training', {}).get('instruments') or []), 'target': d.get('training', {}).get('target_instrument'),
            'files': files}


with cf.ThreadPoolExecutor(8) as ex: models = list(ex.map(one, order))
GOALS = {  # recomendados: guía de deton24 (edición 2026-10-05) restringida a lo que hay en este catálogo
    'acapella': ['VOCALS-Melband-Roformer BigBeta6X (by unwa)'],
    'instrumental': ['INST-Mel-Roformer v1e+ (by unwa)'],
    'stems': ['6STEMS-BS-Roformer-SW'],
    'drum_pieces': ['6STEMS-BS-Roformer-SW', 'DRUMSEP-MDX23C_DrumSep_5stem_new (by jarredou)'],
    'karaoke': ['KARAOKE-BS-Roformer (by anvuew)'],
    'dereverb': ['DE-REVERB-MelBand-Roformer aggr./v2/19.1729 (by anvuew)'],
    'denoise': ['DENOISE-MelBand-Roformer-1 (by aufr33)'],
}
names = {m['name'] for m in models}
assert all(n in names for g in GOALS.values() for n in g)
json.dump({'version': 1, 'code': {'repo': 'https://github.com/dsh04daaf/Music-Source-Separation-Training', 'branch': 'colab-inference'},
           'goals': GOALS, 'models': models}, open(OUT, 'w'), indent=1, ensure_ascii=False)
print(len(models), 'modelos;', sum(1 for m in models for f in m['files'] if 'backup' in f), 'archivos con respaldo')
