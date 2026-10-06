"""Genera los notebooks ES/EN desde una sola plantilla + models.json."""
import json, os
HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
REPO = 'dsh04daaf/Colab-Inference-from-jarredou'
RAW = f'https://raw.githubusercontent.com/{REPO}/main/'
cat = json.load(open(f'{HERE}/models.json', encoding='utf-8'))
names = [m['name'] for m in cat['models']]
L = {
 'es': dict(file='Colab_Inference_ES.ipynb', fauto='auto (igual que el archivo original)', auto='Recomendado (según lo que elegí arriba)',
  goals=[('acapella', 'Acapella (voz) + instrumental'), ('instrumental', 'Instrumental'),
         ('stems', 'Stems: voz, batería, bajo, guitarra, piano, otros'), ('drum_pieces', 'Batería por piezas: bombo, caja, toms, hi-hat, platos'),
         ('karaoke', 'Karaoke: separar voz principal de coros'), ('dereverb', 'Quitar reverb'), ('denoise', 'Quitar ruido')],
  quality=[('max', 'Máxima (recomendada)'), ('fast', 'Rápida')],
  intro=f"""# Separación de música — Colab Inference
Saca **acapellas, instrumentales y stems** con los modelos de la comunidad, sobre el código de [ZFTurbo](https://github.com/ZFTurbo/Music-Source-Separation-Training).

Basado en el notebook original de **jarredou** & deton. Este repo lo conserva, lo mantiene funcionando y respalda los modelos que ya no tienen cuenta de origen. Créditos de cada modelo en el [README](https://github.com/{REPO}#créditos).

**Cómo se usa**
1. En tu Google Drive crea las carpetas `input` y `output`, y sube tus canciones a `input`.
2. Menú *Entorno de ejecución → Cambiar tipo de entorno → GPU T4*.
3. Ejecuta **1. Preparar** (una vez por sesión).
4. En **2. Separar** elige qué quieres y ejecútala. No hace falta tocar nada más.

[English version](https://colab.research.google.com/github/{REPO}/blob/main/Colab_Inference_EN.ipynb)""",
  t1='# 1. Preparar', drive='conectar_google_drive',
  t2='# 2. Separar', want='que_quiero', inp='carpeta_entrada', out='carpeta_salida', fmt='formato',
  adv='### Avanzado (opcional — cada modelo ya trae sus propios ajustes, no hace falta cambiarlos)',
  model='modelo', qual='calidad', chunk='chunk_size', ov='overlap', tta='usar_tta', ext='extraer_instrumental',
  notes="""## ¿Qué modelo se usa para acapellas e instrumentales?
Por defecto, el **MelBand Roformer de KimberleyJSN**. Es una elección de uso, no de métricas: quien mantiene este Colab lo usa para acapellas y se queda con su resultado.

Según las métricas de la [guía de deton24](https://docs.google.com/document/d/17fjNvJzj8ZGSer7c7OFe_CNfUKbAxEh_OBv94ZdRG5c), puntúan más alto **Leap Xe de unwa** (voces) y **deux de becruily** (instrumental). Están los segundos y primeros de sus listas en *Avanzado → modelo*, por si quieres comparar. No hay un mejor modelo para todo: depende de la canción.

## ¿Qué significan los ajustes?
**Cada modelo tiene su propia configuración** (la que publicó su autor) y se carga sola al elegirlo. En `auto` no hay nada que tocar; al terminar se imprime qué valores se usaron.

- **Calidad** — *Máxima* sube el `overlap` a 8, que es el tope útil según jarredou («normalmente no tiene sentido pasar de 8»); tarda más. *Rápida* usa el `overlap` del autor.
- **chunk_size** — el tamaño de los trozos en que se corta la canción para procesarla. Cada modelo se entrenó con uno; `auto` usa el del autor.
- **overlap** — cuánto se pisan esos trozos entre sí. Más alto = uniones más limpias y más tiempo.
- **Formato** — `auto` guarda cada resultado igual que su canción original: mismo tipo (WAV/FLAC), mismos bits y misma frecuencia. Los modelos trabajan por dentro a 44 100 Hz, así que una canción de 48 000 Hz se devuelve a 48 000 Hz para que encaje en tu proyecto, sin que eso añada calidad. Un MP3 o M4A sale como WAV de 16 bits.
- **TTA** — procesa la canción tres veces (normal, canales invertidos, fase invertida) y promedia. Tarda el triple y la mejora rara vez se oye.
- **extraer_instrumental** — solo en modo manual: además del stem del modelo, guarda lo que queda al restarlo de la mezcla.

Algunos modelos (SW de 6 stems, DrumSep, SCNet…) no admiten cambiar chunk/overlap: siempre usan los de su autor.

## Problemas frecuentes
- **«No hay archivos de audio»** — la carpeta de entrada debe ser una *carpeta* (no un archivo) y distingue mayúsculas: `input`, no `Input`.
- **No aparece mi Drive** — vuelve a ejecutar *1. Preparar*.
- **Se quedó sin memoria** — usa calidad *Rápida* o un `chunk_size` más pequeño.
- Al terminar: *Entorno de ejecución → Desconectar y eliminar entorno*, para no gastar tus créditos."""),
 'en': dict(file='Colab_Inference_EN.ipynb', fauto='auto (same as the source file)', auto='Recommended (for what I picked above)',
  goals=[('acapella', 'Acapella (vocals) + instrumental'), ('instrumental', 'Instrumental'),
         ('stems', 'Stems: vocals, drums, bass, guitar, piano, other'), ('drum_pieces', 'Drum pieces: kick, snare, toms, hi-hat, cymbals'),
         ('karaoke', 'Karaoke: split lead vocal from backing'), ('dereverb', 'Remove reverb'), ('denoise', 'Remove noise')],
  quality=[('max', 'Maximum (recommended)'), ('fast', 'Fast')],
  intro=f"""# Music source separation — Colab Inference
Get **acapellas, instrumentals and stems** with the community's models, on top of [ZFTurbo](https://github.com/ZFTurbo/Music-Source-Separation-Training)'s code.

Based on the original notebook by **jarredou** & deton. This repo preserves it, keeps it working and backs up the models whose source account is gone. Credits for every model are in the [README](https://github.com/{REPO}#credits).

**How to use**
1. In your Google Drive create the folders `input` and `output`, and upload your songs to `input`.
2. Menu *Runtime → Change runtime type → T4 GPU*.
3. Run **1. Setup** (once per session).
4. In **2. Separate** pick what you want and run it. Nothing else needs changing.

[Versión en español](https://colab.research.google.com/github/{REPO}/blob/main/Colab_Inference_ES.ipynb)""",
  t1='# 1. Setup', drive='connect_google_drive',
  t2='# 2. Separate', want='i_want', inp='input_folder', out='output_folder', fmt='export_format',
  adv='### Advanced (optional — every model already ships its own settings, no need to change them)',
  model='model', qual='quality', chunk='chunk_size', ov='overlap', tta='use_tta', ext='extract_instrumental',
  notes="""## Which model is used for acapellas and instrumentals?
By default, **KimberleyJSN's MelBand Roformer**. It is a choice from use, not from metrics: the maintainer of this Colab uses it for acapellas and prefers its result.

By the metrics in [deton24's guide](https://docs.google.com/document/d/17fjNvJzj8ZGSer7c7OFe_CNfUKbAxEh_OBv94ZdRG5c), **unwa's Leap Xe** (vocals) and **becruily's deux** (instrumental) score higher. They sit second and first in their lists under *Advanced → model*, in case you want to compare. There is no single best model: it depends on the song.

## What do the settings mean?
**Every model has its own configuration** (the one its author published) and it loads by itself when you pick the model. On `auto` there is nothing to touch; the values used are printed when it finishes.

- **Quality** — *Maximum* raises `overlap` to 8, the useful ceiling according to jarredou ("normally there's no point going over 8"); it takes longer. *Fast* uses the author's `overlap`.
- **chunk_size** — the size of the pieces the song is cut into for processing. Each model was trained with one; `auto` uses the author's.
- **overlap** — how much those pieces overlap. Higher = cleaner joins and more time.
- **Format** — `auto` saves each result like its source song: same type (WAV/FLAC), same bit depth and same sample rate. The models work at 44,100 Hz internally, so a 48,000 Hz song is returned at 48,000 Hz to fit your project, without that adding quality. An MP3 or M4A comes out as 16-bit WAV.
- **TTA** — processes the song three times (normal, swapped channels, inverted phase) and averages. Three times slower and the gain is rarely audible.
- **extract_instrumental** — manual mode only: besides the model's stem, also saves what is left after subtracting it from the mix.

Some models (6-stem SW, DrumSep, SCNet…) take no chunk/overlap overrides: they always use their author's.

## Common problems
- **"No audio files"** — the input must be a *folder* (not a file) and is case sensitive: `input`, not `Input`.
- **My Drive does not show up** — run *1. Setup* again.
- **Out of memory** — use *Fast* quality or a smaller `chunk_size`.
- When done: *Runtime → Disconnect and delete runtime*, so you do not burn your credits."""),
}
CHUNKS = ['auto', 88200, 112455, 132300, 156555, 176400, 352800, 485100, 529200, 588800, 661500, 749259]


