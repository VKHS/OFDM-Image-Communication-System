"""Deterministic, reproducible complex-baseband image OFDM reference.

This is a numerical gold-standard path, NOT cycle-accurate RTL, RF hardware
capture, or a reconstruction of historical Simulink internal arithmetic.
All source bits are preserved unless the caller explicitly changes them.
"""
from __future__ import annotations
import numpy as np

ALPHABETS = {"QPSK": 4, "16PSK": 16, "16QAM": 16, "256QAM": 256}

def constellation(kind: str) -> np.ndarray:
    """Index-labelled, unit-average-energy complex constellation."""
    if kind not in ALPHABETS:
        raise ValueError(f"Unsupported constellation: {kind}")
    m = ALPHABETS[kind]
    if kind.endswith("PSK"):
        positions = np.arange(m, dtype=np.int64)
        labels = positions ^ (positions >> 1)
        c = np.empty(m, dtype=np.complex128)
        c[labels] = np.exp(2j * np.pi * positions / m + (1j * np.pi / 4 if m == 4 else 0))
        return c
    side = int(np.sqrt(m))
    if side * side != m:
        raise AssertionError("QAM requires square constellation")
    levels = np.arange(-(side - 1), side, 2, dtype=float)
    # Gray label each axis for adjacent level transitions.
    axis = np.empty(side)
    for i in range(side):
        label = i ^ (i >> 1)
        axis[label] = levels[i]
    c = np.array([axis[k // side] + 1j * axis[k % side] for k in range(m)])
    return c / np.sqrt(np.mean(np.abs(c) ** 2))

def bits_to_indices(bits: np.ndarray, bits_per_symbol: int) -> np.ndarray:
    b = np.asarray(bits, dtype=np.uint8).reshape(-1)
    if b.size % bits_per_symbol:
        raise ValueError("Input length must be a multiple of bits per symbol")
    if np.any(b > 1):
        raise ValueError("Bit values must be 0 or 1")
    w = 1 << np.arange(bits_per_symbol - 1, -1, -1)
    return (b.reshape(-1, bits_per_symbol) @ w).astype(np.int64)

def indices_to_bits(indices: np.ndarray, bits_per_symbol: int) -> np.ndarray:
    x = np.asarray(indices, dtype=np.int64).reshape(-1)
    return ((x[:, None] >> np.arange(bits_per_symbol - 1, -1, -1)) & 1).astype(np.uint8).reshape(-1)

def _quantize_complex(x: np.ndarray, bits: int, full_scale: float) -> np.ndarray:
    if bits < 2:
        raise ValueError("quantizer bits must be >=2")
    if full_scale <= 0:
        raise ValueError("full scale must be positive")
    levels = 2 ** (bits - 1) - 1
    def q(v):
        return np.clip(np.round(v / full_scale * levels), -levels, levels) * full_scale / levels
    return q(x.real) + 1j * q(x.imag)

def transmit_receive(
    bits: np.ndarray, modulation: str = "16QAM", nfft: int = 64,
    snr_db: float = float("inf"), seed: int = 1234,
    cp_len: int | None = None, active_bins: int | None = None,
    adc_bits: int | None = None, adc_full_scale: float | None = None,
) -> dict:
    """Map bits -> IFFT -> cyclic prefix -> measured-power AWGN -> FFT -> decisions.

    snr_db is waveform *sample* SNR, determined from the actual transmit power.
    This does not claim a particular Eb/N0 because cyclic-prefix overhead,
    active-bin ratio, and bit rate vary with configuration.
    """
    if nfft < 2 or nfft & (nfft - 1):
        raise ValueError("nfft must be a power of two")
    if modulation not in ALPHABETS:
        raise ValueError(f"Unsupported modulation: {modulation}")
    cp_len = nfft // 4 if cp_len is None else int(cp_len)
    if not 0 <= cp_len <= nfft:
        raise ValueError("cyclic prefix length must lie in [0,nfft]")
    active_bins = nfft if active_bins is None else int(active_bins)
    if not 1 <= active_bins <= nfft:
        raise ValueError("active_bins must lie in [1,nfft]")
    b = np.asarray(bits, dtype=np.uint8).reshape(-1)
    if b.size == 0 or np.any(b > 1):
        raise ValueError("bits must be a nonempty binary vector")
    bps = int(np.log2(ALPHABETS[modulation]))
    frame_bits = active_bins * bps
    padding = (-len(b)) % frame_bits
    padded = np.pad(b, (0, padding))
    c = constellation(modulation)
    data_indices = bits_to_indices(padded, bps).reshape(-1, active_bins)
    nframes = data_indices.shape[0]
    # Here active carriers occupy bins [0,active_bins). Other bins are zero.
    X = np.zeros((nframes, nfft), dtype=np.complex128)
    X[:, :active_bins] = c[data_indices]
    tx_baseband = np.fft.ifft(X, axis=1)
    tx = np.concatenate((tx_baseband[:, -cp_len:], tx_baseband), axis=1) if cp_len else tx_baseband
    power = float(np.mean(np.abs(tx) ** 2))
    if np.isinf(snr_db) and snr_db > 0:
        noise_power = 0.
    else:
        if not np.isfinite(snr_db):
            raise ValueError("snr_db must be finite or +inf")
        noise_power = power / (10. ** (snr_db / 10.))
    rng = np.random.default_rng(seed)
    noise = np.sqrt(noise_power / 2) * (rng.standard_normal(tx.shape) + 1j * rng.standard_normal(tx.shape))
    rx = tx + noise
    if adc_bits is not None:
        if adc_full_scale is None:
            # Scale calibrated from the clean TX signal, not the noisy sample max.
            adc_full_scale = 1.1 * float(max(np.max(np.abs(tx.real)), np.max(np.abs(tx.imag))))
        rx = _quantize_complex(rx, int(adc_bits), float(adc_full_scale))
    Y = np.fft.fft(rx[:, cp_len:] if cp_len else rx, axis=1)
    detected_carriers = Y[:, :active_bins].reshape(-1)
    distances = np.abs(detected_carriers[:, None] - c[None, :]) ** 2
    detected_indices = np.argmin(distances, axis=1)
    recovered_bits = indices_to_bits(detected_indices, bps)[: len(b)]
    ref_carriers = X[:, :active_bins].reshape(-1)
    ber = float(np.mean(b != recovered_bits))
    evm = float(np.sqrt(np.mean(np.abs(detected_carriers - ref_carriers) ** 2) /
                        np.mean(np.abs(ref_carriers) ** 2)))
    return dict(
        bits=recovered_bits, ber=ber, evm_rms=evm, frames=nframes,
        transmitted_bits=len(b), padding_bits=padding, modulation=modulation,
        nfft=nfft, active_bins=active_bins, cp_len=cp_len,
        sample_snr_db=float(snr_db), waveform_power=power,
        noise_power=noise_power,
    )
