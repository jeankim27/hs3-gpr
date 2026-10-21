# Q1 · First-order baseline (weeks 1–10)

**Question:** Which frequencies could work at all?

**Goal:** Build the first-order SNR model from the basic equation terms Adrian listed: antenna gain, geometric spreading, bedrock reflection, roughness loss, surface transmission, dielectric attenuation, noise floor, processing gains. Run it over a generic mare surface.

**Exit criterion:** SNR-versus-depth curves for 3 candidate frequencies, with the band narrowed to 1–2 candidates at the baseline review.

## Deliverables

Owners are listed in [ownership.md](../ownership.md). When you add a file, link it in the **Files** column.

| ID | Deliverable | Area | Files |
|---|---|---|---|
| D1.1 | First-order SNR model that reads `parameters.m`; every area's term plugs in | [11](../ownership.md#area-11) + all | |
| D1.2 | Dielectric model: εr, tanδ and attenuation ranges for regolith, basalt and void | [1](../ownership.md#area-1) | |
| D1.3 | Site shortlist and data inventory per site: DEMs, NAC DTMs, composition maps, prior sounder data | [2](../ownership.md#area-2) | |
| D1.4 | Roughness-loss term using literature roughness values | [3](../ownership.md#area-3) | |
| D1.5 | Antenna options versus frequency: length, gain, pattern, deployment feasibility | [4](../ownership.md#area-4) | |
| D1.6 | Waveform and transmit-power options; pulse-compression gain | [5](../ownership.md#area-5) | |
| D1.7 | Noise-floor model, including galactic noise | [6](../ownership.md#area-6) | |
| D1.8 | Timing and geometry constraints: echo delays, transmit eclipsing, Doppler limits after presumming | [7](../ownership.md#area-7), [10](../ownership.md#area-10) | |
| D1.9 | Power and data budget v1 | [8](../ownership.md#area-8) | |
| D1.10 | Answers from Adrian on the unclear notes (see [meeting notes](../notes/2026-10-adrian-jpl.md#open-questions-for-adrian)) | [11](../ownership.md#area-11) | |
