"""Dependency-free audio DSP helpers."""

from .engine import (
    SAMPLE_RATE,
    apply_effect,
    bin_frequency_hz,
    clicks,
    dft_magnitude,
    gain,
    generate_waveform,
    highpass,
    impulse,
    lowpass,
    metrics,
    noise,
    saw,
    sine,
    square,
    write_wav,
)

__all__ = [
    "SAMPLE_RATE",
    "apply_effect",
    "bin_frequency_hz",
    "clicks",
    "dft_magnitude",
    "gain",
    "generate_waveform",
    "highpass",
    "impulse",
    "lowpass",
    "metrics",
    "noise",
    "saw",
    "sine",
    "square",
    "write_wav",
]
