# Scenario matrix and runbook

**Project author: Vahab Khalili.**

`VERIFIED` = deterministic numerical code and passing smoke checks. `ARCHIVED` = original MATLAB/Simulink material documented separately; historical results not automatically rerun. `DESIGN` = specified but not fully implemented as hardware here.

| ID | Scenario | Variables / representative configurations | Status |
|---|---|---|---|
| S01 | Source bit/byte reversibility | byte/bit order; RGB and grayscale | VERIFIED |
| S02 | Mapper/demapper identity | QPSK, 16-PSK, 16-QAM, optional 256-QAM | VERIFIED |
| S03 | Clean channel, all bins | FFT 16/32/64, CP N/4 | VERIFIED (9 primary combinations) |
| S04 | Clean channel, 48/64 active | 48 carriers, N=64, CP=16 | VERIFIED |
| S05 | Noise impact | sample SNR -5 to 20 dB; deterministic seed | VERIFIED model |
| S06 | Transform-size effect | N=16,32,64 with measured-power-normalized noise | VERIFIED model |
| S07 | Optional ADC quantization | explicit full scale, 8/12/14/16 bits | VERIFIED model; not full fixed-point FPGA |
| S08 | Source-quantized examples | 2-bit and 4-bit intensity levels | ARCHIVED lossy demonstrations |
| S09 | Serial radix-2 transform | butterfly, delays, coefficient scheduling, reorder | DESIGN + ARCHIVED models |
| S10 | Vector FFT baseline | Simulink vector transforms | ARCHIVED |
| S11 | Explicit RF I/Q | 40 MHz carrier; 5 MHz symbol-update parameter; 200 MHz simulation grid | ARCHIVED MATLAB |
| S12 | 48-of-64 cyclic-prefix framing | QPSK/16PSK/16QAM; 16-sample CP | VERIFIED numerical + ARCHIVED Simulink |
| S13 | Higher-order QAM | 256-QAM prototype | VERIFIED symbol/bit numerical + ARCHIVED prototype |
| S14 | 16-point FPGA transform | ISE component synthesis screenshot | HARDWARE-SCREENSHOT |

## Suggested executed smoke commands

```bash
python -m unittest discover -s tests -v
python -m ofdm_image.cli --modulation QPSK --nfft 16 --snr inf
python -m ofdm_image.cli --modulation 16QAM --nfft 64 --snr 12
python -m ofdm_image.cli --modulation 16PSK --nfft 32 --snr 8 --adc-bits 12
python -m ofdm_image.cli --modulation 16QAM --nfft 64 --active-bins 48 --cp 16 --snr inf
python -m ofdm_image.cli --modulation 256QAM --nfft 64 --snr inf
```

For actual raster data, install Pillow (`pip install Pillow`) and add `--image path/to/image.png`. The image is flattened into bytes without source precision loss and reconstructed after decoding.

## Archived model catalog

The organized standalone source package contains 42 primary Simulink models across four major groups: vector FFT/IFFT baseline; streaming radix-2 FFT; 48/64 cyclic-prefix framing; and experimental prototypes. Cases include modulation QPSK, 16-PSK, 16-QAM and prototypes with 256-QAM and other settings; selected serial models vary 12/14/16-bit quantization and transform sizes 16/32/64.

These original binary models cannot be validated by GitHub's CPU-only Python pipeline. Review [evidence register](EVIDENCE.md) before comparing or citing archived plots.
