"""Check, without downloading the weights, that the Colab code can load a model: build it on the 'meta'
device (no memory) and compare parameter names and shapes with the checkpoint's, read through HTTP range
requests (a torch .ckpt is a zip). This is exactly what load_state_dict requires.

Run inside an environment with the notebook's requirements, with the code repo mounted at /q:
    python validate_models.py todo.json results.json   # todo = {name: [model_type, config_url, checkpoint_url]}
"""
import sys, io, json, zipfile, pickle, collections, re, traceback, os
import requests, yaml, torch
sys.path.insert(0, '/q'); os.chdir('/q')
from utils import get_model_from_config
from urllib.parse import quote
S = requests.Session()


class HTTPFile(io.RawIOBase):
    def __init__(self, url):
        self.url = url; self.pos = 0; self.cache = {}
        r = S.get(url, headers={'Range': 'bytes=0-0'}, timeout=60, allow_redirects=True); r.raise_for_status()
        self.size = int(r.headers['Content-Range'].split('/')[1]); self.url = r.url
    def seekable(self): return True
    def readable(self): return True
    def tell(self): return self.pos
    def seek(self, off, whence=0):
        self.pos = off if whence == 0 else self.pos + off if whence == 1 else self.size + off
        return self.pos
    def read(self, n=-1):
        if n < 0: n = self.size - self.pos
        n = min(n, self.size - self.pos)
        if n <= 0: return b''
        B = 1 << 19; out = b''; a = self.pos
        while len(out) < n:
            blk = (a + len(out)) // B
            if blk not in self.cache:
                r = S.get(self.url, headers={'Range': f'bytes={blk*B}-{min((blk+1)*B, self.size)-1}'}, timeout=120); r.raise_for_status()
                self.cache[blk] = r.content
            o = (a + len(out)) - blk * B
            out += self.cache[blk][o:o + n - len(out)]
        self.pos += n
        return out
    def readinto(self, b):
        d = self.read(len(b)); b[:len(d)] = d; return len(d)


class Stub:
    def __init__(self, *a, **k): pass
    def __call__(self, *a, **k): return None
    def __setstate__(self, s): pass


class U(pickle.Unpickler):
    def find_class(self, mod, name):
        if mod == 'torch._utils' and name in ('_rebuild_tensor_v2', '_rebuild_tensor'):
            return lambda storage, offset, size, *a, **k: ('T', tuple(size))
        if mod == 'torch._utils' and name == '_rebuild_parameter':
            return lambda data, *a, **k: data
        if mod == 'collections' and name == 'OrderedDict': return collections.OrderedDict
        if mod == 'builtins': return super().find_class(mod, name)
        return Stub
    def persistent_load(self, pid): return None


def ckpt_shapes(url):
    f = HTTPFile(quote(url, safe=':/%'))
    z = zipfile.ZipFile(io.BufferedReader(f, 1 << 16))
    pk = [n for n in z.namelist() if n.endswith('data.pkl')][0]
    d = U(io.BytesIO(z.read(pk))).load()
    wrap = ''
    for k in ('state_dict', 'state', 'model', 'model_state_dict'):
        if isinstance(d, dict) and k in d and isinstance(d[k], dict) and not (isinstance(d[k], tuple)):
            if not any(isinstance(v, tuple) and v and v[0] == 'T' for v in d.values()): d = d[k]; wrap = k
    return {k: v[1] for k, v in d.items() if isinstance(v, tuple) and v and v[0] == 'T'}, wrap, f.size


def check(mt, cfg_url, ck_url):
    r = S.get(quote(cfg_url, safe=':/%'), timeout=60); r.raise_for_status()
    open('/tmp/c.yaml', 'wb').write(r.content)
    try:
        with torch.device('meta'):
            model, cfg = get_model_from_config(mt, '/tmp/c.yaml')
    except Exception as e:
        if 'meta tensor' in repr(e): return {'ok': None, 'why': 'no verificable sin memoria (arquitectura no admite meta)'}
        return {'ok': False, 'why': 'config/arquitectura: ' + (repr(e)[:260])}
    want = {k: tuple(v.shape) for k, v in model.state_dict().items()}
    try:
        have, wrap, size = ckpt_shapes(ck_url)
    except Exception as e:
        return {'ok': None, 'why': 'no se pudo leer el checkpoint: ' + repr(e)[:200]}
    if wrap and mt not in ('htdemucs', 'apollo'):
        return {'ok': False, 'why': f'pesos envueltos en "{wrap}" (el código no lo desenvuelve)', 'bytes': size}
    miss = [k for k in want if k not in have]; extra = [k for k in have if k not in want]
    diff = [k for k in want if k in have and want[k] != have[k]]
    tr = cfg.get('training', {}) if hasattr(cfg, 'get') else {}
    info = {'bytes': size, 'instruments': list(tr.get('instruments') or []), 'target': tr.get('target_instrument'),
            'chunk_size': (cfg.get('audio') or {}).get('chunk_size'), 'overlap': (cfg.get('inference') or {}).get('num_overlap')}
    if miss or extra or diff:
        return {'ok': False, 'why': f'faltan {len(miss)} claves, sobran {len(extra)}, forma distinta {len(diff)}; ej: {(miss or extra or diff)[:2]}', **info}
    return {'ok': True, 'keys': len(want), **info}


if __name__ == '__main__':
    todo = json.load(open(sys.argv[1])); out = json.load(open(sys.argv[2])) if os.path.exists(sys.argv[2]) else {}
    for name, (mt, cfg, ck) in todo.items():
        if name in out: continue
        if mt in ('bandit', 'bandit_v2', 'segm_models', 'swin_upernet', 'apollo', 'demucs'):
            out[name] = {'ok': None, 'why': 'arquitectura fuera del comprobador'}; continue
        out[name] = {'ok': None, 'why': 'el comprobador murió en este modelo'}; json.dump(out, open(sys.argv[2], 'w'), indent=1)
        try: out[name] = check(mt, cfg, ck)
        except Exception as e: out[name] = {'ok': None, 'why': 'error: ' + repr(e)[:240]}
        print(('OK ' if out[name]['ok'] else 'NO ' if out[name]['ok'] is False else '?? '), name[:70], '|', out[name].get('why', ''), flush=True)
        json.dump(out, open(sys.argv[2], 'w'), indent=1)
