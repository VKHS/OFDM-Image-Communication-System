# Mathematical specification

**Author: Vahab Khalili.**

## Source serialization

Let `B` be the number of binary source bits. For an M-ary constellation, `m=log2(M)` bits select one complex symbol. Pad only the tail to a multiple of `mK` bits and record the number of padding bits.

## Constellation

A normalized M-PSK alphabet is `s_q = exp(j(2*pi*q/M+phi0))`. A normalized square M-QAM alphabet uses two independently mapped odd-integer axes with mean energy normalized to one. Transmitter and receiver must use the same index-to-symbol table. For equal-power comparisons, E[|s|^2]=1.

## OFDM transform

For frequency-domain bin `X[k]`, the transmitter computes

```text
x[n] = (1/N) * sum_{k=0}^{N-1} X[k] exp(+j 2pi k n/N).
```

After properly aligned reception and prefix removal:

```text
Y[k] = sum_{n=0}^{N-1} r[n] exp(-j 2pi k n/N).
```

The ideal clean-channel invariant is `FFT(IFFT(X))=X`.

## Active carriers and prefix

With K occupied bins of unit average constellation energy and unnormalized active symbols, the average useful-sample power is `K/N²` under NumPy/MATLAB IFFT normalization. Adding a prefix changes the finite-frame sample average depending on which samples it copies. For N=64, K=48: `K/N²=48/4096=0.01171875`.

## AWGN and reproducibility

For complex noise `w~CN(0,sigma²)`, where the desired **sample** SNR is `gamma` dB, the numerical reference uses:

```text
sigma² = mean(|transmitted_samples|²) / 10^(gamma/10)
w = sqrt(sigma²/2)*(normal_real + j*normal_imag)
```

The exact configured sample SNR is not automatically `Eb/N0`. Prefix, bin occupancy, and bits/symbol change the conversion.

## Hard decision, BER and EVM

```text
q_hat = argmin_q |Y - s_q|²
BER   = count(bit_tx != bit_rx)/number_of_source_bits
EVM   = sqrt(sum(|Y-X|²)/sum(|X|²))
```

Align both bit streams and exclude original tail padding from BER.

## Selected finite precision

A real quantizer can be written `Q(x)=Delta*round(x/Delta)` within an explicitly specified clipping range. Complete FPGA fixed-point equivalence additionally requires signedness, integer/fraction widths, intermediate product width, rounding and overflow rules; source-level nominal “12/14/16 bits” alone does not establish these.

## Streaming IFFT reuse

```text
IFFT(X) = (1/N) * conj(FFT(conj(X)))
```

This reuses butterfly structure but still requires appropriate coefficients, conjugation, output order, and scaling.

## Cyclic prefix

The transmitted sequence is `[x[N-L],...,x[N-1], x[0],...,x[N-1]]`. For N=64 and L=16, it consists of 80 *complex samples*, not 80 bits.
