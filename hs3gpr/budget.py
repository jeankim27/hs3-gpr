"""Q1 budget: radar timing, resolution, propagation, SNR, data and power.

Every equation function names the EQ-ID it implements (see docs/equations.md).
All inputs come from the variable register; nothing is hard-coded here.

Command line
------------
    python -m hs3gpr.budget                          # print the budget
    python -m hs3gpr.budget --set f_center=5e6       # what-if without editing the file
    python -m hs3gpr.budget --markdown q1-baseline/BUDGET.md
    python -m hs3gpr.budget --json budget.json

In a notebook
-------------
    from hs3gpr.params import load
    from hs3gpr import budget
    p = load()
    budget.show(budget.compute(p))
"""

from __future__ import annotations

import argparse
import json
import math
import sys
from dataclasses import asdict, dataclass

import numpy as np

from .constants import C, EARTH_MOON_DISTANCE, GM_MOON, K_B, LEO_REFERENCE_RANGE, R_MOON, T0
from .params import MissingValue, Register, load

# =============================================================================
# Equations (pure functions, SI units)
# =============================================================================


def db(x):
    """Ratio → decibels."""
    return 10.0 * np.log10(x)


def from_db(x_db):
    """Decibels → ratio."""
    return 10.0 ** (np.asarray(x_db) / 10.0)


def wavelength(f):
    """Free-space wavelength λ = c / f."""
    return C / f


def two_way_delay(h):
    """EQ-01 · Round-trip time to a surface at range h: t = 2h / c."""
    return 2.0 * h / C


def extra_delay(d, eps):
    """EQ-01 · Extra round-trip time for depth d in a medium of permittivity eps: 2d√εr / c."""
    return 2.0 * d * np.sqrt(eps) / C


def depth_from_delay(dt, eps):
    """EQ-02 · Depth from delay after the surface echo: d = c·Δt / (2√εr)."""
    return C * dt / (2.0 * np.sqrt(eps))


def vertical_resolution(bandwidth, eps=1.0):
    """EQ-03 · Vertical (range) resolution δz = c / (2B√εr)."""
    return C / (2.0 * bandwidth * np.sqrt(eps))


def attenuation_db_per_m(f, eps, tan_delta):
    """EQ-04 · One-way power attenuation (dB/m), low-loss approximation:
    α ≈ 8.686 · π · √εr · tanδ / λ0."""
    return 8.686 * math.pi * np.sqrt(eps) * tan_delta * f / C


def reflection_coefficient(eps1, eps2):
    """EQ-05 · Normal-incidence amplitude reflection, medium 1 → medium 2:
    Γ = (√ε1 − √ε2) / (√ε1 + √ε2). Power reflection is Γ²."""
    a, b = np.sqrt(eps1), np.sqrt(eps2)
    return (a - b) / (a + b)


def specular_echo_power(p_t, gain_lin, lam, gamma2, r, loss_db=0.0):
    """EQ-06 · Received power from a flat (specular) reflector at effective range r:
    P_r = P_t·G²·λ²·Γ² / ((4π)²·(2r)²) × 10^(−loss/10)."""
    return (p_t * gain_lin ** 2 * lam ** 2 * gamma2
            / ((4.0 * math.pi) ** 2 * (2.0 * r) ** 2) * 10.0 ** (-loss_db / 10.0))


def galactic_noise_temperature(f):
    """EQ-07 · Galactic background noise temperature (K), ITU-R P.372 median:
    Fa = 52 − 23·log10(f / 1 MHz) dB above kT0B, so T = T0·10^(Fa/10).
    Approximation; verify against measured sky spectra for your band."""
    fa = 52.0 - 23.0 * np.log10(f / 1e6)
    return T0 * 10.0 ** (fa / 10.0)


def system_noise_temperature(f, antenna_efficiency, noise_figure_db, t_phys=T0):
    """EQ-07 · T_sys = η·T_gal + (1 − η)·T_phys + T0·(10^(NF/10) − 1)."""
    t_ant = antenna_efficiency * galactic_noise_temperature(f) + (1.0 - antenna_efficiency) * t_phys
    t_rx = T0 * (10.0 ** (noise_figure_db / 10.0) - 1.0)
    return t_ant + t_rx


