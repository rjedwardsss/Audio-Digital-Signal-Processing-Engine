from __future__ import annotations

import argparse

from .engine import (
    SAMPLE_RATE,
    apply_effect,
    bin_frequency_hz,
    dft_magnitude,
    generate_waveform,
    metrics,
    write_wav,
)

WAVEFORMS = ("sine", "square", "saw", "noise", "impulse", "clicks")
EFFECTS = ("none", "gain", "lowpass", "highpass")


def main() -> None:
    parser = argparse.ArgumentParser(description="Tiny stdlib audio DSP engine")
    parser.add_argument("--waveform", choices=WAVEFORMS, default="sine")
    parser.add_argument("--effect", choices=EFFECTS, default="lowpass")
    parser.add_argument("--frequency", type=float, default=440.0)
    parser.add_argument("--seconds", type=float, default=0.25)
    parser.add_argument("--sample-rate", type=int, default=SAMPLE_RATE)
    parser.add_argument("--gain", type=float, default=1.55)
    parser.add_argument("--lowpass-alpha", type=float, default=0.16)
    parser.add_argument("--highpass-alpha", type=float, default=0.92)
    parser.add_argument("--write-wav", metavar="PATH")
    args = parser.parse_args()

    source = generate_waveform(
        args.waveform,
        frequency=args.frequency,
        seconds=args.seconds,
        sample_rate=args.sample_rate,
    )
    processed = apply_effect(
        source,
        args.effect,
        gain_amount=args.gain,
        lowpass_alpha=args.lowpass_alpha,
        highpass_alpha=args.highpass_alpha,
    )
    stats = metrics(processed)
    spectrum = dft_magnitude(processed, bins=12)
    freqs = [bin_frequency_hz(i, sample_rate=args.sample_rate) for i in range(len(spectrum))]

    print(
        f"waveform={args.waveform} effect={args.effect} frequency={args.frequency} "
        f"samples={len(processed)} sample_rate={args.sample_rate}"
    )
    print(f"peak={stats['peak']:.4f} rms={stats['rms']:.4f} mean={stats['mean']:.4f}")
    print("spectrum=" + " ".join(f"{value:.3f}" for value in spectrum))
    print("bins_hz=" + " ".join(f"{value:.0f}" for value in freqs))

    if args.write_wav:
        write_wav(args.write_wav, processed, args.sample_rate)
        print(f"wrote={args.write_wav}")


if __name__ == "__main__":
    main()
