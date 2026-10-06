"""README.md (GitHub) y HF_README.md (tarjeta del repo de respaldo) desde models.json."""
import json, os
HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
REPO = 'dsh04daaf/Colab-Inference-from-jarredou'
HF = 'dshdaaf/separation-models'
cat = json.load(open(f'{HERE}/models.json', encoding='utf-8'))
badge = lambda f: f'[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/{REPO}/blob/main/{f})'


def src(m):
    u = [f for f in m['files'] if f['role'] == 'checkpoint'][0]['url'].split('/')
    return '/'.join(u[:5])


rows = []
for m in cat['models']:
    ck = [f for f in m['files'] if f['role'] == 'checkpoint'][0]
    st = f"{m['chunk_size']} / {m['overlap'] if m['overlap'] is not None else '—'}" + ('' if m['tunable'] else ' (fixed)')
    rows.append(f"| {m['name']} | {m['author']} | [link]({src(m)}) | {'yes' if 'backup' in ck else '—'} | {st} | {ck['bytes'] / 2**20:.0f} MiB |")
table = '| Model | Author | Where the notebook downloads it from | Backed up here | Author settings (chunk / overlap) | Size |\n|---|---|---|---|---|---|\n' + '\n'.join(rows)
STATEMENT = """**None of these models are ours.** They were trained and released by the people credited below; all credit and all rights are theirs.
The goal of this project is preservation and keeping a free tool working, not taking anyone's work. Models are always downloaded from
their author's own link first; the backup is used only when that link is gone. **If you are the author of a model and want it removed,
renamed or credited differently, open an issue or a discussion and it will be done.**"""
STATEMENT_ES = """**Ninguno de estos modelos es nuestro.** Los entrenaron y publicaron las personas acreditadas abajo; todo el crédito y todos los derechos son suyos.
El objetivo de este proyecto es la conservación y mantener funcionando una herramienta gratuita, no apropiarse del trabajo de nadie. Los modelos se descargan
siempre primero del enlace de su autor; el respaldo solo se usa cuando ese enlace ya no existe. **Si eres autor de un modelo y quieres que se retire,
se renombre o se acredite de otra forma, abre un issue o una discusión y se hará.**"""
readme = f"""# Colab Inference — from jarredou

Colab notebooks to separate music (acapellas, instrumentals, stems, drum pieces, de-reverb, de-noise) with the community's models,
running on [ZFTurbo's Music-Source-Separation-Training](https://github.com/ZFTurbo/Music-Source-Separation-Training).

| | |
|---|---|
| English | {badge('Colab_Inference_EN.ipynb')} |
| Español | {badge('Colab_Inference_ES.ipynb')} |

This is a continuation of the **Music-Source-Separation-Training-Colab-Inference** notebook made by **jarredou** & deton.
jarredou's GitHub and Hugging Face accounts no longer exist, which broke the notebook and the models hosted there. This repo:

- keeps the notebook working on the current Colab runtime;
- adds a simple mode: pick what you want (acapella, instrumental, stems…) and the recommended model and its settings are used;
- loads **each model's own settings** (the chunk size and overlap its author published) instead of one value for all;
- backs up the models that only survive as third-party re-uploads ([{HF}](https://huggingface.co/{HF})) and falls back to that copy when a link dies;
- checks every source link weekly.

The plain restoration of jarredou's original notebooks lives in [dsh04daaf/colab](https://github.com/dsh04daaf/colab).

## Not our models

{STATEMENT}

{STATEMENT_ES}

## Credits

- **jarredou** & **deton24** — the original Colab notebook this is built from, and the [guide](https://docs.google.com/document/d/17fjNvJzj8ZGSer7c7OFe_CNfUKbAxEh_OBv94ZdRG5c) the recommendations come from.
- **ZFTurbo** — [Music-Source-Separation-Training](https://github.com/ZFTurbo/Music-Source-Separation-Training), the training and inference code.
- **Qupci** — kept jarredou's `colab-inference` branch alive in a fork; the code here is forked from it.
- **santilli_** — the requirements fix.
- Every model author, listed below.

## Créditos

Los mismos de arriba: el notebook original es de **jarredou** y **deton24**, el código es de **ZFTurbo**, y cada modelo es de su autor (tabla siguiente).

## Models

{len(cat['models'])} models. "Author settings" are the values in the config each author published; the notebook uses them by default.

{table}

## How it is put together

- `models.json` — the catalog: source links, backup links, sizes, checksums and each author's settings.
- `sep.py` — what the notebook runs: setup, downloads with fallback, per-model settings, separation.
- `scripts/` — generators for the catalog, the notebooks and this README, and the weekly source monitor.
"""
open(f'{HERE}/README.md', 'w', encoding='utf-8').write(readme)
bk = [(m, f) for m in cat['models'] for f in m['files'] if 'backup' in f]
brow = '\n'.join(f"| {m['name']} | {m['author']} | `{f['name']}` | {f['bytes'] / 2**20:.0f} MiB | `{f['sha256'][:16]}…` | {'/'.join(f['url'].split('/')[:5])} |" for m, f in bk)
hf = f"""---
license: other
tags:
- audio
- music-source-separation
---
# Backup of music source separation models

Preservation copy of the models used by the [Colab Inference notebook](https://github.com/{REPO}) that today only survive as
third-party re-uploads (their original accounts are gone). Files are byte-for-byte copies; nothing was retrained or modified.

{STATEMENT}

{STATEMENT_ES}

| Model | Author | File | Size | sha256 | Copied from |
|---|---|---|---|---|---|
{brow}

Licenses: each model keeps whatever terms its author set. Where the author stated none, none is claimed here.
"""
open(f'{HERE}/HF_README.md', 'w', encoding='utf-8').write(hf)
print('ok', len(rows), 'modelos,', len(bk), 'archivos respaldados')
