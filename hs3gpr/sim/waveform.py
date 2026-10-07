"""Chirp generation and pulse compression (flowchart steps 5 and 19). Working reference code."""

from __future__ import annotations

import numpy as np


def chirp(chirp_length: float, bandwidth: float, fs: float) -> np.ndarray:
    """Complex-baseband linear FM chirp sweeping −B/2 → +B/2 over `chirp_length` seconds.

    Returns unit-amplitude samples at rate fs (fs ≥ bandwidth for complex baseband)."""
    if fs < bandwidth:
        raise ValueError(f"fs ({fs:g} Hz) must be ≥ bandwidth ({bandwidth:g} Hz) for complex baseband")
    n = int(round(chirp_length * fs))
    t = np.arange(n) / fs
    k = bandwidth / chirp_length                      # sweep rate, Hz/s
    return np.exp(1j * np.pi * (k * t ** 2 - bandwidth * t))


def window(name: str, n: int) -> np.ndarray:
    """Amplitude weighting applied to the reference chirp ('rect', 'hann', 'hamming')."""
    name = (name or "rect").lower()
    if name in ("rect", "none", "rectangular"):
        return np.ones(n)
    if name == "hann":
        return np.hanning(n)
    if name == "hamming":
        return np.hamming(n)
    raise ValueError(f"unknown window '{name}'")


def pulse_compress(traces: np.ndarray, reference: np.ndarray, window_name: str = "hann") -> np.ndarray:
    """Matched-filter each trace (last axis) with the reference chirp (EQ-08).

    Output sample m is the correlation for an echo that *starts* at input sample m, so a
    chirp echo starting at sample m becomes a spike at m. Output length = input length.
    Normalized so the noise level is unchanged: the SNR gain is (Σw)² / Σw², which is T·B
    for a rectangular window sampled at fs = B (see compression_gain)."""
    traces = np.atleast_2d(traces)
    ref = reference * window(window_name, len(reference))
    n = traces.shape[-1]
    nfft = 1 << int(np.ceil(np.log2(n + len(ref))))
    spectrum = np.fft.fft(traces, nfft, axis=-1) * np.conj(np.fft.fft(ref, nfft))
    out = np.fft.ifft(spectrum, axis=-1)[..., :n]
    return out / np.sqrt(np.sum(np.abs(ref) ** 2))


def compression_gain(window_name: str, chirp_length: float, fs: float) -> float:
    """Expected SNR gain (linear) of pulse_compress, relative to the SNR of the raw samples.

    Equals T·fs for a rectangular window, i.e. T·B when sampling at fs = B; a Hann window
    gives about 2/3 of that (≈ 1.8 dB less)."""
    w = window(window_name, int(round(chirp_length * fs)))
    return float(np.sum(w) ** 2 / np.sum(w ** 2))
