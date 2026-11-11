# Changelog

## 2026-11-11 — 32-bit float WAV by default
- **Default output is now 32-bit float WAV at 44.1 kHz** ("wav FLOAT 32 bits (recomendado: no recorta picos)"). Not more
  quality: separated stems can go over 0 dBFS (resampling to 44.1 kHz turns a master's inter-sample/true peaks into real
  samples, and removing the vocals can leave the instrumental louder than the mix); 16/24-bit PCM clips them, float keeps
  them so the gain can be lowered later. The run says whether any stem actually went over 0 dBFS. `auto` stays as an option.
- Final file names (`_instrumental`, `_denoised`…) are set before the messages that mention them, and only on the files
  that run wrote (not older ones in the same folder).
- Fixed: the "the file ending in _instrumental is the instrumental" line was never printed (wrong indentation since v3).

## 2026-11-11 — no more fake hi-res
- **`auto` format keeps the source's type and bit depth but always writes at the model's sample rate (44.1 kHz)**.
  178 of 185 configs say 44100 (6 say nothing → the engine's default 44100; BandIt v2 says 48000), and the engine
  resamples every song to it, so the model never sees anything above 22.05 kHz. Writing a 176.4 kHz song's stems back at
  176.4 kHz (what `auto` did) gave a 24/176.4 file with the 22 kHz cut: fake hi-res. The message says so when it applies.
- Bit depth is real: the engine reads float32, the model runs in mixed precision (float16/32, `use_amp`) and writes 32-bit float.
- Stems that go over 0 dBFS are flagged when the output is 16/24-bit PCM (soundfile clips them); `wav FLOAT` keeps them.

## 2026-11-11 — source monitor fixed + guide watch
- **The weekly monitor had failed every Monday since 2026-10-19**: mirror accounts (Eddycrack864 & co., which re-upload
  other people's models by the hundred) pushed the report past GitHub's 65,536-character issue limit; the failed step also
  skipped saving the snapshot, so the same report came back every week. Mirrors are no longer tracked as authors, the
  report is grouped per account and capped, and the snapshot is saved even when the issue step fails.
- **deton24's guide is now watched too**: when its edition changes, the issue lists the new "Last updates and news"
  items and the model entries with new metrics, next to the edition the notebook's defaults follow (`guide_edition`).

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