def code(src): return {'cell_type': 'code', 'metadata': {'cellView': 'form'}, 'execution_count': None, 'outputs': [], 'source': src.splitlines(keepends=True)}
def md(src): return {'cell_type': 'markdown', 'metadata': {}, 'source': src.splitlines(keepends=True)}


for lang, t in L.items():
    badge = f'<a href="https://colab.research.google.com/github/{REPO}/blob/main/{t["file"]}" target="_parent"><img src="https://colab.research.google.com/assets/colab-badge.svg" alt="Open In Colab"/></a>\n\n'
    goals = [g[1] for g in t['goals']]; quals = [q[1] for q in t['quality']]
    c1 = f"""#@markdown {t['t1']}
{t['drive']} = True #@param {{type:"boolean"}}
import importlib, os, sys, urllib.request
if {t['drive']}:
    from google.colab import drive
    drive.mount('/content/drive')
os.makedirs('/content/sepcolab', exist_ok=True)
for _f in ('sep.py', 'models.json'):
    urllib.request.urlretrieve('{RAW}' + _f, '/content/sepcolab/' + _f)
sys.path.insert(0, '/content/sepcolab')
import sep; importlib.reload(sep)
sep.setup('{lang}')
"""
    c2 = f"""#@markdown {t['t2']}
{t['want']} = {goals[0]!r} #@param {goals!r}
{t['inp']} = '/content/drive/MyDrive/input' #@param {{type:"string"}}
{t['out']} = '/content/drive/MyDrive/output' #@param {{type:"string"}}
{t['fmt']} = {t['fauto']!r} #@param {[t['fauto'], 'wav PCM_16', 'wav PCM_24', 'wav FLOAT', 'flac PCM_16', 'flac PCM_24']!r}
#@markdown ---
#@markdown {t['adv']}
{t['model']} = {t['auto']!r} #@param {[t['auto']] + names!r}
{t['qual']} = {quals[0]!r} #@param {quals!r}
{t['chunk']} = "auto" #@param {[str(c) for c in CHUNKS]!r} {{allow-input: true}}
{t['ov']} = "auto" #@param ["auto", "1", "2", "4", "6", "8"] {{allow-input: true}}
{t['tta']} = False #@param {{type:"boolean"}}
{t['ext']} = True #@param {{type:"boolean"}}
import sys
sys.path.insert(0, '/content/sepcolab')
import sep
sep.run(goal={dict((g[1], g[0]) for g in t['goals'])!r}[{t['want']}],
        model='auto' if {t['model']} == {t['auto']!r} else {t['model']},
        input_folder={t['inp']}, output_folder={t['out']}, export_format='auto' if {t['fmt']} == {t['fauto']!r} else {t['fmt']},
        quality={dict((q[1], q[0]) for q in t['quality'])!r}[{t['qual']}],
        chunk_size={t['chunk']}, overlap={t['ov']}, use_tta={t['tta']}, extract_instrumental={t['ext']}, lang='{lang}')
"""
    nb = {'nbformat': 4, 'nbformat_minor': 0,
          'metadata': {'colab': {'provenance': [], 'gpuType': 'T4'}, 'accelerator': 'GPU',
                       'kernelspec': {'name': 'python3', 'display_name': 'Python 3'}, 'language_info': {'name': 'python'}},
          'cells': [md(badge + t['intro']), code(c1), code(c2), md(t['notes'])]}
    json.dump(nb, open(f'{HERE}/{t["file"]}', 'w', encoding='utf-8'), indent=1, ensure_ascii=False)
    print('ok', t['file'])
