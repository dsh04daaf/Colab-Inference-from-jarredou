---
license: other
tags:
- audio
- music-source-separation
---
# Backup of music source separation models

Preservation copy of the models used by the [Colab Inference notebook](https://github.com/dsh04daaf/Colab-Inference-from-jarredou) that today only survive as
third-party re-uploads (their original accounts are gone). Files are byte-for-byte copies; nothing was retrained or modified.

**None of these models are ours.** They were trained and released by the people credited below; all credit and all rights are theirs.
The goal of this project is preservation and keeping a free tool working, not taking anyone's work. Models are always downloaded from
their author's own link first; the backup is used only when that link is gone. **If you are the author of a model and want it removed,
renamed or credited differently, open an issue or a discussion and it will be done.**

**Ninguno de estos modelos es nuestro.** Los entrenaron y publicaron las personas acreditadas abajo; todo el crédito y todos los derechos son suyos.
El objetivo de este proyecto es la conservación y mantener funcionando una herramienta gratuita, no apropiarse del trabajo de nadie. Los modelos se descargan
siempre primero del enlace de su autor; el respaldo solo se usa cuando ese enlace ya no existe. **Si eres autor de un modelo y quieres que se retire,
se renombre o se acredite de otra forma, abre un issue o una discusión y se hará.**

| Model | Author | File | Size | sha256 | Copied from |
|---|---|---|---|---|---|
| VOCALS-BS-RoformerLargev1 (by unwa) | unwa | `BS-Roformer_LargeV1.ckpt` | 706 MiB | `3d1334565bb9e4c0…` | https://huggingface.co/Sucial/MSST-WebUI |
| VOCALS-BS-RoformerLargev1 (by unwa) | unwa | `BS-Roformer_LargeV1.yaml` | 0 MiB | `a88e3df7d62cd352…` | https://huggingface.co/baicai1145/pymss |
| VOCALS-BS-Roformer_1297 (by viperx) | viperx | `model_bs_roformer_ep_317_sdr_12.9755.yaml` | 0 MiB | `42e5635ceab7287b…` | https://raw.githubusercontent.com/ZFTurbo/Music-Source-Separation-Training |
| VOCALS-BS-Roformer_1297 (by viperx) | viperx | `model_bs_roformer_ep_317_sdr_12.9755.ckpt` | 610 MiB | `5b84f37e8d444c8c…` | https://github.com/TRvlvr/model_repo |
| VOCALS-BS-Roformer_1296 (by viperx) | viperx | `model_bs_roformer_ep_368_sdr_12.9628.ckpt` | 610 MiB | `f6c94864adfb73bb…` | https://github.com/TRvlvr/model_repo |
| VOCALS-BS-Roformer_1296 (by viperx) | viperx | `model_bs_roformer_ep_368_sdr_12.9628.yaml` | 0 MiB | `aea599b3f9bd4892…` | https://raw.githubusercontent.com/TRvlvr/application_data |
| KARAOKE-MelBand-Roformer (by aufr33 & viperx) | aufr33 & viperx | `mel_band_roformer_karaoke_aufr33_viperx_sdr_10.1956.ckpt` | 871 MiB | `1de20d459332fe88…` | https://huggingface.co/Eddycrack864/audio-separator-models |
| KARAOKE-MelBand-Roformer (by aufr33 & viperx) | aufr33 & viperx | `config_mel_band_roformer_karaoke.yaml` | 0 MiB | `1ad4ebd15653108e…` | https://github.com/deton24/Colab-for-new-MDX_UVR_models |
| OTHER-BS-Roformer_1053 (by viperx) | viperx | `model_bs_roformer_ep_937_sdr_10.5309.ckpt` | 375 MiB | `a2e825a03bc908cb…` | https://github.com/TRvlvr/model_repo |
| OTHER-BS-Roformer_1053 (by viperx) | viperx | `model_bs_roformer_ep_937_sdr_10.5309.yaml` | 0 MiB | `302b6cee54adf397…` | https://raw.githubusercontent.com/TRvlvr/application_data |
| 6STEMS-BS-Roformer-SW | unknown ("shared weights") | `BS-Rofo-SW-Fixed.yaml` | 0 MiB | `f9fada9f94e5ba2d…` | https://huggingface.co/enerjazzer/BS-ROFO-SW-Fixed |
| 6STEMS-BS-Roformer-SW | unknown ("shared weights") | `BS-Rofo-SW-Fixed.ckpt` | 667 MiB | `24e7d35ee9c64415…` | https://huggingface.co/enerjazzer/BS-ROFO-SW-Fixed |
| CINEMATIC-BandIt_v2 multi (by kwatcharasupat) | kwatcharasupat | `config_dnr_bandit_v2_mus64.yaml` | 0 MiB | `b7062645d3fcd996…` | https://raw.githubusercontent.com/ZFTurbo/Music-Source-Separation-Training |
| CINEMATIC-BandIt_v2 multi (by kwatcharasupat) | kwatcharasupat | `checkpoint-multi_fixed.ckpt` | 142 MiB | `20bcd513dc7eb054…` | https://huggingface.co/Politrees/UVR_resources |
| DRUMSEP-MDX23C_DrumSep_5stem_new (by jarredou) | jarredou | `drumsep_5stems_mdx23c_jarredou.ckpt` | 417 MiB | `1f8e636fb674b88a…` | https://huggingface.co/xavriley/source_separation_mirror |
| DRUMSEP-MDX23C_DrumSep_5stem_new (by jarredou) | jarredou | `config_mdx23c_drumsep2025.yaml` | 0 MiB | `d2962f43d6682e8e…` | https://huggingface.co/xavriley/source_separation_mirror |
| DRUMSEP-MDX23C_DrumSep_6stem (by aufr33 & jarredou) | aufr33 & jarredou | `aufr33-jarredou_DrumSep_model_mdx23c_ep_141_sdr_10.8059.ckpt` | 417 MiB | `d2a4aa53eb584d21…` | https://huggingface.co/Sucial/MSST-WebUI |
| DRUMSEP-MDX23C_DrumSep_6stem (by aufr33 & jarredou) | aufr33 & jarredou | `config_drumsep_mdx23c.yaml` | 0 MiB | `17d1649a227f8411…` | https://huggingface.co/Politrees/UVR_resources |
| DE-REVERB-MDX23C (by aufr33 & jarredou) | aufr33 & jarredou | `dereverb_mdx23c_sdr_6.9096.ckpt` | 427 MiB | `eae2471b707758d7…` | https://huggingface.co/Sucial/MSST-WebUI |
| DE-REVERB-MDX23C (by aufr33 & jarredou) | aufr33 & jarredou | `config_dereverb_mdx23c.yaml` | 0 MiB | `a0cf11216913ab89…` | https://huggingface.co/Eddycrack864/audio-separator-models |
| DEBLEED-MelBand-Roformer (by unwa/97chris) | unwa/97chris | `mel_band_roformer_bleed_suppressor_v1.ckpt` | 871 MiB | `a9a9d10faa7f8997…` | https://huggingface.co/Eddycrack864/audio-separator-models |
| DEBLEED-MelBand-Roformer (by unwa/97chris) | unwa/97chris | `config_mel_band_roformer_bleed_suppressor_v1.yaml` | 0 MiB | `bca5755de9946ded…` | https://huggingface.co/Eddycrack864/audio-separator-models |
| VOCALS-Male Female-BS-RoFormer Male Female Beta 7_2889 (by aufr33) | aufr33 | `bs_roformer_male_female_by_aufr33_sdr_7.2889.ckpt` | 503 MiB | `3cf11736d1b42a11…` | https://huggingface.co/RareSirMix/AIModelRehosting |
| VOCALS-Male Female-BS-RoFormer Male Female Beta 7_2889 (by aufr33) | aufr33 | `config_chorus_male_female_bs_roformer.yaml` | 0 MiB | `e952a90412ed3e9d…` | https://huggingface.co/Sucial/Chorus_Male_Female_BS_Roformer |
| PHANTOM-CENTER-HTDemucs (by wesleyr36) | wesleyr36 | `model_htdemucs_ep_21_sdr_13.6970.ckpt` | 160 MiB | `b9970dca36a15c0d…` | https://huggingface.co/baicai1145/pymss |
| PHANTOM-CENTER-HTDemucs (by wesleyr36) | wesleyr36 | `model_htdemucs_ep_21_sdr_13.6970.yaml` | 0 MiB | `cdc9f166e42ef308…` | https://huggingface.co/baicai1145/pymss |

Licenses: each model keeps whatever terms its author set. Where the author stated none, none is claimed here.
