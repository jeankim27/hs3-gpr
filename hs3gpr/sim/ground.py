"""Ground processing (flowchart steps 18–24)."""

from __future__ import annotations

import numpy as np

from ..budget import depth_from_delay
from . import waveform


def range_compress(traces: np.ndarray, p, fs=None) -> np.ndarray:
    """Step 19: matched filter with the reference chirp, using the register's waveform settings.
    (In flight data the reference comes from the calibration loopback.)"""
    fs = fs or p["sim_sample_rate"]
    ref = waveform.chirp(p["chirp_length"], p["bandwidth"], fs)
    return waveform.pulse_compress(traces, ref, p["range_window"])


def sar_focus(compressed: np.ndarray, meta: dict, p, x_out=None) -> np.ndarray:
    """Step 21: SAR focusing. TODO (Q2, deliverable D2.5).

    Suggested method (back-projection, see cumming2005):
      for each output position x0 and each depth sample:
        1. find the traces within ±L/2 of x0 (L from EQ-09 for along_track_resolution_req)
        2. for each trace, compute the two-way delay to the point (x0, depth) and read the
           compressed trace at that delay (interpolate)
        3. multiply by exp(+j·4π·r/λ) to undo the propagation phase
        4. add them up
    Start with a point target in vacuum (test V-03), then layers, then the void.

    Returns a focused complex image with shape (len(x_out), n_samples)."""
    raise NotImplementedError("TODO (Q2, D2.5): SAR back-projection — see the docstring in hs3gpr/sim/ground.py")


def multilook(image: np.ndarray, looks: int) -> np.ndarray:
    """Step 22: average the power of each group of `looks` neighboring traces."""
    looks = int(looks)
    usable = (image.shape[0] // looks) * looks
    power = np.abs(image[:usable]) ** 2
    return power.reshape(-1, looks, image.shape[1]).mean(axis=1)


def time_to_depth(delay_after_surface: np.ndarray, eps: float) -> np.ndarray:
    """Step 24: convert delay after the surface echo (s) to depth (m) with EQ-02."""
    return depth_from_delay(np.asarray(delay_after_surface, float), eps)
