"""Colab runner for jarredou's Music-Source-Separation-Training inference notebook.

The notebook only collects the form values and calls setup() / run(); everything else
(model catalog, downloads with backup fallback, per-model settings) lives here and in models.json.
"""
import glob
import json
import os
import shutil
import subprocess
import sys
import functools

print = functools.partial(print, flush=True)

ROOT = '/content/Music-Source-Separation-Training'
HERE = os.path.dirname(os.path.abspath(__file__))
CATALOG = os.path.join(HERE, 'models.json')
MAX_OVERLAP = 8  # jarredou: "normally there's no point going over 8"

# requirements fix by santilli_ (from jarredou's notebook); pandas left unpinned: 2.2.2 has no Python 3.13 wheel
REQUIREMENTS = """mutagen==1.47.0
ml_collections==1.1.0
numpy>=1.26.0
pandas
scipy
tqdm
segmentation_models_pytorch==0.3.3
timm
audiomentations
pedalboard
omegaconf
beartype
rotary_embedding_torch==0.3.5
einops
demucs
torchmetrics==0.11.4
spafe==0.3.2
protobuf
torch_audiomentations
asteroid==0.7.0
auraloss
torchseg
"""

T = {
    'es': {
        'cloning': 'Descargando el código…',
        'installing': 'Instalando dependencias (unos minutos)…',
        'install_fail': 'La instalación FALLÓ. Últimas líneas del registro:',
        'install_ok': '✅ Instalación terminada.',
        'no_files': '❌ No hay archivos de audio en {}. Sube tus canciones a esa carpeta (es la ruta de una carpeta, no de un archivo).',
        'model': 'Modelo: {} — por {}',
        'settings': 'Ajustes usados: chunk_size={} · overlap={} · TTA={}',
        'settings_fixed': 'Ajustes usados: los del autor del modelo (este modelo no admite cambios) · TTA={}',
        'dl': 'Descargando {} ({:.0f} MB)…',
        'dl_backup': '   el enlace original falló; usando el respaldo…',
        'dl_fail': '❌ No se pudo descargar {} ni del original ni del respaldo.',
        'cached': '{} ya estaba descargado.',
        'step': '── Paso {}/{}: {}',
        'done': '✅ Listo. Resultados en: {}',
        'failed': '❌ La separación falló (código {}). Revisa el mensaje de arriba.',
        'no_drums': '❌ No se encontró la pista de batería del paso anterior.',
        'is_inst': 'El archivo terminado en "_instrumental" es el instrumental.',
    },
    'en': {
        'cloning': 'Downloading the code…',
        'installing': 'Installing dependencies (a few minutes)…',
        'install_fail': 'Installation FAILED. Last lines of the log:',
        'install_ok': '✅ Installation is done.',
        'no_files': '❌ No audio files in {}. Upload your songs to that folder (it must be a folder path, not a file path).',
        'model': 'Model: {} — by {}',
        'settings': 'Settings used: chunk_size={} · overlap={} · TTA={}',
        'settings_fixed': "Settings used: the model author's own (this model takes no overrides) · TTA={}",
        'dl': 'Downloading {} ({:.0f} MB)…',
        'dl_backup': '   original link failed; using the backup…',
        'dl_fail': '❌ Could not download {} from the original link or the backup.',
        'cached': '{} already downloaded.',
        'step': '── Step {}/{}: {}',
        'done': '✅ Done. Results in: {}',
        'failed': '❌ Separation failed (exit code {}). Check the message above.',
        'no_drums': '❌ The drums stem from the previous step was not found.',
        'is_inst': 'The file ending in "_instrumental" is the instrumental.',
    },
}
AUDIO_EXT = ('.wav', '.flac', '.mp3', '.m4a', '.aiff', '.aif', '.ogg', '.opus', '.wma')


def catalog():
    with open(CATALOG, encoding='utf-8') as f:
        return json.load(f)


def setup(lang='es'):
    t = T[lang]
    cat = catalog()
    if not os.path.isdir(ROOT):
        print(t['cloning'], flush=True)
        subprocess.run(['git', 'clone', '-q', '-b', cat['code']['branch'], cat['code']['repo'], ROOT], check=True)
    os.makedirs(os.path.join(ROOT, 'ckpts'), exist_ok=True)
    req = os.path.join(ROOT, 'requirements.txt')
    with open(req, 'w') as f:
        f.write(REQUIREMENTS)
    print(t['installing'], flush=True)
    r = subprocess.run([sys.executable, '-m', 'pip', 'install', '-r', req], capture_output=True, text=True)
    if r.returncode != 0:
        print(t['install_fail'])
        print('\n'.join((r.stdout + r.stderr).splitlines()[-40:]))
        raise SystemExit(1)
    print(t['install_ok'])


def _fetch(url, dest):
    r = subprocess.run(['curl', '-L', '--fail', '--retry', '3', '-sS', '-o', dest + '.part', url])
    return r.returncode == 0 and os.path.exists(dest + '.part')


