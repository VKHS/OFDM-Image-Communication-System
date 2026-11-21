"""Run and report deterministic OFDM image-link scenarios."""
import argparse
import json
from pathlib import Path
import numpy as np
from .core import transmit_receive

def main(argv=None):
    p = argparse.ArgumentParser(description="OFDM image-link deterministic reference")
    p.add_argument("--modulation", choices=["QPSK", "16PSK", "16QAM", "256QAM"], default="16QAM")
    p.add_argument("--nfft", type=int, choices=[16, 32, 64], default=64)
    p.add_argument("--snr", type=float, default=12.0, help="Actual signal-power-based sample SNR, dB")
    p.add_argument("--seed", type=int, default=1234)
    p.add_argument("--cp", type=int, default=None)
    p.add_argument("--active-bins", type=int, default=None)
    p.add_argument("--adc-bits", type=int, default=None)
    p.add_argument("--image", type=Path, default=None, help="Optional grayscale/RGB image, requires Pillow")
    p.add_argument("--output", type=Path, default=None)
    args = p.parse_args(argv)
    if args.image:
        from PIL import Image
        image = np.asarray(Image.open(args.image).convert("RGB"), dtype=np.uint8)
    else:
        # Committed code contains a reproducible synthetic RGB test image:
        y, x = np.mgrid[0:32, 0:32]
        image = np.stack(((x*8) % 256, (y*8) % 256, ((x+y)*4) % 256), axis=-1).astype(np.uint8)
    bits = np.unpackbits(image.reshape(-1))
    result = transmit_receive(bits, args.modulation, args.nfft, args.snr, args.seed,
                              args.cp, args.active_bins, args.adc_bits)
    recovered = np.packbits(result.pop("bits")).reshape(image.shape)
    result["image_shape"] = list(image.shape)
    result["pixel_mae"] = float(np.mean(np.abs(image.astype(float)-recovered.astype(float))))
    result["exact_reconstruction"] = bool(np.array_equal(image, recovered))
    result["evidence"] = "independent_numerical_reference"
    payload = json.dumps(result, indent=2, allow_nan=True)
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(payload + "\n")
    print(payload)
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
