# Figure library

**Project author: Vahab Khalili.**

## Saved original results

- **[Complete historical Lena and OFDM result gallery — 80 images](../docs/HISTORICAL_RESULTS.md)**
- [Original image-output directory](historical/image_outputs)
- [80 original JPEG outputs and original BER curves](historical/image_outputs)
- [Six bundles containing 155 report-extracted figures](../archive)
- [Figure index, including all original media and formats](ARCHIVED_FIGURE_INDEX.csv)

## Detailed system and hardware diagrams

| Figure | Contents | Editable SVG |
|---|---|---|
| F01 | Full end-to-end OFDM image transceiver | [View](new_design/F01_complete_system.svg) |
| F02 | Four integrated design domains | [View](new_design/F02_four_design_domains.svg) |
| F03 | Serial radix-2 streaming FFT pipeline | [View](new_design/F03_serial_fft_pipeline.svg) |
| F04 | Butterfly and sample scheduling | [View](new_design/F04_butterfly_and_scheduling.svg) |
| F05 | Complex baseband versus quadrature RF | [View](new_design/F05_baseband_vs_rf.svg) |
| F06 | Image bytes, bits and modulation symbols | [View](new_design/F06_data_representation.svg) |
| F07 | Validation and evidence ladder | [View](new_design/F07_validation_ladder.svg) |
| F08 | Hardware claim/measurement limitations | [View](new_design/F08_limited_claims.svg) |
| F09 | QPSK, 16-PSK and 16-QAM constellations | [View](new_design/F09_constellations.svg) |
| F10 | OFDM framing and cyclic prefix | [View](new_design/F10_ofdm_framing.svg) |
| F11 | FFT stage delays | [View](new_design/F11_stage_delays.svg) |
| F12 | Historical reported BER redrawn as diagram | [View](new_design/F12_reported_ber.svg) |
| F13 | IFFT signal-power scaling | [View](new_design/F13_power_scaling.svg) |

Each numbered figure has a full-resolution PNG; original editable DOT and generation scripts are present where applicable.

## Independent numerical reference

- [BER versus SNR/FFT size](reference_results/reference_ber_by_fft.png)
- [Lena input and reference](reference_results/reference_input_used.png)
- [Reconstruction and constellation scatter](reference_results/reference_reconstruction_and_constellations.png)
- [Recomputed BER/EVM CSV](reference_results/recomputed_ber_evm.csv)

Historical figures are **ARCHIVED**, conceptual diagrams are **DESIGN**, and independently recomputed numerical figures are **VERIFIED REFERENCE**. None constitutes physical RF/FPGA measurement.