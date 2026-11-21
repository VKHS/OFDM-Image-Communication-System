# Verification results, interpretation and remaining gaps

## Independently verified in this package

The new Python complex-baseband reference produced **zero bit errors** in all 9 noiseless combinations of QPSK, 16-QAM and 16-PSK with FFT lengths 16, 32 and 64. It completed 45 seeded AWGN cases with an original 128x128 RGB test-array version and reported BER and EVM in `figures/reference_results/recomputed_ber_evm.csv`. The channel noise calculation is based on measured complex time-domain signal power.

At an actual 12 dB sample-domain SNR with N=64 in the newly computed experiment, the BER values are: QPSK 0.0000508626, 16-QAM 0.02477264, 16-PSK 0.06702677 (the latter two four bits/symbol; QPSK two bits/symbol). These numbers are **not** results reported by the archived source projects.

## Historical reported values reproduced descriptively

In a serial 16-QAM N=16 nominal-14-bit example, reported BER is 0.0584 at 10 dB, 0.01727 at 13 dB, and 0.002459 at 16 dB. Other reported nominal 12/14/16-bit cases at 10 dB show very similar BER (~0.0585/0.0584/0.05838). The original simulations were not rerun here.

## Important limitations

- Several early demonstrations discard low image bits before modulation, so their image damage is not solely a channel effect.
- Some FFT-size comparisons reuse fixed noise amplitude while IFFT output power changes; those comparisons do not isolate the effect of N at equal SNR.
- At least one nominal 12-bit converter demonstration uses model gain 8192 and quantizer step 620 (effective input-domain 0.07568), different from its written rationale.
- Some serial models quantize coefficients and external transform outputs while internal arithmetic remains inherited floating point. This is not complete fixed-point proof.
- Some scripts rely on additional MATLAB toolboxes or files, and some legacy converter paths are incomplete.
- A synthesis screenshot reports one 16-point FFT component and is insufficient to claim deployed whole-link resource/clock/power results.
- The newly authored MATLAB reference and historical models were not run in the current runtime.
- No uncited hardware or energy measurements were generated or inserted.

## Interpretation policy

Keep separate: (i) intended block architecture; (ii) original model settings; (iii) recorded screenshot results; (iv) new independent reference results; and (v) hardware measurements, which were not supplied.
