# Audio Digital Signal Processing Engine

A tiny dependency-free Python DSP engine for generating signals, applying simple filters, inspecting frequency bins, and writing a minimal WAV file.

Portfolio demo: https://rjedwards.dev/projects/audio-dsp

## Features

- Generate sine, square, saw, noise, impulse, and click-train buffers.
- Parameterized frequency, gain, lowpass alpha, and highpass alpha.
- Apply gain, one-pole lowpass, and one-pole highpass effects.
- Compute a small DFT magnitude spectrum for buffers up to 256 samples.
- Print approximate bin center frequencies in Hz.
- Write mono 16-bit PCM WAV files with the standard `wave` module.

## Run

```bash
python -m audio_dsp
python -m audio_dsp --waveform square --frequency 220 --effect lowpass --lowpass-alpha 0.2
python -m audio_dsp --waveform noise --effect highpass --write-wav out.wav
python -m audio_dsp --waveform saw --effect gain --gain 1.8 --write-wav saw.wav
```

The CLI prints sample metrics, compact spectrum bins, and bin frequency labels. No third-party packages are required.
