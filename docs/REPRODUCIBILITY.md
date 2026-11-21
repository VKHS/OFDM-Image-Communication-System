# Reproducible execution and scenario sweep

**Project author: Vahab Khalili.**

## Environment

Use Python 3.10 or newer with NumPy. No MATLAB license is required for the numerical reference.

```bash
git clone https://github.com/VKHS/OFDM-Image-Communication-System.git
cd OFDM-Image-Communication-System
python -m venv .venv
source .venv/bin/activate
python -m pip install -e .
python -m unittest discover -s tests -v
```

## Recompute the 45-case AWGN matrix

```bash
python -m ofdm_image.sweep --output results/sweep.csv --bytes 512 --seed 1234
```

The sweep covers QPSK, 16-PSK, 16-QAM × FFT 16, 32, 64 × waveform sample SNR 4, 8, 12, 16, 20 dB. It holds the *source bits* fixed, uses deterministic AWGN and power-aware noise calibration, and records both BER and EVM, wave power, noise power, active bins, prefix, bit count, and seed.

The 512-byte default fixture is intentionally tiny for CI. Small BER samples have large uncertainty; research-grade BER estimation requires orders of magnitude more transmitted bits and confidence intervals.

## Run an image example

```bash
pip install Pillow
python -m ofdm_image.cli --image path/to/image.png --modulation 16QAM --nfft 64 --snr 12 --output results/image_example.json
```

The JSON reports whether the reconstructed bits recreate the image exactly and its image-channel MAE. Image plots can be generated separately; no historical reconstructed image is claimed to come from this code.

## Reproducibility distinctions

The Python core deliberately implements a **floating-point FFT numerical reference**, not the archived Simulink models, bit-accurate FPGA arithmetic, DAC/ADC physical transfer characteristics or a cycle-accurate serial butterfly. Dedicated tests for those levels require source assets and tools not present in the GitHub text-only core.

See [scenario matrix](SCENARIOS.md) and [evidence register](EVIDENCE.md).