def compressed_snr(p_r, chirp_length, t_sys):
    """EQ-08 · Single-pulse SNR after the matched filter: E/N0 = P_r·T / (k·T_sys).
    Equivalent to (P_r / kT_sysB) × T·B."""
    return p_r * chirp_length / (K_B * t_sys)


def fresnel_zone_diameter(lam, h):
    """EQ-09 · First Fresnel zone diameter √(2λh)."""
    return np.sqrt(2.0 * lam * h)


def pulse_limited_diameter(h, bandwidth):
    """EQ-09 · Pulse-limited footprint diameter 2√(h·c/B)."""
    return 2.0 * np.sqrt(h * C / bandwidth)


def synthetic_aperture_length(lam, h, dx):
    """EQ-09 · Synthetic aperture length for along-track resolution dx: L = λh / (2·dx)."""
    return lam * h / (2.0 * dx)


def presummed_spacing(n_presum, v_ground, prf):
    """EQ-10 · Along-track distance between presummed traces: N·v_g / PRF.
    Must not exceed the along-track resolution you want SAR to reach."""
    return n_presum * v_ground / prf


def data_rate(prf, n_samples, bits, n_presum=1):
    """EQ-11 · Data rate (bit/s) = PRF × samples per trace × bits / N."""
    return prf * n_samples * bits / n_presum


def fspl_db(r, f):
    """EQ-12 · Free-space path loss 20·log10(4πr/λ)."""
    return 20.0 * np.log10(4.0 * math.pi * r * f / C)


def orbital_speed(h):
    """EQ-13 · Circular orbital speed √(GM / (R + h))."""
    return np.sqrt(GM_MOON / (R_MOON + h))


def ground_speed(h):
    """EQ-13 · Speed of the nadir point over the surface: v·R / (R + h)."""
    return orbital_speed(h) * R_MOON / (R_MOON + h)


def orbital_period(h):
    """EQ-13 · Circular orbital period 2π·√((R + h)³ / GM)."""
    return 2.0 * math.pi * np.sqrt((R_MOON + h) ** 3 / GM_MOON)


def duty_cycle(chirp_length, prf):
    """EQ-14 · Fraction of time transmitting: T·PRF."""
    return chirp_length * prf


def window_clear_of_transmit(prf, t_open, t_len, chirp_length, t_recovery):
    """EQ-14 · True if the receive window [t_open, t_open + t_len] avoids every transmit
    interval [k/PRF, k/PRF + T + t_rec] (the receiver is deaf while transmitting)."""
    pri = 1.0 / prf
    t_close = t_open + t_len
    blocked = chirp_length + t_recovery
    k_first = math.floor(t_open / pri) - 1
    k_last = math.floor(t_close / pri) + 1
    for k in range(k_first, k_last + 1):
        tx_start, tx_end = k * pri, k * pri + blocked
        if t_open < tx_end and t_close > tx_start:
            return False
    return True


# =============================================================================
# Composite calculations used by the budget and the notebooks
# =============================================================================


def _column(p: Register, depth):
    """Regolith-over-basalt column: (depth in regolith, depth in basalt)."""
    t_reg = p.require("regolith_thickness")
    d_reg = min(depth, t_reg)
    return d_reg, max(0.0, depth - t_reg)


