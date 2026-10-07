"""Q1 equations checked against hand-worked values (docs/equations.md)."""

import pytest

from hs3gpr import budget as b
from hs3gpr.params import load


def test_eq01_two_way_delay():
    assert b.two_way_delay(30e3) == pytest.approx(200.1e-6, rel=1e-3)
    assert b.two_way_delay(100e3) == pytest.approx(667.1e-6, rel=1e-3)


def test_eq01_eq02_depth_round_trip():
    dt = b.extra_delay(500.0, 7.0)
    assert dt == pytest.approx(8.83e-6, rel=1e-2)
    assert b.depth_from_delay(dt, 7.0) == pytest.approx(500.0)


def test_eq03_vertical_resolution():
    assert b.vertical_resolution(10e6) == pytest.approx(14.99, rel=1e-3)
    assert b.vertical_resolution(10e6, 7.0) == pytest.approx(5.67, rel=1e-2)


def test_eq04_attenuation_scales_with_frequency():
    a20 = b.attenuation_db_per_m(20e6, 7.0, 0.01)
    assert a20 == pytest.approx(0.0482, rel=1e-2)
    assert b.attenuation_db_per_m(40e6, 7.0, 0.01) == pytest.approx(2 * a20)


def test_eq05_roof_reflection():
    assert b.reflection_coefficient(7.0, 1.0) ** 2 == pytest.approx(0.204, abs=1e-3)


def test_eq07_galactic_noise_falls_with_frequency():
    assert b.galactic_noise_temperature(5e6) > b.galactic_noise_temperature(20e6) > b.galactic_noise_temperature(60e6)


def test_eq09_footprints():
    assert b.fresnel_zone_diameter(15.0, 50e3) == pytest.approx(1225, rel=1e-3)
    assert b.pulse_limited_diameter(50e3, 10e6) == pytest.approx(2449, rel=1e-3)


def test_eq12_moon_vs_leo_path_loss():
    extra = b.fspl_db(384_400e3, 8.4e9) - b.fspl_db(500e3, 8.4e9)
    assert extra == pytest.approx(57.7, abs=0.1)


def test_eq13_low_lunar_orbit():
    assert 1500 < b.ground_speed(50e3) < 1700
    assert 100 < b.orbital_period(50e3) / 60 < 125


def test_eq14_receive_window_blocking():
    # echo at ~330 µs: clear with PRF 1 kHz, blocked with PRF 3 kHz (next pulse lands on it)
    assert b.window_clear_of_transmit(1000, 330e-6, 40e-6, 50e-6, 5e-6)
    assert not b.window_clear_of_transmit(3000, 330e-6, 40e-6, 50e-6, 5e-6)


def test_budget_runs_on_current_register():
    rows = b.compute(load())
    assert rows
    assert all(r.check in ("ok", "fail", "needs", "") for r in rows)


def test_buried_echo_weakens_with_depth():
    s = b.snr_vs_depth(load(), [100, 300, 500])
    assert s[0] > s[1] > s[2]
