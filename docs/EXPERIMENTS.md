# Experimental methodology and interpretation

**Author: Vahab Khalili.**

## Comparable experiment protocol

For each modulation and FFT length, transmit **the same original bytes**, use a unit-average-energy constellation, define an identical occupied-bin allocation, use a fixed cyclic prefix ratio, inject complex AWGN based on **actual transmitted sample power**, record seed, preserve padding length, and report BER and EVM. Report the SNR definition explicitly; do not equate waveform sample SNR to Eb/N0 without accounting for symbol efficiency and CP/bin overhead.

## Metrics

- **BER**: mismatched source bits divided by original transmitted source bit count.
- **EVM**: RMS complex-symbol error normalized by transmitted symbol energy.
- **Image MAE/MSE/PSNR**: supplemental visual-fidelity metrics requiring known image shape and source bit order.
- **Stream latency**: output-valid delay plus converter/framing contributions (not equal to abstract transform stage count).
- **FPGA utilization / timing / power**: only report if underlying RTL, constraints, tool report and measurement procedure exist.

## Why nominal SNR may be misleading

An IFFT normalized by 1/N reduces time-sample signal power. Some historical MATLAB/Simulink examples configure a fixed-power AWGN block while varying N. In those cases the **actual** SNR changes and a BER-vs-N curve cannot be attributed solely to FFT size. The independent reference measures actual waveform power and scales complex noise accordingly.

## Why source quantization must be isolated

Mapping an 8-bit image channel to 2 or 4 significant bits before modulation causes irreversible reconstruction error even in a perfect link. QPSK and 16-QAM should instead both carry all original byte bits when testing communication fidelity. Record any deliberate rate-distortion case as a *separate* source-coding scenario.

## Finite-precision limitations

An `adc_bits` numerical setting only quantizes I and Q received samples. It does **not** make butterflies, twiddle multiplication, accumulation, FFT scaling and word growth bit-accurate. Nominal precision results from selected Simulink quantizers must be labeled partial finite-precision studies.

## Archived quantitative observations (not independently rerun)

One saved serial 16-QAM/16-point/nominal-14-bit experiment reports BER at 10/13/16 dB as 0.0584 / 0.01727 / 0.002459. At 10 dB, its nominal 12/14/16-bit conditions report BER 0.0585 / 0.0584 / 0.05838. These results are illustrative *historical report values*, not output of this repository's Python CI.

## Reproducibility gates

1. Check code environment and test seed.
2. Verify exact noiseless bit recovery.
3. Verify frame lengths and CP removal.
4. Confirm measured waveform power and generated AWGN variance.
5. Sweep SNR with sufficient independent frames and report uncertainty for BER.
6. Compare fixed-point against floating point with a defined arithmetic manifest.
7. Run serial RTL cosimulation before any hardware-resource assertion.