def single_pulse_snr_db(p: Register, depth=None, target="void_roof", h=None):
    """Single-pulse SNR (dB) after pulse compression.

    depth=None → the surface echo. Otherwise a flat buried reflector at `depth` (m) in a
    regolith-over-basalt column. target: "void_roof" (basalt → vacuum) or
    "basalt_layer" (regolith → basalt boundary strength, as a generic layer)."""
    f0, chirp, p_t = p.require("f_center", "chirp_length", "tx_peak_power")
    g_dbi, eta, nf = p.require("antenna_gain", "antenna_efficiency", "receiver_noise_figure")
    eps_r, eps_b = p.require("eps_regolith", "eps_basalt")
    h = p.require("altitude_nominal") if h is None else h
    lam = wavelength(f0)
    gain = 10.0 ** (g_dbi / 10.0) * eta
    t_sys = system_noise_temperature(f0, eta, nf)
    g_surface = reflection_coefficient(1.0, eps_r) ** 2
    if depth is None:
        p_r = specular_echo_power(p_t, gain, lam, g_surface, h)
        return float(db(compressed_snr(p_r, chirp, t_sys)))
    tan_r, tan_b = p.require("tan_delta_regolith", "tan_delta_basalt")
    d_reg, d_bas = _column(p, depth)
    g_rb = reflection_coefficient(eps_r, eps_b) ** 2 if d_bas > 0 else 0.0
    one_way_transmission = (1.0 - g_surface) * (1.0 - g_rb)
    if target == "void_roof":
        g_target = reflection_coefficient(eps_b if d_bas > 0 else eps_r, 1.0) ** 2
    elif target == "basalt_layer":
        g_target = reflection_coefficient(eps_r, eps_b) ** 2
    else:
        raise ValueError("target must be 'void_roof' or 'basalt_layer'")
    loss = 2.0 * (attenuation_db_per_m(f0, eps_r, tan_r) * d_reg
                  + attenuation_db_per_m(f0, eps_b, tan_b) * d_bas)
    r_eff = h + d_reg / math.sqrt(eps_r) + d_bas / math.sqrt(eps_b)
    p_r = specular_echo_power(p_t, gain, lam, g_target * one_way_transmission ** 2, r_eff)
    return float(db(compressed_snr(p_r, chirp, t_sys))) - loss   # subtract in dB: no underflow


def processing_gains_db(p: Register, h=None):
    """(pulse compression, presum, SAR) gains in dB, and M (traces combined by SAR)."""
    f0, bw, chirp = p.require("f_center", "bandwidth", "chirp_length")
    n, prf, dx = p.require("presum_factor", "prf", "along_track_resolution_req")
    h = p.require("altitude_nominal") if h is None else h
    spacing = presummed_spacing(n, ground_speed(h), prf)
    m = max(1, math.floor(synthetic_aperture_length(wavelength(f0), h, dx) / spacing))
    return float(db(chirp * bw)), float(db(n)), float(db(m)), m


def final_snr_db(p: Register, depth, target="void_roof", h=None):
    """SNR (dB) of a buried reflector after pulse compression, presumming, SAR and losses.
    (The pulse-compression gain is already inside the single-pulse SNR.)"""
    _, g_n, g_m, _ = processing_gains_db(p, h)
    return single_pulse_snr_db(p, depth, target, h) + g_n + g_m - p.require("system_losses")


def snr_vs_depth(p: Register, depths, target="void_roof", h=None):
    """Final SNR (dB) for an array of depths (m)."""
    return np.array([final_snr_db(p, float(d), target, h) for d in depths])


def max_detectable_depth(p: Register, snr_required_db=None, target="void_roof", h=None, d_limit=3000.0):
    """Deepest reflector (m) whose final SNR still meets the requirement.
    Returns 0 if even a shallow one fails, d_limit if everything down to d_limit passes."""
    req = p.require("snr_required") if snr_required_db is None else snr_required_db
    f = lambda d: final_snr_db(p, d, target, h) - req
    lo, hi = 1.0, d_limit
    if f(lo) < 0:
        return 0.0
    if f(hi) >= 0:
        return d_limit
    for _ in range(60):
        mid = 0.5 * (lo + hi)
        lo, hi = (mid, hi) if f(mid) >= 0 else (lo, mid)
    return lo


# =============================================================================
# The budget table
# =============================================================================


@dataclass
class Row:
    group: str
    label: str
    value: object          # number, text, or None when an input is TBD
    unit: str
    eq: str = ""
    check: str = ""        # "ok" | "fail" | "needs" | "" (information only)
    note: str = ""


