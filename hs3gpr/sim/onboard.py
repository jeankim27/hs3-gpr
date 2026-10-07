"""Onboard processing (flowchart steps 14–15): presumming and requantization. Working reference code."""

from __future__ import annotations

import numpy as np

from .receiver import adc


def presum(traces: np.ndarray, n: int) -> np.ndarray:
    """Coherently add each group of `n` consecutive traces (EQ-08: SNR × n, data ÷ n).

    Leftover traces at the end that do not fill a group are dropped."""
    n = int(n)
    if n < 1:
        raise ValueError("presum factor must be ≥ 1")
    usable = (traces.shape[0] // n) * n
    return traces[:usable].reshape(-1, n, traces.shape[1]).sum(axis=1)


def presum_positions(x: np.ndarray, n: int) -> np.ndarray:
    """Along-track position of each presummed trace (mean of its group)."""
    usable = (len(x) // n) * n
    return np.asarray(x[:usable], float).reshape(-1, n).mean(axis=1)


def requantize(traces: np.ndarray, bits: int, full_scale=None) -> np.ndarray:
    """Reduce bits per sample before downlink (TS-3). Full scale defaults to the largest |I| or |Q|."""
    if full_scale is None:
        full_scale = float(np.max(np.abs(np.concatenate([traces.real.ravel(), traces.imag.ravel()])))) or 1.0
    return adc(traces, bits, full_scale)
