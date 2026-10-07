"""Receiver and digitizer models (flowchart steps 12–13)."""

from __future__ import annotations

import numpy as np

from ..constants import K_B


def noise_sigma(t_sys: float, fs: float) -> float:
    """RMS of complex noise per sample (√W) for system temperature t_sys over bandwidth fs."""
    return float(np.sqrt(K_B * t_sys * fs))


def add_noise(traces: np.ndarray, sigma: float, rng=None) -> np.ndarray:
    """Add circular complex Gaussian noise with total RMS `sigma` per sample."""
    rng = np.random.default_rng() if rng is None else rng
    noise = (rng.standard_normal(traces.shape) + 1j * rng.standard_normal(traces.shape)) * (sigma / np.sqrt(2))
    return traces + noise


def adc(traces: np.ndarray, bits: int, full_scale: float) -> np.ndarray:
    """Uniform quantizer on I and Q separately, clipping at ±full_scale."""
    step = 2.0 * full_scale / (2 ** bits)

    def q(x):
        return np.clip(np.round(x / step) * step, -full_scale, full_scale - step)

    return q(traces.real) + 1j * q(traces.imag)


def receiver_chain(traces, p, rng=None):
    """TODO (Q2, D2.3): gain plan → noise (EQ-07) → ADC with p["adc_bits"].

    Decide how full scale is set (e.g. surface echo + headroom) and record it in
    q2-simulation/interfaces.md."""
    raise NotImplementedError("TODO (Q2, D2.3): receiver gain plan and ADC full-scale choice")
