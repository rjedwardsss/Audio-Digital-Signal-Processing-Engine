from __future__ import annotations

import math
import random
import struct
import wave
from typing import Iterable

SampleBuffer = list[float]

SAMPLE_RATE = 8000


def clamp(sample: float) -> float:
    return max(-1.0, min(1.0, sample))


def sine(
    frequency: float = 440.0,
    seconds: float = 1.0,
    sample_rate: int = SAMPLE_RATE,
    amplitude: float = 0.65,
) -> SampleBuffer:
    count = int(seconds * sample_rate)
    return [amplitude * math.sin(2 * math.pi * frequency * i / sample_rate) for i in range(count)]


def square(
    frequency: float = 440.0,
    seconds: float = 1.0,
    sample_rate: int = SAMPLE_RATE,
    amplitude: float = 0.65,
) -> SampleBuffer:
    count = int(seconds * sample_rate)
    amp = amplitude * 0.85
    out: SampleBuffer = []
    for i in range(count):
        phase = (frequency * i) / sample_rate
        frac = phase - math.floor(phase)
        out.append(amp if frac < 0.5 else -amp)
    return out


def saw(
    frequency: float = 440.0,
    seconds: float = 1.0,
    sample_rate: int = SAMPLE_RATE,
    amplitude: float = 0.65,
) -> SampleBuffer:
    count = int(seconds * sample_rate)
    amp = amplitude * 0.85
    out: SampleBuffer = []
    for i in range(count):
        phase = (frequency * i) / sample_rate
        frac = phase - math.floor(phase)
        out.append((2 * frac - 1) * amp)
    return out


def noise(
    seconds: float = 1.0,
    sample_rate: int = SAMPLE_RATE,
    amplitude: float = 0.35,
    seed: int = 7,
) -> SampleBuffer:
    rng = random.Random(seed)
    return [rng.uniform(-amplitude, amplitude) for _ in range(int(seconds * sample_rate))]


def impulse(
    seconds: float = 1.0,
    sample_rate: int = SAMPLE_RATE,
    amplitude: float = 0.65,
) -> SampleBuffer:
    count = max(1, int(seconds * sample_rate))
    out = [0.0] * count
    out[0] = amplitude
    return out


def clicks(
    frequency: float = 440.0,
    seconds: float = 1.0,
    sample_rate: int = SAMPLE_RATE,
    amplitude: float = 0.65,
) -> SampleBuffer:
    count = max(1, int(seconds * sample_rate))
    out = [0.0] * count
    period = max(2, round(sample_rate / max(1.0, frequency / 8.0)))
    for i in range(0, count, period):
        out[i] = amplitude
    return out


def generate_waveform(
    kind: str,
    *,
    frequency: float = 440.0,
    seconds: float = 0.5,
    sample_rate: int = SAMPLE_RATE,
    amplitude: float | None = None,
    seed: int = 7,
) -> SampleBuffer:
    if kind == "noise":
        return noise(
            seconds=seconds,
            sample_rate=sample_rate,
            amplitude=0.35 if amplitude is None else amplitude,
            seed=seed,
        )
    amp = 0.65 if amplitude is None else amplitude
    if kind == "square":
        return square(frequency=frequency, seconds=seconds, sample_rate=sample_rate, amplitude=amp)
    if kind == "saw":
        return saw(frequency=frequency, seconds=seconds, sample_rate=sample_rate, amplitude=amp)
    if kind == "impulse":
        return impulse(seconds=seconds, sample_rate=sample_rate, amplitude=amp)
    if kind == "clicks":
        return clicks(frequency=frequency, seconds=seconds, sample_rate=sample_rate, amplitude=amp)
    return sine(frequency=frequency, seconds=seconds, sample_rate=sample_rate, amplitude=amp)


def gain(samples: Iterable[float], amount: float) -> SampleBuffer:
    return [clamp(sample * amount) for sample in samples]


def lowpass(samples: Iterable[float], alpha: float = 0.16) -> SampleBuffer:
    out: SampleBuffer = []
    previous = 0.0
    for sample in samples:
        previous = previous + alpha * (sample - previous)
        out.append(previous)
    return out


def highpass(samples: Iterable[float], alpha: float = 0.92) -> SampleBuffer:
    out: SampleBuffer = []
    previous_input = 0.0
    previous_output = 0.0
    for sample in samples:
        value = alpha * (previous_output + sample - previous_input)
        out.append(value)
        previous_input = sample
        previous_output = value
    return out


def apply_effect(
    samples: Iterable[float],
    effect: str,
    *,
    gain_amount: float = 1.55,
    lowpass_alpha: float = 0.16,
    highpass_alpha: float = 0.92,
) -> SampleBuffer:
    data = list(samples)
    if effect == "gain":
        return gain(data, gain_amount)
    if effect == "lowpass":
        return lowpass(data, alpha=lowpass_alpha)
    if effect == "highpass":
        return highpass(data, alpha=highpass_alpha)
    return list(data)


def dft_magnitude(samples: Iterable[float], bins: int = 32) -> SampleBuffer:
    window = list(samples)[:256]
    if not window:
        return []
    size = len(window)
    magnitudes: SampleBuffer = []
    for k in range(min(bins, size)):
        real = 0.0
        imag = 0.0
        for n, sample in enumerate(window):
            angle = 2 * math.pi * k * n / size
            real += sample * math.cos(angle)
            imag -= sample * math.sin(angle)
        magnitudes.append(math.hypot(real, imag) / size)
    return magnitudes


def bin_frequency_hz(bin_index: int, window_size: int = 256, sample_rate: int = SAMPLE_RATE) -> float:
    return (bin_index * sample_rate) / window_size


def metrics(samples: Iterable[float]) -> dict[str, float]:
    data = list(samples)
    if not data:
        return {"peak": 0.0, "rms": 0.0, "mean": 0.0}
    peak = max(abs(sample) for sample in data)
    rms = math.sqrt(sum(sample * sample for sample in data) / len(data))
    mean = sum(data) / len(data)
    return {"peak": peak, "rms": rms, "mean": mean}


def write_wav(path: str, samples: Iterable[float], sample_rate: int = SAMPLE_RATE) -> None:
    with wave.open(path, "wb") as handle:
        handle.setnchannels(1)
        handle.setsampwidth(2)
        handle.setframerate(sample_rate)
        frames = b"".join(struct.pack("<h", int(clamp(sample) * 32767)) for sample in samples)
        handle.writeframes(frames)