def compute(p: Register) -> list[Row]:
    """Compute every budget row. Rows whose inputs are TBD say which inputs they need."""
    rows: list[Row] = []

    def add(group, label, unit, eq, fn, check=None, note=""):
        try:
            value = fn()
        except MissingValue as e:
            rows.append(Row(group, label, None, unit, eq, "needs", "needs " + ", ".join(e.keys)))
            return None
        status, msg = "", note
        if check is not None:
            try:
                status, msg = check(value)
            except MissingValue as e:
                status, msg = "needs", "to check, set " + ", ".join(e.keys)
        rows.append(Row(group, label, value, unit, eq, status, msg))
        return value

    def at_most(limit_key, scale=1.0, unit=""):
        def check(v):
            limit = p.require(limit_key) * scale
            return ("ok", f"limit {_fmt(limit)} {unit}".strip()) if v <= limit else \
                   ("fail", f"exceeds {limit_key} = {_fmt(limit)} {unit}".strip())
        return check

    def at_least(limit_key, scale=1.0, unit=""):
        def check(v):
            limit = p.require(limit_key) * scale
            return ("ok", f"margin {_fmt(v - limit)} {unit}".strip()) if v >= limit else \
                   ("fail", f"short by {_fmt(limit - v)} {unit}".strip())
        return check

    r = p.require
    G = "Timing"
    add(G, "Wavelength λ", "m", "λ = c/f0", lambda: wavelength(r("f_center")))
    add(G, "Surface echo delay, lowest altitude", "µs", "EQ-01", lambda: two_way_delay(r("altitude_min")) * 1e6)
    add(G, "Surface echo delay, nominal altitude", "µs", "EQ-01", lambda: two_way_delay(r("altitude_nominal")) * 1e6)
    add(G, "Surface echo delay, highest altitude", "µs", "EQ-01", lambda: two_way_delay(r("altitude_max")) * 1e6)
    add(G, "Extra delay to the deepest roof (basalt)", "µs", "EQ-01",
        lambda: extra_delay(r("roof_depth_max"), r("eps_basalt")) * 1e6)
    add(G, "Window length needed (margin + deepest roof)", "µs", "EQ-01",
        lambda: (r("window_margin") + extra_delay(r("roof_depth_max"), r("eps_basalt"))) * 1e6,
        check=at_most("window_length", 1e6, "µs"),
        note="")
    add(G, "Time available for the chirp at lowest altitude", "µs", "EQ-14",
        lambda: (two_way_delay(r("altitude_min")) - r("window_margin") - r("tr_recovery_time")) * 1e6,
        check=lambda v: ("ok", f"chirp is {_fmt(r('chirp_length') * 1e6)} µs") if r("chirp_length") * 1e6 <= v
        else ("fail", f"chirp ({_fmt(r('chirp_length') * 1e6)} µs) still transmitting when the echo arrives"))
    add(G, "Duty cycle", "%", "EQ-14", lambda: duty_cycle(r("chirp_length"), r("prf")) * 100)

    def blind_altitudes():
        prf, win, pre, chirp, rec = r("prf", "window_length", "window_margin", "chirp_length", "tr_recovery_time")
        hs = np.linspace(r("altitude_min"), r("altitude_max"), 400)
        bad = [h for h in hs if not window_clear_of_transmit(prf, two_way_delay(h) - pre, win, chirp, rec)]
        if not bad:
            return "clear at all altitudes"
        return f"blocked between {min(bad)/1e3:.0f} and {max(bad)/1e3:.0f} km"
    add(G, "Receive window vs transmit pulses", "", "EQ-14", blind_altitudes,
        check=lambda v: ("ok", "") if v.startswith("clear") else ("fail", "change PRF or plan around these altitudes"))

    G = "Resolution & footprint"
    add(G, "Vertical resolution, free space", "m", "EQ-03", lambda: vertical_resolution(r("bandwidth")))
    add(G, "Vertical resolution, regolith", "m", "EQ-03", lambda: vertical_resolution(r("bandwidth"), r("eps_regolith")))
    add(G, "Vertical resolution, basalt", "m", "EQ-03", lambda: vertical_resolution(r("bandwidth"), r("eps_basalt")),
        check=at_most("vertical_resolution_req", 1.0, "m"))
    add(G, "Fresnel zone diameter (nominal altitude)", "m", "EQ-09",
        lambda: fresnel_zone_diameter(wavelength(r("f_center")), r("altitude_nominal")))
    add(G, "Pulse-limited footprint (nominal altitude)", "m", "EQ-09",
        lambda: pulse_limited_diameter(r("altitude_nominal"), r("bandwidth")))
    add(G, "Synthetic aperture length for δx_req", "m", "EQ-09",
        lambda: synthetic_aperture_length(wavelength(r("f_center")), r("altitude_nominal"), r("along_track_resolution_req")))
    add(G, "Orbital period (nominal altitude)", "min", "EQ-13", lambda: orbital_period(r("altitude_nominal")) / 60)
    add(G, "Ground speed (nominal altitude)", "m/s", "EQ-13", lambda: ground_speed(r("altitude_nominal")))
    add(G, "Spacing between presummed traces", "m", "EQ-10",
        lambda: presummed_spacing(r("presum_factor"), ground_speed(r("altitude_nominal")), r("prf")),
        check=at_most("along_track_resolution_req", 1.0, "m"))
    add(G, "Traces combined by SAR, M", "-", "EQ-09", lambda: processing_gains_db(p)[3])
    add(G, "SAR aperture time", "s", "EQ-09",
        lambda: synthetic_aperture_length(wavelength(r("f_center")), r("altitude_nominal"), r("along_track_resolution_req"))
        / ground_speed(r("altitude_nominal")),
        note="the clock must stay coherent this long; see clock_stability")

    G = "Propagation"
    add(G, "Wave speed in regolith", "× c", "c/√εr", lambda: 1 / math.sqrt(r("eps_regolith")))
    add(G, "Wave speed in basalt", "× c", "c/√εr", lambda: 1 / math.sqrt(r("eps_basalt")))
    add(G, "Attenuation in regolith (one way)", "dB/m", "EQ-04",
        lambda: attenuation_db_per_m(r("f_center"), r("eps_regolith"), r("tan_delta_regolith")))
    add(G, "Attenuation in basalt (one way)", "dB/m", "EQ-04",
        lambda: attenuation_db_per_m(r("f_center"), r("eps_basalt"), r("tan_delta_basalt")))

    def two_way_loss():
        d_reg, d_bas = _column(p, r("roof_depth_max"))
        return 2 * (attenuation_db_per_m(r("f_center"), r("eps_regolith"), r("tan_delta_regolith")) * d_reg
                    + attenuation_db_per_m(r("f_center"), r("eps_basalt"), r("tan_delta_basalt")) * d_bas)
    add(G, "Two-way attenuation to the deepest roof", "dB", "EQ-04", two_way_loss)
    add(G, "Surface reflection (vacuum → regolith)", "dB", "EQ-05",
        lambda: db(reflection_coefficient(1.0, r("eps_regolith")) ** 2))
    add(G, "Layer reflection (regolith → basalt)", "dB", "EQ-05",
        lambda: db(reflection_coefficient(r("eps_regolith"), r("eps_basalt")) ** 2))
    add(G, "Roof reflection (basalt → void)", "dB", "EQ-05",
        lambda: db(reflection_coefficient(r("eps_basalt"), 1.0) ** 2))

    G = "Noise & SNR"
    add(G, "Galactic noise temperature at f0", "K", "EQ-07", lambda: galactic_noise_temperature(r("f_center")))
    add(G, "System noise temperature", "K", "EQ-07",
        lambda: system_noise_temperature(r("f_center"), r("antenna_efficiency"), r("receiver_noise_figure")))
    add(G, "Surface echo SNR, one pulse (compressed)", "dB", "EQ-06, EQ-08", lambda: single_pulse_snr_db(p))
    add(G, "Deepest roof SNR, one pulse (compressed)", "dB", "EQ-06, EQ-08",
        lambda: single_pulse_snr_db(p, r("roof_depth_max")))
    add(G, "Gain: pulse compression T·B", "dB", "EQ-08", lambda: processing_gains_db(p)[0],
        note="already included in the one-pulse rows")
    add(G, "Gain: presumming N", "dB", "EQ-08", lambda: processing_gains_db(p)[1])
    add(G, "Gain: SAR M", "dB", "EQ-08", lambda: processing_gains_db(p)[2])
    add(G, "Other losses", "dB", "", lambda: -r("system_losses"))
    add(G, "Deepest roof SNR after processing", "dB", "EQ-08",
        lambda: final_snr_db(p, r("roof_depth_max")), check=at_least("snr_required", 1.0, "dB"))
    add(G, "Deepest roof that meets SNR_req", "m", "EQ-08", lambda: max_detectable_depth(p),
        check=at_least("roof_depth_max", 1.0, "m"))
    add(G, "Surface-to-roof echo ratio (one pulse)", "dB", "",
        lambda: single_pulse_snr_db(p) - single_pulse_snr_db(p, r("roof_depth_max")),
        note="surface-echo sidelobes and ADC dynamic range must cope with this")

    G = "Data & downlink"
    add(G, "Samples per trace", "-", "", lambda: r("window_length") * r("adc_sample_rate"))
    add(G, "Raw data rate (no presum)", "Mbit/s", "EQ-11",
        lambda: data_rate(r("prf"), r("window_length") * r("adc_sample_rate"), r("adc_bits")) / 1e6)
    add(G, "Data rate after presum + requantization", "Mbit/s", "EQ-11",
        lambda: data_rate(r("prf"), r("window_length") * r("adc_sample_rate"), r("requant_bits"), r("presum_factor")) / 1e6)

    def bits_per_day():
        rate = data_rate(r("prf"), r("window_length") * r("adc_sample_rate"), r("requant_bits"), r("presum_factor"))
        return rate * r("obs_time_per_day")
    add(G, "Radar data per day", "MB", "EQ-11", lambda: bits_per_day() / 8e6)
    add(G, "Downlink rate needed to clear a day's data", "kbit/s", "EQ-11",
        lambda: bits_per_day() / r("contact_time_per_day") / 1e3,
        check=at_most("downlink_rate", 1e-3, "kbit/s"))
    add(G, "Memory needed for one day of data", "MB", "", lambda: bits_per_day() / 8e6,
        check=at_most("mass_memory", 1e-6, "MB"))
    add(G, "Path loss Moon → Earth at f_dl", "dB", "EQ-12", lambda: fspl_db(EARTH_MOON_DISTANCE, r("downlink_frequency")))
    add(G, "Extra path loss vs a 500 km LEO link", "dB", "EQ-12",
        lambda: fspl_db(EARTH_MOON_DISTANCE, r("downlink_frequency")) - fspl_db(LEO_REFERENCE_RANGE, r("downlink_frequency")))

    G = "Power"
    add(G, "Peak DC power during a pulse", "W", "EQ-15",
        lambda: r("radar_idle_power") + r("tx_peak_power") / r("pa_efficiency"),
        check=at_most("payload_power_peak", 1.0, "W"))
    add(G, "Average power while observing", "W", "EQ-15",
        lambda: r("radar_idle_power") + r("tx_peak_power") * duty_cycle(r("chirp_length"), r("prf")) / r("pa_efficiency"))
    add(G, "Radar power averaged over a day", "W", "EQ-15",
        lambda: (r("radar_idle_power") + r("tx_peak_power") * duty_cycle(r("chirp_length"), r("prf")) / r("pa_efficiency"))
        * r("obs_time_per_day") / 86400,
        check=at_most("payload_power_orbit_avg", 1.0, "W"))
    add(G, "Energy per day", "Wh", "EQ-15",
        lambda: (r("radar_idle_power") + r("tx_peak_power") * duty_cycle(r("chirp_length"), r("prf")) / r("pa_efficiency"))
        * r("obs_time_per_day") / 3600)
    add(G, "Energy drawn per pulse", "mJ", "EQ-15",
        lambda: r("tx_peak_power") * r("chirp_length") / r("pa_efficiency") * 1e3,
        note="sizes the capacitor bank")
    return rows


