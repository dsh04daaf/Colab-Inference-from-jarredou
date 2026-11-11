# Changelog

## 2026-11-11
- **Full spectrum for hi-res songs.** The engine resamples every song to the model's rate (44.1 kHz), so with
  `auto` format a 96/176.4/192 kHz song came back at its own rate but cut at 22 kHz. Now the part of the original
  above the model's cut (the original minus its own down/up resampling) is shared between the stems, frame by
  frame, by how much each one carries at 18–21 kHz (silence there → instrumental/"other"). The stems still add up
  to the song (checked: residual −120 dB at 24 bits). Only for lossless sources; fixed formats keep the model rate.
- Drum pieces take their top band from the full-band drums stem, not from the whole song.
- Stems are rebuilt one at a time so long hi-res mixes do not run Colab out of RAM.
