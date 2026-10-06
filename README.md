# Colab Inference — from jarredou

Colab notebooks to separate music (acapellas, instrumentals, stems, drum pieces, de-reverb, de-noise) with the community's models,
running on [ZFTurbo's Music-Source-Separation-Training](https://github.com/ZFTurbo/Music-Source-Separation-Training).

| | |
|---|---|
| English | [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/dsh04daaf/Colab-Inference-from-jarredou/blob/main/Colab_Inference_EN.ipynb) |
| Español | [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/dsh04daaf/Colab-Inference-from-jarredou/blob/main/Colab_Inference_ES.ipynb) |

This is a continuation of the **Music-Source-Separation-Training-Colab-Inference** notebook made by **jarredou** & deton.
jarredou's GitHub and Hugging Face accounts no longer exist, which broke the notebook and the models hosted there. This repo:

- keeps the notebook working on the current Colab runtime;
- adds a simple mode: pick what you want (acapella, instrumental, stems…) and the recommended model and its settings are used;
- loads **each model's own settings** (the chunk size and overlap its author published) instead of one value for all;
- backs up the models that only survive as third-party re-uploads ([dshdaaf/separation-models](https://huggingface.co/dshdaaf/separation-models)) and falls back to that copy when a link dies;
- checks every source link weekly.

The plain restoration of jarredou's original notebooks lives in [dsh04daaf/colab](https://github.com/dsh04daaf/colab).

## Not our models

**None of these models are ours.** They were trained and released by the people credited below; all credit and all rights are theirs.
The goal of this project is preservation and keeping a free tool working, not taking anyone's work. Models are always downloaded from
their author's own link first; the backup is used only when that link is gone. **If you are the author of a model and want it removed,
renamed or credited differently, open an issue or a discussion and it will be done.**

**Ninguno de estos modelos es nuestro.** Los entrenaron y publicaron las personas acreditadas abajo; todo el crédito y todos los derechos son suyos.
El objetivo de este proyecto es la conservación y mantener funcionando una herramienta gratuita, no apropiarse del trabajo de nadie. Los modelos se descargan
siempre primero del enlace de su autor; el respaldo solo se usa cuando ese enlace ya no existe. **Si eres autor de un modelo y quieres que se retire,
se renombre o se acredite de otra forma, abre un issue o una discusión y se hará.**

## Credits

- **jarredou** & **deton24** — the original Colab notebook this is built from, and the [guide](https://docs.google.com/document/d/17fjNvJzj8ZGSer7c7OFe_CNfUKbAxEh_OBv94ZdRG5c) the recommendations come from.
- **ZFTurbo** — [Music-Source-Separation-Training](https://github.com/ZFTurbo/Music-Source-Separation-Training), the training and inference code.
- **Qupci** — kept jarredou's `colab-inference` branch alive in a fork; the code here is forked from it.
- **santilli_** — the requirements fix.
- Every model author, listed below.

## Créditos

Los mismos de arriba: el notebook original es de **jarredou** y **deton24**, el código es de **ZFTurbo**, y cada modelo es de su autor (tabla siguiente).

## Models

77 models. "Author settings" are the values in the config each author published; the notebook uses them by default.

| Model | Author | Where the notebook downloads it from | Backed up here | Author settings (chunk / overlap) | Size |
|---|---|---|---|---|---|
| VOCALS-MelBand-Roformer (by KimberleyJSN) | KimberleyJSN | [link](https://huggingface.co/KimberleyJSN/melbandroformer) | — | 352800 / 2 | 871 MiB |
| VOCALS-MelBand-Roformer (by Becruily) | Becruily | [link](https://huggingface.co/becruily/mel-band-roformer-vocals) | — | 352800 / 2 | 871 MiB |
| VOCALS-MelBand-Roformer voc_Fv5 (by Gabox) | Gabox | [link](https://huggingface.co/GaboxR67/MelBandRoformers) | — | 352800 / 1 | 871 MiB |
| VOCALS-MelBand-Roformer voc_Fv4 (by Gabox) | Gabox | [link](https://huggingface.co/GaboxR67/MelBandRoformers) | — | 352800 / 1 | 871 MiB |
| VOCALS-MelBand-Roformer voc_Fv6 experimental (by Gabox) | Gabox | [link](https://huggingface.co/GaboxR67/MelBandRoformers) | — | 352800 / 1 | 871 MiB |
| VOCALS-MelBand-Roformer voc_Fv7 beta 3 (by Gabox) | Gabox | [link](https://huggingface.co/GaboxR67/MelBandRoformers) | — | 352800 / 1 | 871 MiB |
| VOCALS-MelBand-Roformer voc_Fv7 beta 2 (by Gabox) | Gabox | [link](https://huggingface.co/GaboxR67/MelBandRoformers) | — | 352800 / 1 | 871 MiB |
| VOCALS-MelBand-Roformer voc_Fv7 beta (by Gabox) | Gabox | [link](https://huggingface.co/GaboxR67/MelBandRoformers) | — | 352800 / 1 | 871 MiB |
| VOCALS-MelBand-Roformer voc_Fv3 (by Gabox) | Gabox | [link](https://huggingface.co/GaboxR67/MelBandRoformers) | — | 352800 / 1 | 871 MiB |
| VOCALS-Melband-Roformer BigBeta6 (by unwa) | unwa | [link](https://huggingface.co/pcunwa/Mel-Band-Roformer-big) | — | 529200 / 2 | 1485 MiB |
| VOCALS-Melband-Roformer BigBeta6X (by unwa) | unwa | [link](https://huggingface.co/pcunwa/Mel-Band-Roformer-big) | — | 529200 / 2 | 1629 MiB |
| VOCALS-MelBand-Roformer voc_gabox2 (by Gabox) | Gabox | [link](https://huggingface.co/GaboxR67/MelBandRoformers) | — | 352800 / 1 | 871 MiB |
| VOCALS-MelBand-Roformer Kim FT 2 Bleedless (by Unwa) | Unwa | [link](https://huggingface.co/pcunwa/Kim-Mel-Band-Roformer-FT) | — | 485100 / 8 | 871 MiB |
| VOCALS-MelBand-Roformer Kim FT 2 (by Unwa) | Unwa | [link](https://huggingface.co/pcunwa/Kim-Mel-Band-Roformer-FT) | — | 485100 / 8 | 871 MiB |
| VOCALS-Mel-Roformer FT 3 Preview (by unwa) | unwa | [link](https://huggingface.co/pcunwa/Kim-Mel-Band-Roformer-FT) | — | 485100 / 8 | 871 MiB |
| VOCALS-MelBand-Roformer Kim FT (by Unwa) | Unwa | [link](https://huggingface.co/pcunwa/Kim-Mel-Band-Roformer-FT) | — | 485100 / 8 | 871 MiB |
| VOCALS-Melband-Roformer BigBeta5e (by unwa) | unwa | [link](https://huggingface.co/pcunwa/Mel-Band-Roformer-big) | — | 485100 / 2 | 1411 MiB |
| VOCALS-Mel-Roformer BigBeta4 (by unwa) | unwa | [link](https://huggingface.co/pcunwa/Mel-Band-Roformer-big) | — | 485100 / 2 | 1502 MiB |
| VOCALS-BS-Roformer Resurrection (by unwa) | unwa | [link](https://huggingface.co/pcunwa/BS-Roformer-Resurrection) | — | 785920 / 2 | 195 MiB |
| VOCALS-BS-Roformer Revive 3e (by unwa) | unwa | [link](https://huggingface.co/pcunwa/BS-Roformer-Revive) | — | 485100 / 2 | 610 MiB |
| VOCALS-BS-Roformer Revive 2 (by unwa) | unwa | [link](https://huggingface.co/pcunwa/BS-Roformer-Revive) | — | 485100 / 2 | 610 MiB |
| VOCALS-BS-Roformer Revive (by unwa) | unwa | [link](https://huggingface.co/pcunwa/BS-Roformer-Revive) | — | 485100 / 2 | 610 MiB |
| VOCALS-BS-RoformerLargev1 (by unwa) | unwa | [link](https://huggingface.co/Sucial/MSST-WebUI) | yes | 352800 / — | 706 MiB |
| VOCALS-BS-Roformer_1297 (by viperx) | viperx | [link](https://github.com/TRvlvr/model_repo) | yes | 352800 / 2 | 610 MiB |
| VOCALS-BS-Roformer_1296 (by viperx) | viperx | [link](https://github.com/TRvlvr/model_repo) | yes | 352800 / 4 | 610 MiB |
| VOCALS-InstVocHQ | Anjok07, aufr33 & ZFTurbo | [link](https://github.com/ZFTurbo/Music-Source-Separation-Training) | — | 261120 / 4 (fixed) | 427 MiB |
| INST-Mel-Roformer v1e (by unwa) | unwa | [link](https://huggingface.co/pcunwa/Mel-Band-Roformer-Inst) | — | 485100 / 2 | 871 MiB |
| INST-Mel-Roformer v1e+ (by unwa) | unwa | [link](https://huggingface.co/pcunwa/Mel-Band-Roformer-Inst) | — | 485100 / 2 | 871 MiB |
| INST-BS-Roformer Resurrection (by unwa) | unwa | [link](https://huggingface.co/pcunwa/BS-Roformer-Resurrection) | — | 749259 / 2 | 195 MiB |
| INST-Mel-Roformer INSTV8B (by Gabox) | Gabox | [link](https://huggingface.co/GaboxR67/MelBandRoformers) | — | 485100 / 2 | 871 MiB |
| INST-MelBand-Roformer Inst_Fv8 v2 (by Gabox) | Gabox | [link](https://huggingface.co/GaboxR67/MelBandRoformers) | — | 485100 / 2 | 871 MiB |
| INST-MelBand-Roformer (by Becruily) | Becruily | [link](https://huggingface.co/becruily/mel-band-roformer-instrumental) | — | 352800 / 2 | 871 MiB |
| INST-Mel-Roformer INSTV7 (by Gabox) | Gabox | [link](https://huggingface.co/GaboxR67/MelBandRoformers) | — | 485100 / 2 | 871 MiB |
| INST-MelBand-Roformer Inst_Fv4 (by Gabox) | Gabox | [link](https://huggingface.co/GaboxR67/MelBandRoformers) | — | 485100 / 2 | 871 MiB |
| INST-Mel-Roformer Neo_InstVFX (by neoculture) | neoculture | [link](https://huggingface.co/natanworkspace/melband_roformer) | — | 485100 / 2 | 871 MiB |
| INST-Mel-Roformer INSTFVX (by Gabox) | Gabox | [link](https://huggingface.co/GaboxR67/MelBandRoformers) | — | 485100 / 2 | 871 MiB |
| INST-Mel-Roformer INSTV7N (by Gabox) | Gabox | [link](https://huggingface.co/GaboxR67/MelBandRoformers) | — | 485100 / 2 | 871 MiB |
| INST-Mel-Roformer INSTFV7Z (by Gabox) | Gabox | [link](https://huggingface.co/GaboxR67/MelBandRoformers) | — | 485100 / 2 | 871 MiB |
| INST-Mel-Roformer INSTV6N (by Gabox) | Gabox | [link](https://huggingface.co/GaboxR67/MelBandRoformers) | — | 485100 / 2 | 871 MiB |
| INST-Mel-Roformer INSTV5 (by Gabox) | Gabox | [link](https://huggingface.co/GaboxR67/MelBandRoformers) | — | 485100 / 2 | 871 MiB |
| INST-Mel-Roformer INSTV6 (by Gabox) | Gabox | [link](https://huggingface.co/GaboxR67/MelBandRoformers) | — | 485100 / 2 | 871 MiB |
| INST-Mel-Roformer inst_gabox3 (by Gabox) | Gabox | [link](https://huggingface.co/GaboxR67/MelBandRoformers) | — | 485100 / 2 | 871 MiB |
| INST-Mel-Roformer Metal Model Preview (by Mesk) | Mesk | [link](https://huggingface.co/meskvlla33/metal_roformer_preview) | — | 881559 / 5 | 901 MiB |
| INST-VOC-Mel-Roformer a.k.a. duality (by unwa) | unwa | [link](https://huggingface.co/pcunwa/Mel-Band-Roformer-InstVoc-Duality) | — | 485100 / 2 | 1639 MiB |
| INST-VOC-Mel-Roformer a.k.a. duality v2 (by unwa) | unwa | [link](https://huggingface.co/pcunwa/Mel-Band-Roformer-InstVoc-Duality) | — | 485100 / 2 | 1639 MiB |
| INST-Mel-Roformer v1 (by unwa) | unwa | [link](https://huggingface.co/pcunwa/Mel-Band-Roformer-Inst) | — | 485100 / 2 | 871 MiB |
| INST-Mel-Roformer v1+ (by unwa) | unwa | [link](https://huggingface.co/pcunwa/Mel-Band-Roformer-Inst) | — | 485100 / 2 | 871 MiB |
| INST-Mel-Roformer v2 (by unwa) | unwa | [link](https://huggingface.co/pcunwa/Mel-Band-Roformer-Inst) | — | 485100 / 2 | 1502 MiB |
| KARAOKE-BS-Roformer (by anvuew) | anvuew | [link](https://huggingface.co/anvuew/karaoke_bs_roformer) | — | 640000 / 4 | 195 MiB |
| KARAOKE-MelBand-Roformer (by becruily) | becruily | [link](https://huggingface.co/becruily/mel-band-roformer-karaoke) | — | 485100 / 8 | 1639 MiB |
| KARAOKE-MelBand-Roformer (by aufr33 & viperx) | aufr33 & viperx | [link](https://huggingface.co/Eddycrack864/audio-separator-models) | yes | 352800 / 4 | 871 MiB |
| OTHER-BS-Roformer_1053 (by viperx) | viperx | [link](https://github.com/TRvlvr/model_repo) | yes | 131584 / 4 | 375 MiB |
| 6STEMS-BS-Roformer-SW | unknown ("shared weights") | [link](https://huggingface.co/enerjazzer/BS-ROFO-SW-Fixed) | yes | 588800 / 2 (fixed) | 667 MiB |
| 4STEMS-MelBand-Roformer_Large (by Amane) | Amane | [link](https://huggingface.co/Aname-Tommy/melbandroformer4stems) | — | 661500 / 4 (fixed) | 3590 MiB |
| 4STEMS-SCNet_XL_MUSDB18 (by ZFTurbo) | ZFTurbo | [link](https://github.com/ZFTurbo/Music-Source-Separation-Training) | — | 485100 / 4 (fixed) | 206 MiB |
| 4STEMS-SCNet_Large (by starrytong) | starrytong | [link](https://github.com/ZFTurbo/Music-Source-Separation-Training) | — | 485100 / 4 (fixed) | 161 MiB |
| 4STEMS-BS-Roformer_MUSDB18 (by ZFTurbo) | ZFTurbo | [link](https://github.com/ZFTurbo/Music-Source-Separation-Training) | — | 485100 / 2 (fixed) | 503 MiB |
| 4STEMS-SCNet_MUSDB18 (by starrytong) | starrytong | [link](https://github.com/ZFTurbo/Music-Source-Separation-Training) | — | 485100 / 4 (fixed) | 40 MiB |
| CROWD-REMOVAL-MelBand-Roformer (by aufr33) | aufr33 | [link](https://github.com/ZFTurbo/Music-Source-Separation-Training) | — | 352800 / 4 | 871 MiB |
| VOCALS-VitLarge23 (by ZFTurbo) | ZFTurbo | [link](https://github.com/ZFTurbo/Music-Source-Separation-Training) | — | 261632 / 4 (fixed) | 824 MiB |
| CINEMATIC-BandIt_Plus (by kwatcharasupat) | kwatcharasupat | [link](https://github.com/ZFTurbo/Music-Source-Separation-Training) | — | 264600 / 4 (fixed) | 142 MiB |
| CINEMATIC-BandIt_v2 multi (by kwatcharasupat) | kwatcharasupat | [link](https://huggingface.co/Politrees/UVR_resources) | yes | 384000 / 4 (fixed) | 142 MiB |
| DRUMSEP-MDX23C_DrumSep_5stem_new (by jarredou) | jarredou | [link](https://huggingface.co/xavriley/source_separation_mirror) | yes | 523776 / 4 (fixed) | 417 MiB |
| DRUMSEP-MDX23C_DrumSep_6stem (by aufr33 & jarredou) | aufr33 & jarredou | [link](https://huggingface.co/Sucial/MSST-WebUI) | yes | 130560 / 4 (fixed) | 417 MiB |
| DE-REVERB-MDX23C (by aufr33 & jarredou) | aufr33 & jarredou | [link](https://huggingface.co/Sucial/MSST-WebUI) | yes | 261120 / 4 (fixed) | 427 MiB |
| DE-REVERB-MelBand-Roformer aggr./v2/19.1729 (by anvuew) | anvuew | [link](https://huggingface.co/anvuew/dereverb_mel_band_roformer) | — | 352800 / 2 (fixed) | 871 MiB |
| DE-REVERB-BS-Roformer dereverb_room mono (by anvuew) | anvuew | [link](https://huggingface.co/anvuew/dereverb_room) | — | 384000 / 2 (fixed) | 113 MiB |
| DE-REVERB-MelBand-Roformer mono 20.4029 (by anvuew) | anvuew | [link](https://huggingface.co/anvuew/dereverb_mel_band_roformer) | — | 352800 / 2 (fixed) | 871 MiB |
| DE-REVERB-Echo-MelBand-Roformer (by Sucial) | Sucial | [link](https://huggingface.co/Sucial/Dereverb-Echo_Mel_Band_Roformer) | — | 352800 / 4 (fixed) | 797 MiB |
| LEAD-VOCAL-DE-REVERB-MelBand-Roformer (by Gabox) | Gabox | [link](https://huggingface.co/GaboxR67/MelBandRoformers) | — | 485100 / 8 (fixed) | 871 MiB |
| DENOISE-MelBand-Roformer-1 (by aufr33) | aufr33 | [link](https://github.com/ZFTurbo/Music-Source-Separation-Training) | — | 352800 / 4 | 871 MiB |
| DENOISE-MelBand-Roformer-2 (by aufr33) | aufr33 | [link](https://github.com/ZFTurbo/Music-Source-Separation-Training) | — | 352800 / 4 | 871 MiB |
| DEBLEED-MelBand-Roformer (by unwa/97chris) | unwa/97chris | [link](https://huggingface.co/Eddycrack864/audio-separator-models) | yes | 485100 / 2 | 871 MiB |
| DENOISE-DEBLEED-MelBand-Roformer (by Gabox) | Gabox | [link](https://huggingface.co/GaboxR67/MelBandRoformers) | — | 485100 / 2 | 871 MiB |
| VOCALS-Male Female-BS-RoFormer Male Female Beta 7_2889 (by aufr33) | aufr33 | [link](https://huggingface.co/RareSirMix/AIModelRehosting) | yes | 352800 / 2 | 503 MiB |
| PHANTOM-CENTER-HTDemucs (by wesleyr36) | wesleyr36 | [link](https://huggingface.co/baicai1145/pymss) | yes | 132300 / — | 160 MiB |
| GUITAR-MelBand-Roformer (by becruily) | becruily | [link](https://huggingface.co/becruily/mel-band-roformer-guitar) | — | 485100 / 2 | 43 MiB |

## How it is put together

- `models.json` — the catalog: source links, backup links, sizes, checksums and each author's settings.
- `sep.py` — what the notebook runs: setup, downloads with fallback, per-model settings, separation.
- `scripts/` — generators for the catalog, the notebooks and this README, and the weekly source monitor.
