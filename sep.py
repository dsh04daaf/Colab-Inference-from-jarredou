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
SAFE_CHUNK = 352800  # fallback when the GPU runs out of memory with the author's chunk size
MAX_OVERLAP = 8  # jarredou: "normally there's no point going over 8"

# requirements fix by santilli_ (from jarredou's notebook); pandas left unpinned: 2.2.2 has no Python 3.13 wheel;
# openunmix added: demucs 4.1 no longer pulls it and the HTDemucs models import it
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
openunmix
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
        'fmt': 'Formato de {}: {} · {} bits · {} Hz',
        'fmt_same_sr': '44100 (el del modelo)',
        'working': 'Separando… (la barra de abajo avanza por trozos; con calidad máxima o TTA tarda varios minutos por canción)',
        'oom': '⚠️ La GPU se quedó sin memoria con los ajustes del autor. Reintentando con chunk_size={} y overlap menor…',
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
        'fmt': 'Format of {}: {} · {} bit · {} Hz',
        'fmt_same_sr': "44100 (the model's)",
        'working': 'Separating… (the bar below moves chunk by chunk; maximum quality or TTA takes several minutes per song)',
        'oom': "⚠️ The GPU ran out of memory with the author's settings. Retrying with chunk_size={} and a lower overlap…",
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


def _stream(cmd, cwd=None):
    """Run a command showing its output live (Colab does not display a child process's output by itself)."""
    import time
    p = subprocess.Popen(cmd, cwd=cwd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, bufsize=0,
                         env={**os.environ, 'PYTHONUNBUFFERED': '1'})
    buf, last, pending, tail = b'', 0.0, None, b''
    while True:
        chunk = os.read(p.stdout.fileno(), 4096)
        if not chunk:
            break
        buf += chunk
        tail = (tail + chunk)[-20000:]
        while True:
            i = min([x for x in (buf.find(b'\r'), buf.find(b'\n')) if x >= 0], default=-1)
            if i < 0:
                break
            line, sep_, buf = buf[:i].decode('utf-8', 'replace'), buf[i:i + 1], buf[i + 1:]
            if sep_ == b'\n':
                if line.strip() or pending:
                    print((line if line.strip() else pending or '').ljust(100))
                pending = None
            elif line.strip():  # progress bar update
                pending = line
                if time.time() - last > 1:
                    print(line.ljust(100), end='\r')
                    last = time.time()
    if pending:
        print(pending.ljust(100))
    _stream.oom = b'out of memory' in tail.lower()
    return p.wait()


def _fetch(url, dest):
    code = _stream(['curl', '-L', '--fail', '--retry', '3', '--progress-bar', '-o', dest + '.part', url])
    return code == 0 and os.path.exists(dest + '.part')


def _slug(name):
    import re
    return re.sub(r'[^A-Za-z0-9._+-]+', '_', name).strip('_')


def _download(f, t, folder):
    from urllib.parse import quote
    os.makedirs(folder, exist_ok=True)
    dest = os.path.join(folder, f['name'])
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


def _source_format(path):
    """(container, subtype, samplerate) of an input file; lossy or unreadable inputs map to 16-bit WAV."""
    try:
        import soundfile as sf
        i = sf.info(path)
        sub = {'DOUBLE': 'FLOAT'}.get(i.subtype, i.subtype)
        if sub in ('PCM_16', 'PCM_24', 'PCM_32', 'FLOAT'):  # any lossless PCM container (WAV, WAVEX, AIFF, FLAC…)
            if i.format == 'FLAC':
                return 'flac', sub if sub in ('PCM_16', 'PCM_24') else 'PCM_24', i.samplerate
            return 'wav', sub, i.samplerate
        return 'wav', 'PCM_16', i.samplerate
    except Exception:
        return 'wav', 'PCM_16', None


def _convert(path, container, subtype, samplerate):
    """Rewrite one result file in the requested container / bit depth / sample rate."""
    import soundfile as sf
    data, sr = sf.read(path, dtype='float32', always_2d=True)
    if samplerate and samplerate != sr:
        import soxr
        data, sr = soxr.resample(data, sr, samplerate, quality='VHQ'), samplerate
    dest = os.path.splitext(path)[0] + '.' + container
    tmp = dest + '.tmp.' + container
    sf.write(tmp, data, sr, subtype=subtype)
    if dest != path:
        os.remove(path)
    os.replace(tmp, dest)
    return dest


