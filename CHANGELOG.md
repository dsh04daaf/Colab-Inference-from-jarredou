# Changelog

## 2026-11-11 — catalog v3: guide defaults + 42 models
- **Defaults are now the best public model of each kind in deton24's guide (edition 2026-11-10)**: acapella = Leap Xe (unwa),
  instrumental = deux (becruily), karaoke = BS-Roformer (becruily & frazer), remove noise = denoise/debleed (Gabox);
  stems (SW), drum pieces (SW → DrumSep 5 stem), remove reverb (anvuew BS) unchanged. Notebook notes rewritten with the table.
- **42 models added** (185 total), taken from the Colab deton24 & makidanye maintain (listra92's fork): unwa's HyperACE v1/v2
  (voc/inst), Inst-FNO, EXP Siamese, Large-Inst; anvuew voc_mag v2; SW vocals-only; gilliaan's phantom center (MDX23C/SCNet/BS/Mel),
  karaoke, de-effect, invert clean, drums duality, bowed strings, stereoize; becruily's delimit; Apollo vocal enhancers; and more.
  All checked against the code (names and shapes); 3 left out (VRL needs code nobody publishes, BandIt v2 Eng not checkable,
  one Sucial link dead) and 8 were duplicates of models already listed.
- **Models with their own code** (`bs_roformer_custom`): the runner copies the model's `bs_roformer.py` into the engine before
  running (engine fork commit b285bd3). Extra pip packages per model (`pip`, e.g. neuraloperator for FNO) install only when used.
- Lists re-ranked by the new guide edition (VOCALS, INST, KARAOKE, DE-REVERB, DENOISE).
- Output names: the instrumental is always `_instrumental` (whatever the model calls it); Gabox denoise gives `_denoised` / `_noise`.
- Backup: 5 more models that only live in third-party re-uploads (noblebarkrr, listra92, deton24) → dshdaaf/separation-models.
- Fixed the config link of gilliaan's Phantom Center BS-Roformer v2 (pointed to the .ckpt) and added its v3beta.

## 2026-11-11 (later)
- **Reverted** the top-band restoration below. The part above the model's cut cannot be separated by the model,
  only shared by a rule, so some cymbal "air" could end up in the vocal stem. Back to the plain model output:
  hi-res songs come back at their own rate but cut at the model's band (≈22 kHz).

## 2026-11-11
- **Full spectrum for hi-res songs.** The engine resamples every song to the model's rate (44.1 kHz), so with
  `auto` format a 96/176.4/192 kHz song came back at its own rate but cut at 22 kHz. Now the part of the original
  above the model's cut (the original minus its own down/up resampling) is shared between the stems, frame by
  frame, by how much each one carries at 18–21 kHz (silence there → instrumental/"other"). The stems still add up
  to the song (checked: residual −120 dB at 24 bits). Only for lossless sources; fixed formats keep the model rate.
- Drum pieces take their top band from the full-band drums stem, not from the whole song.
- Stems are rebuilt one at a time so long hi-res mixes do not run Colab out of RAM.
