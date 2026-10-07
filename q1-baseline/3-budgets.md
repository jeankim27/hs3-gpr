# D1.5 · Interface agreements

Each row is a number the radar needs from another subteam, or a number it imposes on them.
Get the other lead to agree, then fill **Agreed with** and set the variable's status in the register.
Live numbers: [`BUDGET.md`](BUDGET.md).

## Power (EPS)
| Item | Radar needs | EPS provides | Register key | Agreed with |
|---|---|---|---|---|
| Peak DC power during a pulse | see BUDGET.md | | `payload_power_peak` | |
| Radar power averaged over a day | see BUDGET.md | | `payload_power_orbit_avg` | |
| Energy drawn per pulse (capacitor bank) | see BUDGET.md | | `tx_peak_power`, `pa_efficiency` | |

## Data (comms, C&DH)
| Item | Radar needs | Provided | Register key | Agreed with |
|---|---|---|---|---|
| Downlink rate for radar data | see BUDGET.md | | `downlink_rate` | |
| Contact time per day | | | `contact_time_per_day` | |
| Onboard memory for radar data | see BUDGET.md | | `mass_memory` | |

## Mass and volume (structures)
| Item | Estimate | Allocation | Register key | Agreed with |
|---|---|---|---|---|
| Radar electronics | | | `payload_mass` | |
| Antenna (stowed) | | | `payload_volume` | |

## Orbit and pointing (GNC, ADCS)
| Item | Radar needs | Provided | Register key | Agreed with |
|---|---|---|---|---|
| Altitude band and station-keeping | 30–100 km | | `altitude_min`, `altitude_max` | |
| Inclination (site access) | | | `inclination` | |
| Position knowledge (FOUND + tracking) | | | `orbit_knowledge_error` | |
| Attitude knowledge (LOST) | | | `attitude_knowledge_error` | |
| Antenna pointing | | | `pointing_accuracy` | |

## Noise (all electronics)
| Item | Radar needs | Provided | Register key | Agreed with |
|---|---|---|---|---|
| Spacecraft self-noise in the radar band | below galactic noise | | `bus_emi_limit` | |
