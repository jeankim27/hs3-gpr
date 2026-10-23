# Ownership

Each area has one owner who makes its decisions and keeps its numbers in [`parameters.m`](parameters.m). A co-owner works alongside the owner and is usually taking the area over. Load is relative within this team: L light, M medium, H heavy.

## Team

| Name | Program | Status |
|---|---|---|
| [Jean Kim](https://github.com/jeankim27) | MSE, senior | Project lead · leaves after Q3 |
| Omar Alawi | ECE, junior | Continuing · hardware focus |
| Andy Cai | ECE, master's | Graduates before Q3 |
| Alex McNutt | ECE, sophomore | New member · next year's systems owner |
| Cris Hernandez | ECE, junior | New member |

**To add a GitHub link:** replace a plain name with `[Name](https://github.com/username)`.

## Who owns what

"A (B co-owns)" means A leads and B co-owns. "Archived" means the results live in the year-end report and `parameters.m`, with no owner in the build year.

| # | Area | Q1–Q2 | Q3 | Next year (build) | Load Q1 | Q2 | Q3 |
|---|---|---|---|---|---|---|---|
| 1 | [Lunar materials & dielectrics](#area-1) | Jean | Jean | Archived | H | M | M |
| 2 | [Target sites & regional data](#area-2) | Omar | Omar | Archived | H | H | M |
| 3 | [Surface roughness & clutter](#area-3) | Jean + Alex (Alex leads Q2) | Alex | Archived | M | H | H |
| 4 | [Antenna](#area-4) | Andy (Omar co-owns) | Omar | Omar | H | M | H |
| 5 | [Transmitter & waveform](#area-5) | Omar | Omar | Omar | M | M | H |
| 6 | [Receiver, ADC & clock](#area-6) | Andy + Alex (Alex leads Q2) | Alex | Alex | M | M | H |
| 7 | [Radar timing & control](#area-7) | Alex (Cris co-owns) | Alex (Cris co-owns) | Alex (Cris co-owns) | L | M | H |
| 8 | [Power, onboard data & downlink](#area-8) | Andy (Cris co-owns) | Cris | Cris | M | M | M |
| 9 | [Ground processing](#area-9) | Omar | Omar | Omar | M | H | H |
| 10 | [Orbit & observation geometry](#area-10) | Jean | Jean | Archived | M | H | M |
| 11 | [Systems integration & SNR/SCR model](#area-11) | Jean | Jean (Alex shadows) | Alex | H | M | H |
| 12 | [Simulation code & repo](#area-12) | Jean (merged into 11) | Jean (merged into 11) | Alex (merged into 11) | L | M | M |

Area 12 is part of the lead role: with MATLAB and a simple repo, integration doesn't need its own owner.

## Handoffs

- **Q1:** Andy leads 4, 6 and 8, with Omar co-owning 4, Alex co-owning 6 and Cris co-owning 8. Alex co-owns 3 with Jean.
- **Q2:** Alex takes the lead on 3 and 6; Jean and Andy review.
- **Week 20, Andy hands off:** at the frequency and target decision review, Alex presents 6, Cris presents 8 and Omar presents 4.
- **Q3:** Alex shadows 11 (decision records, requirements freeze, reviews).
- **Week 30, Jean hands off:** the year-end report and `parameters.m` carry areas 1–3 and 10 forward. Alex owns 11 next year.

## Workload

Points per quarter: H = 3, M = 2, L = 1, co-owning or shadowing = 1.

| Person | Q1 | Q2 | Q3 |
|---|---|---|---|
| Jean | 11 | 10 | 9 |
| Omar | 8 | 9 | 11 |
| Andy | 7 | 5 | graduated |
| Alex | 3 | 7 | 10 |
| Cris | 2 | 2 | 3 |

Open items: whether to keep the Monte Carlo runs in D3.4 now that Cris has joined, and whether Cris takes on more, since Cris has the lightest load and stays for the build year.

## Liaisons to other HS-3 subteams

| Subteam | Our liaison |
|---|---|
| HS-3 systems lead | [Area 11](#area-11) |
| EPS (power) | [Area 8](#area-8) |
| Comms | [Area 8](#area-8) |
| C&DH / flight computer | [Area 8](#area-8) |
| Structures, thermal | [Area 4](#area-4) |
| GNC / ADCS (LOST, FOUND) | [Area 10](#area-10) |

---

<a id="area-1"></a>
## 1. Lunar materials & dielectrics

- **Owns:** εr (from density), loss tangent (from FeO + TiO₂), attenuation in dB/m, Fresnel reflection and transmission at the surface and tube roof, time-to-depth conversion.
- **Q1:** Dielectric model with literature ranges for regolith, mare basalt and void.
- **Q2:** Attenuation and reflection values for each candidate site.
- **Q3:** Layered subsurface model (regolith over basalt over void) for second-order runs.
- **Works with:** Areas 2, 3.

<a id="area-2"></a>
## 2. Target sites & regional data

- **Owns:** Candidate lava-tube list within the target regions (Oceanus Procellarum and Mare Imbrium) and selection criteria. Regional context for each site: DEMs (LOLA, SLDEM, LROC NAC DTMs), imagery, composition maps. Data download and catalog.
- **Q1:** Site shortlist and a data inventory per site.
- **Q2:** Per-site data package used by the models; site ranking.
- **Q3:** Final target(s) with meter-scale surface data.
- **Works with:** Areas 1, 3, 10 (which latitudes we can reach).
- **Data sources:** [NASA open data: Moon](https://data.nasa.gov/dataset/?tags=moon) · [LROC QuickMap](https://quickmap.lroc.im-ldi.com/)

<a id="area-3"></a>
## 3. Surface roughness & clutter

- **Owns:** Roughness statistics (RMS height and slope), the roughness-loss term, clutter power, signal-to-clutter ratio (SCR) versus depth, DEM-based clutter simulation.
- **Q1:** First-order roughness loss using literature roughness values.
- **Q2:** First-order SCR versus depth and frequency for each site.
- **Q3:** Second-order modeling: Gaussian roughness statistics and clutter simulation from DEMs. Hurst fits as a stretch goal.
- **Works with:** Areas 2, 4 (off-nadir pattern), 9.

<a id="area-4"></a>
## 4. Antenna

- **Owns:** Antenna type and geometry (length, orientation), pattern and gain, impedance match over the bandwidth, deployment mechanism, stowed volume, interaction with the spacecraft body.
- **Q1:** Antenna options versus frequency (a half-wave dipole is 7.5 m at 20 MHz, 3 m at 50 MHz); gain and pattern for the link budget.
- **Q2:** Antenna input to the frequency decision; deployment concept; mass and volume to Structures.
- **Q3:** Pattern simulation including the spacecraft body; deployment prototype plan.
- **Works with:** Areas 3, 5; Structures/thermal and ADCS subteams.

<a id="area-5"></a>
## 5. Transmitter & waveform

- **Owns:** Chirp length, bandwidth and shape; chirp generator (DDS or FPGA + DAC); power amplifier; T/R switch; calibration loopback.
- **Q1:** Chirp time-bandwidth product and pulse-compression gain; transmit power options.
- **Q2:** Waveform spec, sidelobe and window trade, amplifier requirements.
- **Q3:** Benchtop chirp generation with loopback pulse compression on a software-defined radio.
- **Works with:** Areas 4, 6, 8, 9 (chirp replica).

<a id="area-6"></a>
## 6. Receiver, ADC & clock

- **Owns:** Limiter, LNA, filters, gain, ADC (sample rate, bits), noise floor (galactic, receiver, spacecraft, Earth RFI), master clock coherence.
- **Q1:** Noise-floor model; galactic noise dominates at these frequencies.
- **Q2:** Receiver chain spec, dynamic range, ADC choice.
- **Q3:** Receiver bench-test plan and clock stability budget.
- **Works with:** Areas 5, 7, 8 (data rate).

<a id="area-7"></a>
## 7. Radar timing & control

- **Owns:** PRF, receive-window delay, presum count, gain settings. Checks that a parameter set doesn't fail: echoes landing on the next transmit pulse, or Doppler aliasing after presumming. Radar controller FPGA.
- **Q1:** Timing constraints across the 30–100 km altitude range.
- **Q2:** Allowed PRF and presum region; command table.
- **Q3:** FPGA timing controller on a development board.
- **Works with:** Areas 6, 8, 9, 10.

<a id="area-8"></a>
## 8. Power, onboard data & downlink

- **Owns:** Peak and orbit-average power, transmit capacitor bank, duty cycle. Onboard coherent presumming, formatting and tagging, mass memory. Data volume and downlink budget.
- **Q1:** Power budget and data budget (for example, 24 Mbit/s raw becomes 1.5 Mbit/s after presumming by 16).
- **Q2:** Presum versus downlink trade, duty cycle per orbit, requirements sent to the EPS and Comms subteams.
- **Q3:** Onboard data format spec and power profile.
- **Works with:** Areas 7, 9; EPS, Comms and C&DH subteams.

<a id="area-9"></a>
## 9. Ground processing

- **Owns:** Decoding and RFI cleaning, pulse compression, geometry alignment, along-track SAR focusing, multilooking, cross-track clutter suppression using repeat passes.
- **Q1:** Processing-gain chain (pulse compression, SAR).
- **Q2:** End-to-end processing of a simple synthetic point target.
- **Q3:** Along-track SAR plus a cross-track repeat-pass demo on synthetic clutter scenes.
- **Works with:** Areas 3, 5, 7, 10.

<a id="area-10"></a>
## 10. Orbit & observation geometry

- **Owns:** Altitude, inclination, ground-track spacing, revisits and repeat-pass plan over targets, orbit and attitude knowledge requirements.
- **Q1:** Geometry basics: echo delays, ground speed, track spacing (about 31 km per orbit at the equator).
- **Q2:** Requirements memo for repeat-pass processing; estimate of the mission time it needs.
- **Q3:** Observation plan for the chosen target(s).
- **Works with:** Areas 2, 9; GNC/ADCS subteam.

<a id="area-11"></a>
## 11. Systems integration & SNR/SCR model

- **Owns:** The combined SNR/SCR model built from everyone's terms, [`parameters.m`](parameters.m), the frequency decision, reviews, final report.
- **Q1:** First-order SNR model that every area's term plugs into.
- **Q2:** Frequency and target decision at week 20.
- **Q3:** Second-order closure; hardware requirements freeze; build plan.
- **Works with:** Everyone; HS-3 systems lead.

<a id="area-12"></a>
## 12. Simulation code & repo

- **Owns:** Repo upkeep and folder tidiness. Helps other owners turn their models into working MATLAB code and combines them into one runnable model.
- **Q1:** Repo upkeep (light).
- **Q2:** Integrated first-order model, runnable end to end from `parameters.m`.
- **Q3:** Monte Carlo runs and a reproducible run of the final model.
- **Works with:** Everyone.
