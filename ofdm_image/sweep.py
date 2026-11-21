"""Run a reproducible OFDM scenario grid; output numerical evidence as CSV.

No external datasets or plotting dependencies are required. The generated CSV
contains freshly computed reference values, never historical MATLAB results.
"""
from __future__ import annotations
import argparse
import csv
from pathlib import Path
import numpy as np
from .core import transmit_receive

def sweep_csv(output: Path, *, byte_count: int = 512, seed: int = 1234) -> list[dict]:
    if byte_count < 1:
        raise ValueError("byte_count must be positive")
    # Explicit seeded byte fixture; same source bitstream for every case.
    rng = np.random.default_rng(seed)
    bits = np.unpackbits(rng.integers(0, 256, size=byte_count, dtype=np.uint8))
    records = []
    for mode in ("QPSK", "16PSK", "16QAM"):
        for nfft in (16, 32, 64):
            for snr in (4, 8, 12, 16, 20):
                r = transmit_receive(bits, mode, nfft, snr, seed=seed,
                                     cp_len=nfft//4)
                records.append(dict(
                    modulation=mode, nfft=nfft, sample_snr_db=snr,
                    active_bins=nfft, cp_len=nfft//4,
                    ber=f"{r['ber']:.12g}",
                    evm_rms=f"{r['evm_rms']:.12g}",
                    waveform_power=f"{r['waveform_power']:.12g}",
                    noise_power=f"{r['noise_power']:.12g}",
                    source_bits=len(bits), seed=seed,
                    evidence="independent_numerical_reference"
                ))
    output.parent.mkdir(parents=True, exist_ok=True)
    with output.open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=list(records[0]))
        w.writeheader()
        w.writerows(records)
    return records

def main(argv=None):
    p = argparse.ArgumentParser()
    p.add_argument("--output", type=Path, default=Path("results/sweep.csv"))
    p.add_argument("--bytes", type=int, default=512, dest="byte_count")
    p.add_argument("--seed", type=int, default=1234)
    args = p.parse_args(argv)
    records = sweep_csv(args.output, byte_count=args.byte_count, seed=args.seed)
    print(f"Computed {len(records)} seeded, measured-power-normalized AWGN cases at {args.output}")

if __name__ == "__main__":
    main()