# =============================================================================
# Output: text, Markdown, JSON
# =============================================================================

GROUP_ORDER = ["Timing", "Resolution & footprint", "Propagation", "Noise & SNR", "Data & downlink", "Power"]
_ICON = {"ok": "✅", "fail": "❌", "needs": "⏳", "": ""}


def _fmt(v):
    if v is None:
        return "—"
    if isinstance(v, str):
        return v
    if isinstance(v, (int, np.integer)):
        return f"{int(v):,}"
    v = float(v)
    if v == 0:
        return "0"
    a = abs(v)
    if a >= 1000:
        return f"{v:,.0f}"
    if a >= 100:
        return f"{v:.0f}"
    if a >= 10:
        return f"{v:.1f}"
    if a >= 0.1:
        return f"{v:.2f}"
    return f"{v:.3g}"


def summary(rows):
    counts = {k: sum(1 for r in rows if r.check == k) for k in ("ok", "fail", "needs")}
    return counts


def to_markdown(rows, title="Q1 budget"):
    c = summary(rows)
    out = [f"# {title}", "",
           "Generated from [`params/variables.yaml`](../params/variables.yaml) by "
           "`python -m hs3gpr.budget --markdown q1-baseline/BUDGET.md`.",
           "**Don't edit this file by hand** — change the register and it regenerates. "
           "Equations: [docs/equations.md](../docs/equations.md).", "",
           f"**Checks:** ✅ {c['ok']} pass · ❌ {c['fail']} fail · ⏳ {c['needs']} need an input that is still TBD", ""]
    for group in GROUP_ORDER:
        group_rows = [r for r in rows if r.group == group]
        if not group_rows:
            continue
        out += [f"## {group}", "", "| Quantity | Value | Unit | Equation | Check |", "|---|---:|---|---|---|"]
        for r in group_rows:
            check = (_ICON[r.check] + " " + r.note).strip()
            out.append(f"| {r.label} | {_fmt(r.value)} | {r.unit} | {r.eq} | {check} |")
        out.append("")
    return "\n".join(out)


