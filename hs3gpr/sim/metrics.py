"""Measurements on simulated data (flowchart step 25)."""

from __future__ import annotations

import numpy as np


def snr_db(trace: np.ndarray, signal_index: int, noise_slice: slice) -> float:
    """SNR (dB) of the sample at `signal_index` against the mean noise power in `noise_slice`."""
    trace = np.asarray(trace)
    signal = np.abs(trace[signal_index]) ** 2
    noise = np.mean(np.abs(trace[noise_slice]) ** 2)
    return float(10 * np.log10(signal / noise))


def resolution_3db(profile: np.ndarray, spacing: float) -> float:
    """Width (in units of `spacing`) of the main lobe at half power (−3 dB) around the peak."""
    power = np.abs(np.asarray(profile)) ** 2
    peak = int(np.argmax(power))
    half = power[peak] / 2.0
    left = peak
    while left > 0 and power[left - 1] >= half:
        left -= 1
    right = peak
    while right < len(power) - 1 and power[right + 1] >= half:
        right += 1
    return (right - left + 1) * spacing


def detect(image, meta, p):
    """TODO (Q2): apply the detection rule (register: detection_rule) and return detections."""
    raise NotImplementedError("TODO (Q2): detection rule — record it in params/variables.yaml first")
