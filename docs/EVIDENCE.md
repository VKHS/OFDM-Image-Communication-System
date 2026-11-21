# Evidence register, limitations and provenance

**Author: Vahab Khalili.**

This repository unifies the original project design while distinguishing what can presently be reproduced from what is known only from the supplied historical archive.

| Claim | Status | Evidence |
|---|---|---|
| Source bits roundtrip through mapper, IFFT, CP, FFT and demapper in ideal link | VERIFIED | `tests/test_smoke.py` |
| QPSK/16PSK/16QAM × FFT 16/32/64 at zero noise | VERIFIED | 9 integration subtests |
| 48/64 active-bin frame and CP removal | VERIFIED | Integration tests |
| Seeded complex-AWGN impairment with measured waveform power | VERIFIED numerical implementation | `ofdm_image/core.py` |
| Quantized received I/Q data | VERIFIED numerical implementation | Optional ADC quantizer |
| Historical vector and serial Simulink scenarios | ARCHIVED | Standalone consolidated source package |
| RF up/downconversion with held samples, filters and quadrature carriers | ARCHIVED | Historical MATLAB code |
| Serial FFT delay-feedback topology | DESIGN + ARCHIVED | `docs/STREAMING_FFT.md` and original models |
| 16-point FPGA resource use | HARDWARE-SCREENSHOT | Historical ISE screenshot only |
| Full FPGA transceiver implementation and physical RF transmission | NOT ESTABLISHED | No source-controlled full RTL or board log |
| Board-level FPGA timing and per-rail power consumption | NOT ESTABLISHED | No timing/power measurement report |

## Separation of datasets

- **Independent reference:** Python simulation in this repository, fresh synthetic input fixture or user-supplied images, reproducible seed.
- **Historical:** MATLAB/Simulink implementations, saved reconstructed images, selected figures and screenshots preserved in the separately supplied consolidated project archive.
- **Conceptual:** Architectural vector drawings, equations and proposed implementation details.

Historical files should not be silently claimed as re-executed. An archived PDF screenshot is not a source-level regression test. A figure with a conceptual streaming pipeline is not a schematic of placed-and-routed hardware.

## Limits of this GitHub copy

This initial GitHub tree includes original-project documentation, editable vector overview figures, runnable numerical code and CI. The large standalone MATLAB/Simulink/figure package is not implicitly imported into GitHub. In particular, it must not be described as version-controlled here until the corresponding files have actually been uploaded.

## Authorship

Sole author of the design and owner of this curated project: **Vahab Khalili**. This statement records the ownership requested by the project owner; code-generation and editorial processes are not represented as additional human project contributors.
