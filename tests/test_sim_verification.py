"""Simulation verification plan (q2-simulation/verification-plan.md).

V-01, V-02 and V-06 run now. V-03 and V-05 skip until the Q2 code they need exists,
then switch on by themselves. A skipped test prints what to build next.
"""

import numpy as np
import pytest

from hs3gpr import budget
from hs3gpr.params import load
from hs3gpr.sim import echo, ground, metrics, onboard, receiver, scene, waveform


def _requires(fn, *args, **kwargs):
    try:
        return fn(*args, **kwargs)
    except NotImplementedError as e:
        pytest.skip(str(e))


def test_V01_pulse_compression_gain_equals_TB():
    T, B = 50e-6, 10e6
    fs = B                                    # critically sampled → gain should be T·B = 500
    ref = waveform.chirp(T, B, fs)
    n, start, amp = 3000, 800, 0.05
    signal = np.zeros((1, n), complex)
    signal[0, start:start + len(ref)] = amp * ref
    noise = receiver.add_noise(np.zeros((400, n), complex), 1.0, np.random.default_rng(1))
    s_out = waveform.pulse_compress(signal, ref, "rect")
    n_out = waveform.pulse_compress(noise, ref, "rect")
    snr_in = amp ** 2 / 1.0
    valid = n - len(ref)                      # last len(ref) outputs see only part of the chirp
    snr_out = np.abs(s_out[0, start]) ** 2 / np.mean(np.abs(n_out[:, :valid]) ** 2)
    assert 10 * np.log10(snr_out / snr_in) == pytest.approx(10 * np.log10(T * B), abs=0.3)


def test_V02_presum_gain_equals_N():
    N, n = 16, 256
    signal = np.full((N * 50, n), 0.1 + 0.0j)
    noise = receiver.add_noise(np.zeros((N * 400, n), complex), 1.0, np.random.default_rng(2))
    s_out = onboard.presum(signal, N)
    n_out = onboard.presum(noise, N)
    gain = (np.abs(s_out[0, 0]) ** 2 / np.mean(np.abs(n_out) ** 2)) / (0.1 ** 2 / 1.0)
    assert 10 * np.log10(gain) == pytest.approx(10 * np.log10(N), abs=0.3)


def test_V03_sar_resolution_on_a_point_target():
    p = load()
    h = p["altitude_nominal"]
    spacing = budget.presummed_spacing(p["presum_factor"], budget.ground_speed(h), p["prf"])
    aperture = budget.synthetic_aperture_length(budget.wavelength(p["f_center"]), h, p["along_track_resolution_req"])
    x = np.arange(-aperture, aperture + spacing, spacing)
    traces, meta = _requires(echo.simulate_traces, scene.point_target_scene(0.0, 0.0), p, x, noise=False)
    compressed = ground.range_compress(traces, p, meta["fs"])
    x_out = np.arange(-1000.0, 1000.0, 5.0)
    image = _requires(ground.sar_focus, compressed, meta, p, x_out=x_out)
    i, j = np.unravel_index(np.argmax(np.abs(image)), image.shape)
    res = metrics.resolution_3db(image[:, j], 5.0)
    assert res == pytest.approx(p["along_track_resolution_req"], rel=0.35)


def test_V05_end_to_end_snr_matches_budget():
    p = load()
    depth = 300.0
    h = p["altitude_nominal"]
    spacing = budget.presummed_spacing(p["presum_factor"], budget.ground_speed(h), p["prf"])
    x = np.arange(-2000.0, 2000.0 + spacing, spacing)
    sc = scene.flat_scene(p, roof_depth=depth, void_width=4000.0)
    traces, meta = _requires(echo.simulate_traces, sc, p, x, rng=np.random.default_rng(3))
    compressed = ground.range_compress(traces, p, meta["fs"])
    image = _requires(ground.sar_focus, compressed, meta, p, x_out=np.array([0.0]))
    roof_delay = budget.two_way_delay(h) + budget.extra_delay(p["regolith_thickness"], p["eps_regolith"]) \
        + budget.extra_delay(depth - p["regolith_thickness"], p["eps_basalt"])
    k = int(round((roof_delay - meta["t0"][0]) * meta["fs"]))
    measured = metrics.snr_db(image[0], k, slice(-200, None))
    expected = budget.final_snr_db(p, depth)
    assert measured == pytest.approx(expected, abs=p["snr_tolerance"])


def test_V06_data_volume_matches_budget():
    p = load()
    n_samples = int(round(p["window_length"] * p["adc_sample_rate"]))
    one_second = np.zeros((int(p["prf"]), n_samples), complex)
    presummed = onboard.presum(one_second, p["presum_factor"])
    bits = presummed.shape[0] * presummed.shape[1] * p["requant_bits"]
    expected = budget.data_rate(p["prf"], n_samples, p["requant_bits"], p["presum_factor"])
    assert bits == pytest.approx(expected, rel=0.05)
