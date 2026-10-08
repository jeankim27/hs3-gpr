# Team roles

Five roles cover everything in this project. Each person owns one role and backs up one other.

The role tags (`systems`, `radar-hw`, `scene`, `processing`, `sim`) are the `owner:` values in
[`params/variables.yaml`](../params/variables.yaml) and the owners listed on each quarter's deliverables.
Picking a role tells you exactly which variables, flowchart steps and deliverables are yours.

Fewer than five people? One person takes two roles. Good pairs: `radar-hw` + `processing`, or `systems` + `sim`.

## The five roles

| Role | Tag | Owns (flowchart steps) | Main deliverables | Good fit |
|---|---|---|---|---|
| **Systems lead** | `systems` | Requirements, variable register, budgets, reviews, final report · steps 1–3, 25 | D1.1, D1.3, D1.5, D1.7, D3.7, D3.8 | Organized, comfortable with numbers; |
| **RF & antenna** | `radar-hw` | Frequency choice, chirp, transmitter, T/R switch, antenna, receiver, ADC, clock, calibration loopback · steps 4–8, 12–13 | TS-1, TS-2, receiver/ADC model (D2.3), error sources (D3.3) | EE: electromagnetics, circuits |
| **Lunar science & scene** | `scene` | Lunar materials (εr, tanδ), lava-tube sizes, target sites, attenuation, clutter, noise, depth conversion · steps 9–11, 23–24 | Environment research, scene model (D2.2), echo physics (D2.3), LOLA terrain and clutter (D3.1–D3.2) | Physics, Earth & space sciences; a strong researcher |
| **Signal processing** | `processing` | Presumming, downlink trade, pulse compression, geometry, SAR, multilook, detection · steps 14, 17, 19–22 | TS-3, onboard model (D2.4), SAR focusing (D2.5), clutter discrimination (D3.4) | EE signals/DSP, math, Python |
| **Simulation & software** | `sim` | Simulation framework, interfaces, tests, notebooks, repo, website, data formats · steps 15–16, 18 | Toolchain (D1.6), architecture (D2.1), verification suite (D2.6), demo lead (D2.7), detectability map (D3.5) | CS/ECE; the team's strongest programmer |

## Workload by quarter

| Role | Q1 · design baseline | Q2 · simulation | Q3 · final design |
|---|---|---|---|
| Systems | **Heavy**: requirements, budget, interfaces, review | Medium: verification sign-off, mid-project review | **Heavy**: system closure, final report |
| RF & antenna | **Heavy**: frequency and antenna trades | Medium: receiver and ADC model | Medium: clock noise and other error sources |
| Scene | **Heavy**: loss-tangent and lava-tube research | **Heavy**: scene model, echo physics | **Heavy**: LOLA terrain, clutter simulation |
| Processing | Medium: presum/downlink trade, learn SAR | **Heavy**: pulse compression, SAR focusing | Medium: clutter discrimination, detection |
| Simulation | Light: repo, notebooks, budget tool | **Heavy**: framework, tests, end-to-end runs | **Heavy**: Monte Carlo runs, reproducible pipeline |

In Q1 the simulation person has spare time: help the scene person with research and get comfortable with the code.

## Liaisons to other HS-3 subteams

Each number that comes from outside the team has one person here who chases it.

| Subteam | Liaison | What we need from them |
|---|---|---|
| HS-3 systems lead | `systems` | Allocations, schedule |
| EPS | `radar-hw` | Peak and orbit-average power |
| Structures, thermal | `radar-hw` | Mass, stowed volume, antenna deployment, temperatures |
| Comms | `processing` | Downlink rate, contact time |
| GNC / ADCS (LOST, FOUND) | `scene` | Inclination (site access), orbit and attitude knowledge |
| C&DH / flight computer | `sim` | Onboard memory, data formats |

## Backups

Each role has a backup who can cover during midterms or if someone leaves. Pairs share background knowledge.

| Role | Backup |
|---|---|
| `systems` | `sim` |
| `sim` | `systems` |
| `radar-hw` | `scene` |
| `processing` | `radar-hw` |
| `scene` | `systems` |
