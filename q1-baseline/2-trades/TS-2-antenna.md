# TS-2 · Antenna

- **Owner:** radar-hw · **Due:** week 8 · **Decision:** DR-002 (to write)
- **Register keys:** `antenna_type`, `antenna_length`, `antenna_gain`, `antenna_efficiency`, `payload_mass`, `payload_volume`

## Question
Which antenna gives enough efficiency and bandwidth at `f_center` while fitting the mass, volume and
deployment limits of a 6U/12U CubeSat?

## Options
| Option | Notes |
|---|---|
| Full half-wave dipole, deployable (tape spring) | Best efficiency; longest; deployment mechanism needed |
| Shorter dipole + matching network | Fits easily; radiation resistance and bandwidth drop as length shrinks |
| Crossed dipoles | Polarization diversity; twice the deployment |
| Monopole against the spacecraft body | Simpler; the bus becomes part of the antenna (pattern harder to predict) |

## Criteria (agree weights before scoring)
| Criterion | Weight | How measured |
|---|---|---|
| Radiation efficiency at f0 | 25% | estimate or simulation (e.g. NEC-based tools) |
| Usable bandwidth vs `bandwidth` | 20% | impedance match over the band |
| Stowed volume and mass | 20% | vs `payload_volume`, `payload_mass` |
| Deployment risk | 20% | mechanism complexity, heritage |
| Effect on clutter (pattern, orientation) | 15% | along- vs cross-track orientation |

## Results
| Option | Efficiency | Bandwidth OK? | Stowed size | Risk | Score |
|---|---|---|---|---|---|
| | | | | | |

## Recommendation
_2–3 sentences, then write DR-002 and update the register._
