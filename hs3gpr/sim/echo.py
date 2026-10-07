"""Raw echo generator (flowchart steps 8–11). TODO (Q2, deliverable D2.3).

This is the heart of the simulation: for every trace position, add up the delayed,
attenuated chirps that come back from the surface, the layers, the voids and any point
targets. Build it in this order and run the tests after each step:

1. Point targets in vacuum (makes test V-03, SAR resolution, runnable):
       range r(x) = sqrt(h² + (x − x_t)²)  ·  delay τ = 2r / c
       echo = amplitude · chirp(t − τ) · exp(−j·4π·r/λ)        ← the phase SAR relies on
2. Flat interfaces at nadir (surface, regolith → basalt, void roof, void floor):
       delay from EQ-01 · amplitude from EQ-05/EQ-06 · two-way attenuation from EQ-04
3. Noise (receiver.add_noise) and ADC quantization (receiver.adc).
4. Q3: off-nadir surface facets from a LOLA elevation model → clutter.

Keep everything in complex baseband at p["sim_sample_rate"]. Return (traces, meta) as
described in hs3gpr/sim/__init__.py.
"""

from __future__ import annotations

import numpy as np


def simulate_traces(scene, p, x_positions, h=None, rng=None, noise=True):
    """Simulate raw (uncompressed) traces at along-track positions `x_positions` (m).

    Parameters
    ----------
    scene : hs3gpr.sim.scene.Scene
    p : hs3gpr.params.Register
    x_positions : 1-D array of along-track positions (m), one trace each (already presummed spacing)
    h : altitude (m); default p["altitude_nominal"]
    rng : numpy Generator for noise
    noise : add galactic + receiver noise if True

    Returns
    -------
    traces : complex ndarray (len(x_positions), n_samples)
    meta : dict(fs=..., t0=ndarray, x=ndarray, h=ndarray)
    """
    raise NotImplementedError("TODO (Q2, D2.3): see the module docstring in hs3gpr/sim/echo.py")