def _download(f, t):
    from urllib.parse import quote
    dest = os.path.join(ROOT, 'ckpts', f['name'])
    want = f.get('bytes')
    if os.path.exists(dest) and (not want or os.path.getsize(dest) == want or f['role'] == 'config'):
        print(t['cached'].format(f['name']))
        return dest
    print(t['dl'].format(f['name'], (want or 0) / 1e6), flush=True)
    sources = [quote(f['url'], safe=':/%')] + ([f['backup']] if f.get('backup') else [])
    for i, url in enumerate(sources):
        if i:
            print(t['dl_backup'], flush=True)
        if _fetch(url, dest) and (not want or os.path.getsize(dest + '.part') == want):
            os.replace(dest + '.part', dest)
            return dest
        if os.path.exists(dest + '.part'):
            os.remove(dest + '.part')
    print(t['dl_fail'].format(f['name']))
    raise SystemExit(1)


def _conf_edit(config_path, chunk_size, overlap):
    """jarredou's conf_edit: write chunk_size / overlap into the model config."""
    import yaml

    class IndentDumper(yaml.Dumper):
        def increase_indent(self, flow=False, indentless=False):
            return super().increase_indent(flow, False)

    yaml.SafeLoader.add_constructor('tag:yaml.org,2002:python/tuple',
                                    lambda loader, node: tuple(loader.construct_sequence(node)))
    with open(config_path) as f:
        data = yaml.load(f, Loader=yaml.SafeLoader)
    if 'use_amp' not in data.keys():
        data['training']['use_amp'] = True
    data['audio']['chunk_size'] = chunk_size
    data['inference']['num_overlap'] = overlap
    if data['inference']['batch_size'] == 1:
        data['inference']['batch_size'] = 2
    with open(config_path, 'w') as f:
        yaml.dump(data, f, default_flow_style=False, sort_keys=False, Dumper=IndentDumper, allow_unicode=True)


def resolve_settings(m, quality='max', chunk_size='auto', overlap='auto'):
    """Per-model settings. Returns (chunk, overlap) or None when the model's config is left untouched."""
    if not m['tunable']:
        return None
    base_overlap = m.get('overlap') or 2
    chunk = m['chunk_size'] if str(chunk_size) == 'auto' else int(chunk_size)
    if str(overlap) != 'auto':
        ov = int(overlap)
    else:
        ov = max(base_overlap, MAX_OVERLAP) if quality == 'max' else base_overlap
    return chunk, ov


def _separate(m, input_folder, output_folder, export_format, quality, chunk_size, overlap, use_tta, extract, t):
    print(t['model'].format(m['name'], m['author']))
    paths = {f['role']: _download(f, t) for f in m['files']}
    st = resolve_settings(m, quality, chunk_size, overlap)
    if st:
        _conf_edit(paths['config'], *st)
        print(t['settings'].format(st[0], st[1], use_tta))
    else:
        print(t['settings_fixed'].format(use_tta))
    os.makedirs(output_folder, exist_ok=True)
    cmd = [sys.executable, 'inference.py', '--model_type', m['model_type'], '--config_path', paths['config'],
           '--start_check_point', paths['checkpoint'], '--input_folder', input_folder, '--store_dir', output_folder]
    if extract:
        cmd.append('--extract_instrumental')
    if export_format.startswith('flac'):
        cmd += ['--flac_file', '--pcm_type', export_format.split(' ')[1]]
    if use_tta:
        cmd.append('--use_tta')
    r = subprocess.run(cmd, cwd=ROOT)
    if r.returncode != 0:
        print(t['failed'].format(r.returncode))
        raise SystemExit(1)


def run(goal='acapella', model='auto', input_folder='/content/drive/MyDrive/input',
        output_folder='/content/drive/MyDrive/output', export_format='wav FLOAT', quality='max',
        chunk_size='auto', overlap='auto', use_tta=False, extract_instrumental=True, lang='es'):
    t = T[lang]
    cat = catalog()
    by = {m['name']: m for m in cat['models']}
    files = [f for f in glob.glob(os.path.join(input_folder, '*')) if f.lower().endswith(AUDIO_EXT)]
    if not files:
        print(t['no_files'].format(input_folder))
        raise SystemExit(1)
    if model != 'auto':
        steps, goal = [by[model]], 'manual'
    else:
        steps = [by[n] for n in cat['goals'][goal]]
    if goal == 'drum_pieces':
        print(t['step'].format(1, 2, steps[0]['name']))
        _separate(steps[0], input_folder, output_folder, export_format, quality, 'auto', 'auto', use_tta, False, t)
        drums_in = '/content/_drums_in'
        shutil.rmtree(drums_in, ignore_errors=True)
        os.makedirs(drums_in)
        found = [f for f in glob.glob(os.path.join(output_folder, '*_drums.*'))]
        if not found:
            print(t['no_drums'])
            raise SystemExit(1)
        for f in found:
            shutil.copy(f, drums_in)
        print(t['step'].format(2, 2, steps[1]['name']))
        out2 = os.path.join(output_folder, 'drum_pieces')
        _separate(steps[1], drums_in, out2, export_format, quality, 'auto', 'auto', use_tta, False, t)
        print(t['done'].format(output_folder))
        return
    m = steps[0]
    if goal == 'manual':
        extract = extract_instrumental
    else:
        extract = goal in ('acapella', 'karaoke', 'dereverb', 'denoise')
    _separate(m, input_folder, output_folder, export_format, quality, chunk_size, overlap, use_tta, extract, t)
    if goal == 'instrumental' and m.get('target') == 'other':
        for f in glob.glob(os.path.join(output_folder, '*_other.*')):
            os.replace(f, f.replace('_other.', '_instrumental.'))
        print(t['is_inst'])
    print(t['done'].format(output_folder))