def _match_format(input_files, folder, since, export_format, t, quiet=False):
    """Convert every file the engine just wrote in `folder` (auto = same format as its source song)."""
    fixed = None if export_format == 'auto' else (export_format.split(' ')[0], export_format.split(' ')[1], None)
    stems = sorted(((os.path.splitext(os.path.basename(f))[0], f) for f in input_files), key=lambda x: -len(x[0]))
    shown = set()
    for out in sorted(glob.glob(os.path.join(folder, '*.wav'))):
        if os.path.getmtime(out) < since:
            continue
        src = next((f for s, f in stems if os.path.basename(out).startswith(s + '_')), None)
        if not src:
            continue
        fmt = fixed or _source_format(src)
        _convert(out, *fmt)
        if src not in shown and not quiet:
            shown.add(src)
            print(t['fmt'].format(os.path.basename(src), fmt[0].upper(), fmt[1].replace('PCM_', '').replace('FLOAT', '32 float'),
                                  fmt[2] or t['fmt_same_sr']))


def _separate(m, input_folder, output_folder, export_format, quality, chunk_size, overlap, use_tta, extract, t, source_files=None):
    print(t['model'].format(m['name'], m['author']))
    folder = os.path.join(ROOT, 'ckpts', _slug(m['name']))
    paths = {f['role']: _download(f, t, folder) for f in m['files']}
    st = resolve_settings(m, quality, chunk_size, overlap)
    if st:
        _conf_edit(paths['config'], *st)
        print(t['settings'].format(st[0], st[1], use_tta))
    else:
        print(t['settings_fixed'].format(use_tta))
    os.makedirs(output_folder, exist_ok=True)
    import time
    since = time.time() - 2
    print(t['working'])
    cmd = [sys.executable, 'inference.py', '--model_type', m['model_type'], '--config_path', paths['config'],
           '--start_check_point', paths['checkpoint'], '--input_folder', input_folder, '--store_dir', output_folder]
    if extract:
        cmd.append('--extract_instrumental')
    if use_tta:
        cmd.append('--use_tta')
    code = _stream(cmd, cwd=ROOT)
    if code != 0 and _stream.oom and st and st[0] > SAFE_CHUNK:
        print(t['oom'].format(SAFE_CHUNK))
        _conf_edit(paths['config'], SAFE_CHUNK, min(st[1], 4))
        code = _stream(cmd, cwd=ROOT)
    if code != 0:
        print(t['failed'].format(code))
        raise SystemExit(1)
    if export_format != 'wav FLOAT':
        _match_format(source_files or glob.glob(os.path.join(input_folder, '*')), output_folder, since, export_format, t, quiet=bool(source_files))


def run(goal='acapella', model='auto', input_folder='/content/drive/MyDrive/input',
        output_folder='/content/drive/MyDrive/output', export_format='auto', quality='max',
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
        import time
        since = time.time() - 2
        _separate(steps[0], input_folder, output_folder, 'wav FLOAT', quality, 'auto', 'auto', use_tta, False, t)
        drums_in = '/content/_drums_in'
        shutil.rmtree(drums_in, ignore_errors=True)
        os.makedirs(drums_in)
        found = [f for f in glob.glob(os.path.join(output_folder, '*_drums.wav')) if os.path.getmtime(f) >= since]
        if not found:
            print(t['no_drums'])
            raise SystemExit(1)
        for f in found:
            shutil.copy(f, drums_in)
        print(t['step'].format(2, 2, steps[1]['name']))
        out2 = os.path.join(output_folder, 'drum_pieces')
        _separate(steps[1], drums_in, out2, export_format, quality, 'auto', 'auto', use_tta, False, t, source_files=files)
        if export_format != 'wav FLOAT':
            _match_format(files, output_folder, since, export_format, t)
        print(t['done'].format(output_folder))
        return
    m = steps[0]
    if goal == 'manual':
        extract = extract_instrumental
    else:
        extract = goal in ('acapella', 'karaoke', 'dereverb', 'denoise')
    _separate(m, input_folder, output_folder, export_format, quality, chunk_size, overlap, use_tta, extract, t)
    if (goal == 'instrumental' and m.get('target') == 'other') or goal == 'acapella':
        for f in glob.glob(os.path.join(output_folder, '*_other.*')):
            os.replace(f, '_instrumental.'.join(f.rsplit('_other.', 1)))
        if goal == 'instrumental':
            print(t['is_inst'])
    print(t['done'].format(output_folder))
