# D1.1 · Requirements

Turn the mission goal into numbers we can verify. Write requirements with **shall**, one idea each.
Values in `[brackets]` are register keys: the number lives in the register, not here.

**Mission goal:** map lava tubes beneath the lunar surface to identify sites for future lunar bases.

| ID | Requirement (draft) | Why | Verified by | Status |
|---|---|---|---|---|
| REQ-01 | The radar shall detect a void whose roof is at most `[roof_depth_max]` below the surface, with SNR ≥ `[snr_required]` after ground processing. | Core science goal | Analysis (BUDGET.md) → simulation V-05 | draft |
| REQ-02 | The radar shall resolve a void of height ≥ `[tube_height_min]` (vertical resolution ≤ `[vertical_resolution_req]` in basalt). | See roof and floor separately | Analysis (EQ-03) → simulation | draft |
| REQ-03 | After SAR processing, along-track resolution shall be ≤ `[along_track_resolution_req]`. | Resolve tubes of width ≥ `[tube_width_min]` | Simulation V-03 | draft |
| REQ-04 | The mission shall observe each site in `[target_sites]` at least `[passes_per_site]` times. | Repeat coverage and confirmation | Orbit analysis (GNC) | draft |
| REQ-05 | Radar data generated per day shall not exceed `[downlink_rate]` × `[contact_time_per_day]`. | Raw downlink must close | BUDGET.md | draft |
| REQ-06 | Radar peak and orbit-average power shall stay within `[payload_power_peak]` and `[payload_power_orbit_avg]`. | EPS allocation | BUDGET.md | draft |
| REQ-07 | Radar mass and stowed volume shall stay within `[payload_mass]` and `[payload_volume]`. | Structures allocation | Mass/volume estimate | draft |
| REQ-08 | Ground processing shall separate surface clutter from subsurface echoes at the target sites. | Avoid false lava tubes | Clutter simulation (Q3) | draft |
| REQ-09 | Depth estimates shall state their uncertainty from the permittivity range. | Honest depth maps | Analysis (EQ-02) | draft |

## Notes and open questions
- What lava-tube sizes does the literature support for lunar tubes? (sets `tube_height_min`, `tube_width_min`)
- Which sites does the orbit inclination allow? (with GNC)