def to_text(rows):
    lines = []
    for group in GROUP_ORDER:
        group_rows = [r for r in rows if r.group == group]
        if not group_rows:
            continue
        lines.append(f"\n{group}\n" + "-" * len(group))
        for r in group_rows:
            mark = {"ok": "[ok]  ", "fail": "[FAIL]", "needs": "[TBD] ", "": "      "}[r.check]
            note = f"  ({r.note})" if r.note else ""
            lines.append(f"{mark} {r.label:<48} {_fmt(r.value):>14} {r.unit:<7}{note}")
    c = summary(rows)
    lines.append(f"\n{c['ok']} pass · {c['fail']} fail · {c['needs']} need inputs")
    return "\n".join(lines)


def to_json(rows):
    return {"summary": summary(rows),
            "groups": GROUP_ORDER,
            "rows": [dict(asdict(r), display=_fmt(r.value)) for r in rows]}


def show(rows, groups=None):
    """Pretty display in Jupyter (falls back to text)."""
    if groups:
        rows = [r for r in rows if r.group in groups]
    try:
        from IPython.display import Markdown, display
        display(Markdown(to_markdown(rows, title="Budget").split("\n", 5)[-1]))
    except ImportError:
        print(to_text(rows))


def _parse_set(items):
    changes = {}
    for item in items or []:
        key, _, raw = item.partition("=")
        try:
            value = float(raw)
        except ValueError:
            value = raw
        changes[key.strip()] = value
    return changes


def main(argv=None):
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except (AttributeError, ValueError):
        pass
    ap = argparse.ArgumentParser(description="HS-3 GPR budget from params/variables.yaml")
    ap.add_argument("--set", action="append", metavar="KEY=VALUE",
                    help="what-if change without editing the file (repeatable)")
    ap.add_argument("--markdown", metavar="PATH", help="write a Markdown table (e.g. q1-baseline/BUDGET.md)")
    ap.add_argument("--json", metavar="PATH", help="write JSON (used by the website)")
    args = ap.parse_args(argv)
    p = load()
    changes = _parse_set(args.set)
    if changes:
        p = p.with_values(**changes)
    rows = compute(p)
    if args.markdown:
        with open(args.markdown, "w", encoding="utf-8") as fh:
            fh.write(to_markdown(rows) + "\n")
    if args.json:
        with open(args.json, "w", encoding="utf-8") as fh:
            json.dump(to_json(rows), fh, ensure_ascii=False, indent=1)
    if not (args.markdown or args.json):
        print(to_text(rows))
    return 0


if __name__ == "__main__":
    sys.exit(main())
