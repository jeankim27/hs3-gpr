# Variable register

> Generated from [`variables.yaml`](variables.yaml) by `python tools/register.py`. **Edit `variables.yaml`, not this file.** It is regenerated automatically when changes land on `main`.

Status: 🔴 **TBD** no value yet · 🟡 **assumed** placeholder, needs a source or trade · 🔵 **derived** backed by an analysis · 🟢 **frozen** agreed baseline (change only with a decision record)

## Progress

| Quarter | Variables | 🔴 TBD | 🟡 Assumed | 🔵 Derived | 🟢 Frozen | Pinned down (derived + frozen) |
|---|---:|---:|---:|---:|---:|---|
| [Q1](#q1) | 58 | 18 | 40 | 0 | 0 | □□□□□□□□□□ 0% |
| [Q2](#q2) | 8 | 1 | 7 | 0 | 0 | □□□□□□□□□□ 0% |
| [Q3](#q3) | 5 | 2 | 3 | 0 | 0 | □□□□□□□□□□ 0% |

### Q1 variables still TBD, by owner

- **comms** (1): `downlink_rate`
- **eps** (2): `payload_power_orbit_avg`, `payload_power_peak`
- **gnc** (4): `inclination`, `orbit_knowledge_error`, `attitude_knowledge_error`, `pointing_accuracy`
- **radar-hw** (2): `clock_stability`, `dynamic_range_required`
- **scene** (1): `surface_rms_slope`
- **structures** (2): `payload_mass`, `payload_volume`
- **systems** (6): `tube_height_min`, `tube_width_min`, `vertical_resolution_req`, `passes_per_site`, `bus_emi_limit`, `mass_memory`

<a id="q1"></a>
## Q1 · pin down by week 10

### Requirements & target

| Variable | Symbol | Value | Range considered | Status | Owner | Source |
|---|---|---|---|---|---|---|
| **Deepest lava-tube roof to detect**<br>`roof_depth_max` | d_max | 500 m | 100 m – 1 km | 🟡 assumed | systems | team (mission assumption) |
| **Smallest tube height to detect**<br>`tube_height_min` | h_tube | TBD | 20 m – 200 m | 🔴 TBD | systems | literature on lunar lava-tube sizes |
| **Smallest tube width to detect**<br>`tube_width_min` | w_tube | TBD | 50 m – 1 km | 🔴 TBD | systems | literature on lunar lava-tube sizes |
| **SNR needed after processing to call a detection**<br>`snr_required` | SNR_req | 10 dB | 6 dB – 15 dB | 🟡 assumed | systems | team; refine with the detection analysis in Q2 |
| **Required vertical resolution (in basalt)**<br>`vertical_resolution_req` | δz_req | TBD | 5 m – 50 m | 🔴 TBD | systems | derive from tube_height_min |
| **Required along-track resolution**<br>`along_track_resolution_req` | δx_req | 250 m | 100 m – 1 km | 🟡 assumed | systems | team; derive from tube_width_min |
| **Target sites**<br>`target_sites` |  | Marius Hills Hole, Mare Tranquillitatis Hole, Mare Ingenii Hole |  | 🟡 assumed | systems | kaku2017; haruyama2009 |
| **Passes over each site**<br>`passes_per_site` |  | TBD | 1 – 10 | 🔴 TBD | systems | observation plan |

### Lunar environment

| Variable | Symbol | Value | Range considered | Status | Owner | Source |
|---|---|---|---|---|---|---|
| **Relative permittivity, regolith**<br>`eps_regolith` | ε_reg | 2.7 | 2.3 – 3.5 | 🟡 assumed | scene | olhoeft1975 (εr ≈ 1.919^ρ with ρ ≈ 1.5 g/cm³) |
| **Relative permittivity, solid mare basalt**<br>`eps_basalt` | ε_bas | 7 | 5.5 – 9 | 🟡 assumed | scene | olhoeft1975 (ρ ≈ 3.0 g/cm³) |
| **Loss tangent, regolith**<br>`tan_delta_regolith` | tanδ_reg | 0.005 | 0.001 – 0.03 | 🟡 assumed | scene | heiken1991 (RESEARCH NEEDED) |
| **Loss tangent, mare basalt**<br>`tan_delta_basalt` | tanδ_bas | 0.01 | 0.003 – 0.06 | 🟡 assumed | scene | heiken1991; ono2009 (RESEARCH NEEDED) |
| **Regolith thickness (mare)**<br>`regolith_thickness` | t_reg | 5 m | 2 m – 15 m | 🟡 assumed | scene | heiken1991 (verify) |
| **Surface RMS slope at wavelength scale**<br>`surface_rms_slope` | s_rms | TBD | 1 deg – 10 deg | 🔴 TBD | scene | LRO LOLA data |
| **Elevation model for clutter simulation**<br>`dem_source` |  | LRO LOLA (resolution TBD) |  | 🟡 assumed | scene | team |
| **Galactic noise model**<br>`galactic_noise_model` |  | ITU-R P.372: Fa = 52 − 23·log10(f / 1 MHz) dB above kT0B |  | 🟡 assumed | scene | itur_p372 (verify against measured sky spectra) |
| **Ionosphere correction needed?**<br>`ionosphere_correction` |  | not planned (assumed negligible at the Moon; verify) |  | 🟡 assumed | scene | team |

### Orbit & spacecraft

| Variable | Symbol | Value | Range considered | Status | Owner | Source |
|---|---|---|---|---|---|---|
| **Nominal altitude**<br>`altitude_nominal` | h | 50 km | 30 km – 100 km | 🟡 assumed | gnc | team (mission assumption) |
| **Lowest altitude**<br>`altitude_min` | h_min | 30 km |  | 🟡 assumed | gnc | team (mission assumption) |
| **Highest altitude**<br>`altitude_max` | h_max | 100 km |  | 🟡 assumed | gnc | team (mission assumption) |
| **Orbit inclination**<br>`inclination` | i | TBD | 0 deg – 90 deg | 🔴 TBD | gnc | GNC team |
| **Position knowledge error (1σ)**<br>`orbit_knowledge_error` | σ_pos | TBD | 1 m – 1 km | 🔴 TBD | gnc | FOUND + ground tracking |
| **Attitude knowledge error (1σ)**<br>`attitude_knowledge_error` | σ_att | TBD | 0.01 deg – 1 deg | 🔴 TBD | gnc | LOST / ADCS team |
| **Antenna pointing accuracy**<br>`pointing_accuracy` |  | TBD | 0.5 deg – 10 deg | 🔴 TBD | gnc | ADCS team |
| **Orbit-average power available to the radar**<br>`payload_power_orbit_avg` | P_avail | TBD | 2 W – 30 W | 🔴 TBD | eps | EPS team |
| **Peak power available to the radar**<br>`payload_power_peak` | P_peak_avail | TBD | 10 W – 100 W | 🔴 TBD | eps | EPS team |
| **Mass allocation (radar + antenna)**<br>`payload_mass` |  | TBD | 1 kg – 5 kg | 🔴 TBD | structures | structures team |
| **Stowed volume allocation (radar + antenna)**<br>`payload_volume` |  | TBD | 1 U – 4 U | 🔴 TBD | structures | structures team |
| **Allowed spacecraft self-noise in the radar band**<br>`bus_emi_limit` |  | TBD |  | 🔴 TBD | systems | team |

### Waveform & timing

| Variable | Symbol | Value | Range considered | Status | Owner | Source |
|---|---|---|---|---|---|---|
| **Center frequency**<br>`f_center` | f0 | 20 MHz | 5 MHz – 60 MHz | 🟡 assumed | radar-hw | TS-1 (open) |
| **Chirp bandwidth**<br>`bandwidth` | B | 10 MHz | 1 MHz – 20 MHz | 🟡 assumed | radar-hw | TS-1 (open) |
| **Chirp length**<br>`chirp_length` | T | 50 µs | 10 µs – 150 µs | 🟡 assumed | radar-hw | EQ-08, EQ-14 |
| **Pulse repetition frequency**<br>`prf` | PRF | 1 kHz | 100 Hz – 3 kHz | 🟡 assumed | radar-hw | EQ-10, EQ-14 |
| **Receive window length**<br>`window_length` | t_win | 40 µs | 15 µs – 100 µs | 🟡 assumed | radar-hw | EQ-01 + terrain margin |
| **Window opens this early before the predicted surface echo**<br>`window_margin` | t_pre | 5 µs | 1 µs – 20 µs | 🟡 assumed | radar-hw | altitude-prediction error (GNC) |
| **T/R switch and receiver recovery time**<br>`tr_recovery_time` | t_rec | 5 µs | 1 µs – 20 µs | 🟡 assumed | radar-hw | parts (TBD) |
| **Pulse-compression window function**<br>`range_window` |  | hann |  | 🟡 assumed | processing | EQ-08 note |

### Radar hardware

| Variable | Symbol | Value | Range considered | Status | Owner | Source |
|---|---|---|---|---|---|---|
| **Transmit peak power (RF)**<br>`tx_peak_power` | P_t | 10 W | 2 W – 100 W | 🟡 assumed | radar-hw | trade with EPS; SHARAD transmits 10 W (seu2007) |
| **Power amplifier efficiency (DC → RF)**<br>`pa_efficiency` | η_PA | 0.4 | 0.2 – 0.7 | 🟡 assumed | radar-hw | parts (TBD) |
| **Radar electronics power while on (excluding the amplifier)**<br>`radar_idle_power` | P_idle | 5 W | 2 W – 15 W | 🟡 assumed | radar-hw | parts (TBD) |
| **Antenna type**<br>`antenna_type` |  | half-wave dipole, deployable |  | 🟡 assumed | radar-hw | TS-2 (open) |
| **Antenna tip-to-tip length**<br>`antenna_length` | L_ant | 7.5 m | 2 m – 30 m | 🟡 assumed | radar-hw | TS-2 (open); half-wave = c / (2 f0) |
| **Antenna gain**<br>`antenna_gain` | G | 2.15 dBi | 0 dBi – 3 dBi | 🟡 assumed | radar-hw | half-wave dipole textbook value |
| **Antenna radiation efficiency**<br>`antenna_efficiency` | η_ant | 0.7 | 0.2 – 0.95 | 🟡 assumed | radar-hw | team estimate |
| **Receiver noise figure**<br>`receiver_noise_figure` | NF | 3 dB | 1 dB – 8 dB | 🟡 assumed | radar-hw | parts (TBD) |
| **ADC resolution**<br>`adc_bits` | n_ADC | 12 bit | 8 bit – 16 bit | 🟡 assumed | radar-hw | parts (TBD) |
| **ADC sample rate**<br>`adc_sample_rate` | f_s | 50 MHz | 20 MHz – 250 MHz | 🟡 assumed | radar-hw | parts (TBD) |
| **Sampling architecture**<br>`sampling_architecture` |  | direct RF sampling |  | 🟡 assumed | radar-hw | trade (open) |
| **Clock phase stability needed over the SAR aperture time**<br>`clock_stability` |  | TBD |  | 🔴 TBD | radar-hw | SAR phase-error budget |
| **Dynamic range, surface echo vs deepest buried echo**<br>`dynamic_range_required` |  | TBD |  | 🔴 TBD | radar-hw | BUDGET.md (surface vs buried SNR) |

### Data & downlink

| Variable | Symbol | Value | Range considered | Status | Owner | Source |
|---|---|---|---|---|---|---|
| **Presum factor**<br>`presum_factor` | N | 16 | 1 – 64 | 🟡 assumed | processing | TS-3 (open) |
| **Bits per sample after presumming**<br>`requant_bits` | n_req | 8 bit | 4 bit – 16 bit | 🟡 assumed | processing | TS-3 (open) |
| **Radar observing time per day**<br>`obs_time_per_day` | t_obs | 1.8 ks | 300 s – 7.2 ks | 🟡 assumed | systems | observation plan |
| **Ground-contact time per day for radar data**<br>`contact_time_per_day` | t_contact | 14.4 ks | 3.6 ks – 43.2 ks | 🟡 assumed | comms | comms team (placeholder) |
| **Downlink data rate available for radar data**<br>`downlink_rate` | R_dl | TBD | 1 kbit/s – 1 Mbit/s | 🔴 TBD | comms | comms link budget |
| **Downlink frequency**<br>`downlink_frequency` | f_dl | 8.4 GHz | 2 GHz – 8.5 GHz | 🟡 assumed | comms | comms team (X-band placeholder) |
| **Onboard memory available for radar data**<br>`mass_memory` |  | TBD | 1 GB – 64 GB | 🔴 TBD | systems | C&DH team |

### Processing

| Variable | Symbol | Value | Range considered | Status | Owner | Source |
|---|---|---|---|---|---|---|
| **Other losses (window, roughness, pointing, implementation)**<br>`system_losses` | L_sys | 3 dB | 1 dB – 10 dB | 🟡 assumed | processing | team estimate |

<a id="q2"></a>
## Q2 · pin down by week 20

### Processing

| Variable | Symbol | Value | Range considered | Status | Owner | Source |
|---|---|---|---|---|---|---|
| **Multilook count**<br>`multilook_count` | L | 4 | 1 – 16 | 🟡 assumed | processing | team |
| **SAR focusing algorithm**<br>`sar_algorithm` |  | back-projection |  | 🟡 assumed | processing | cumming2005 |
| **Detection rule**<br>`detection_rule` |  | TBD |  | 🔴 TBD | processing | Q2 detection analysis |

### Simulation

| Variable | Symbol | Value | Range considered | Status | Owner | Source |
|---|---|---|---|---|---|---|
| **Simulation complex sample rate**<br>`sim_sample_rate` |  | 20 MHz | 10 MHz – 100 MHz | 🟡 assumed | processing | team (must be ≥ bandwidth) |
| **Simulated along-track distance**<br>`sim_track_length` |  | 20 km | 5 km – 100 km | 🟡 assumed | processing | team |
| **How the void is modeled**<br>`void_model` |  | two flat interfaces (roof, floor) with vacuum between |  | 🟡 assumed | scene | team |
| **Allowed difference between simulated and budget SNR**<br>`snr_tolerance` |  | 2 dB | 0.5 dB – 3 dB | 🟡 assumed | systems | verification plan |
| **Trace data format between modules**<br>`trace_format` |  | complex array [n_traces, n_samples] + metadata dict (t0, fs, x, h) |  | 🟡 assumed | processing | q2-simulation/interfaces.md |

<a id="q3"></a>
## Q3 · pin down by week 30

### Realism & analysis

| Variable | Symbol | Value | Range considered | Status | Owner | Source |
|---|---|---|---|---|---|---|
| **Elevation-model resolution used for clutter**<br>`dem_resolution` |  | TBD | 5 m – 120 m | 🔴 TBD | scene | LOLA products available for the target sites |
| **Clutter simulation method**<br>`clutter_method` |  | facet-based (each elevation-model facet is a scatterer) |  | 🟡 assumed | scene | team |
| **Monte Carlo runs per design point**<br>`monte_carlo_runs` |  | 200 | 50 – 1,000 | 🟡 assumed | systems | team |
| **Clock phase-noise model used in the simulation**<br>`clock_phase_noise_model` |  | TBD |  | 🔴 TBD | radar-hw | oscillator datasheet |
| **Basalt loss-tangent values to sweep**<br>`tan_delta_sweep` |  | 0.003, 0.01, 0.03, 0.06 |  | 🟡 assumed | scene | range of tan_delta_basalt |

